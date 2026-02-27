import os  # 导入操作系统模块
import json  # 导入 JSON 处理模块
import numpy as np  # 导入 numpy 用于数组处理
import faiss  # 导入 FAISS 用于向量检索
from sentence_transformers import SentenceTransformer  # 导入 SentenceTransformer 用于加载模型

# 1. 轮询 datawork JSON 文件并整理
def scan_and_process_datawork(root_dir):  # 定义函数，参数为根目录
    datawork_json = []  # 初始化结果数组
    current_id = 1  # 初始化 ID 计数器
    
    # 遍历目录
    for dirpath, _, filenames in os.walk(root_dir):  # 遍历目录树
        for filename in filenames:  # 遍历文件
            if filename.endswith('.json'):  # 筛选 JSON 文件
                file_path = os.path.join(dirpath, filename)  # 拼接完整路径
                try:  # 尝试读取文件
                    with open(file_path, 'r', encoding='utf-8') as f:  # 打开文件
                        data = json.load(f)  # 加载 JSON 数据
                    
                    # 获取 clazz，优先使用 mainTabClazz，否则使用文件名
                    clazz = data.get('mainTabClazz', os.path.splitext(filename)[0])  # 获取 clazz
                    
                    # 提取 response 中的字段
                    if 'response' in data and isinstance(data['response'], dict):  # 检查 response 字段
                        for field, field_info in data['response'].items():  # 遍历 response 字段
                            content = field_info.get('meaning')  # 获取 meaning 作为 content
                            if content:  # 如果 content 存在
                                item = {  # 构建条目
                                    "id": f"{current_id:04d}",  # 格式化 ID，例如 0001
                                    "content": content,  # 设置 content
                                    "clazz": clazz,  # 设置 clazz
                                    "field": field  # 设置 field
                                }  # 结束条目构建
                                datawork_json.append(item)  # 添加到数组
                                current_id += 1  # ID 自增
                except Exception as e:  # 捕获异常
                    print(f"Error processing {file_path}: {e}")  # 打印错误信息
                    
    return datawork_json  # 返回结果数组

# 2. 辅助函数：获取向量
# 加载 HuggingFace 上的中文模型 shibing624/text2vec-base-chinese
# 注意：首次运行会自动下载模型
print("Loading model shibing624/text2vec-base-chinese...")  # 打印加载提示
try:
    model = SentenceTransformer('shibing624/text2vec-base-chinese')  # 加载模型
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def get_embedding(text):  # 定义获取向量的函数
    """
    获取文本的向量表示
    """
    if model is None: 
        raise ValueError("Model not loaded")
    # 使用 model.encode 获取向量
    embedding = model.encode(text)  # 编码文本
    return embedding  # 返回向量



# 3. 存入数据到 FAISS
def save_to_faiss(data_list, index_file="datawork.index", meta_file="datawork_meta.json"):  # 定义保存函数
    if not data_list:  # 检查数据是否为空
        print("No data to save.")  # 打印提示
        return  # 返回
        
    print(f"Generating embeddings for {len(data_list)} items...")  # 打印进度
    contents = [item['content'] for item in data_list]  # 提取 content 列表
    
    # 批量获取向量
    if model is None:
        print("Model not loaded, cannot generate embeddings.")
        return
        
    embeddings = model.encode(contents)  # 获取所有文本的向量
    
    # 转换为 numpy float32 数组，FAISS 需要
    embeddings = np.array(embeddings).astype('float32')  # 转换数据类型
    
    # 创建索引
    dimension = embeddings.shape[1]  # 获取向量维度
    index = faiss.IndexFlatL2(dimension)  # 创建 L2 距离索引
    
    # 添加向量到索引
    index.add(embeddings)  # 添加向量
    
    # 保存索引到文件
    faiss.write_index(index, index_file)  # 保存索引
    print(f"FAISS index saved to {index_file}")  # 打印保存成功
    
    # 保存元数据（用于映射 ID 到具体内容）
    with open(meta_file, 'w', encoding='utf-8') as f:  # 打开元数据文件
        json.dump(data_list, f, ensure_ascii=False, indent=2)  # 写入 JSON
    print(f"Metadata saved to {meta_file}")  # 打印保存成功

# 主执行块
if __name__ == "__main__":  # 如果是主程序运行
    # datawork 目录路径
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本目录
    datawork_dir = os.path.join(base_dir, "datawork")  # 拼接 datawork 目录
    
    if not os.path.exists(datawork_dir):  # 检查目录是否存在
        print(f"Directory not found: {datawork_dir}")  # 打印错误
    else:  # 如果存在
        # 1. 获取并整理数据
        print("Scanning datawork files...")  # 打印提示
        json_data = scan_and_process_datawork(datawork_dir)  # 执行扫描
        print(f"Found {len(json_data)} items.")  # 打印结果数量
        
        # 3. 存入 FAISS
        if json_data:  # 如果有数据
            save_to_faiss(json_data)  # 保存到 FAISS
