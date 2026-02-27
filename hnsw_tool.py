import os  # 导入操作系统模块，用于文件和目录操作
import json  # 导入JSON模块，用于读写JSON文件
import numpy as np  # 导入NumPy库，用于高效的数值运算，特别是数组操作
import hnswlib  # 导入HNSWlib库，用于高效的近似最近邻搜索
from text2vec import SentenceModel  # 从text2vec库导入SentenceModel，用于加载预训练模型并生成文本向量

# 1. 轮询 datawork 目录下的JSON文件并整理数据结构
def scan_and_process_datawork(root_dir):  # 定义函数，用于扫描指定目录并处理数据
    datawork_json = []  # 初始化一个列表，用于存储处理后的数据
    current_id = 0  # 初始化一个ID计数器，从0开始，作为向量的唯一标识
    
    # 遍历指定根目录下的所有文件和子目录
    for dirpath, _, filenames in os.walk(root_dir):  # 使用os.walk遍历目录树
        for filename in filenames:  # 遍历当前目录下的所有文件名
            if filename.endswith('.json'):  # 检查文件是否以.json结尾
                file_path = os.path.join(dirpath, filename)  # 构建文件的完整路径
                try:  # 使用try-except块来捕获和处理可能发生的异常
                    with open(file_path, 'r', encoding='utf-8') as f:  # 以只读模式打开文件，指定编码为utf-8
                        data = json.load(f)  # 解析JSON文件内容
                    
                    # 获取clazz（类名），优先使用'mainTabClazz'字段，如果不存在，则使用JSON文件名（不含扩展名）作为备用
                    clazz = data.get('mainTabClazz', os.path.splitext(filename)[0])  # 获取clazz标识
                    
                    # 提取'response'字段中的详细信息
                    if 'response' in data and isinstance(data['response'], dict):  # 检查'response'字段是否存在且为字典类型
                        for field, field_info in data['response'].items():  # 遍历'response'字典中的每一个字段
                            content = field_info.get('meaning')  # 获取字段描述'meaning'作为需要向量化的内容
                            if content:  # 确保'meaning'内容不为空
                                item = {  # 创建一个字典来存储提取的信息
                                    "id": current_id,  # 设置当前ID
                                    "content": content,  # 设置字段描述内容
                                    "clazz": clazz,  # 设置所属的类
                                    "field": field  # 设置字段名
                                }  # 结束条目构建
                                datawork_json.append(item)  # 将构建好的字典添加到结果列表中
                                current_id += 1  # ID计数器自增，为下一个条目做准备
                except Exception as e:  # 捕获在文件处理过程中可能发生的任何异常
                    print(f"处理 {file_path} 时出错: {e}")  # 打印错误信息和出错的文件路径
                    
    return datawork_json  # 返回包含所有处理后数据的列表

# 2. 加载文本向量化模型
# 加载HuggingFace上的预训练中文模型'shibing624/text2vec-base-chinese'
# 注意：首次运行时会自动从网上下载模型文件
print("正在加载模型 shibing624/text2vec-base-chinese (使用 text2vec)...")  # 打印模型加载提示信息
try:  # 尝试加载模型
    model = SentenceModel('shibing624/text2vec-base-chinese')  # 实例化SentenceModel并加载指定模型
except Exception as e:  # 捕获加载模型时可能发生的异常
    print(f"加载模型失败: {e}")  # 打印失败信息
    model = None  # 将model变量设置为None，表示模型不可用

# 3. 将数据存入 HNSWlib 索引
def save_to_hnsw(data_list, index_file="datawork_hnsw.index", meta_file="datawork_meta.json"):  # 定义函数，将数据保存为HNSW索引和元数据文件
    if not data_list:  # 检查输入的数据列表是否为空
        print("没有数据可保存。")  # 如果为空，则打印提示信息
        return  # 并提前退出函数
        
    print(f"正在为 {len(data_list)} 个条目生成向量...")  # 打印将要处理的条目数量
    contents = [item['content'] for item in data_list]  # 从数据列表中提取所有'content'字段，形成一个新列表
    
    if model is None:  # 检查模型是否已成功加载
        print("模型未加载，无法生成向量。")  # 如果模型不可用，打印提示
        return  # 并退出函数
        
    embeddings = model.encode(contents, show_progress_bar=True)  # 使用模型批量将文本内容编码为向量，并显示进度条
    
    # 将向量数组转换为numpy的float32类型，这是HNSWlib所要求的格式
    embeddings = np.array(embeddings).astype('float32')  # 转换数据类型
    
    # 获取向量的数量和维度
    num_elements, dimension = embeddings.shape  # 获取向量数组的形状（数量, 维度）
    
    # 声明HNSWlib索引
    # space='cosine'表示使用余弦相似度进行距离计算，这对于文本向量通常效果最好
    p = hnswlib.Index(space='cosine', dim=dimension)  # 创建一个HNSWlib索引实例
    
    # 初始化索引，设置最大元素数量和构建参数
    # ef_construction 和 M 是影响索引构建速度和查询精度的重要参数
    p.init_index(max_elements=num_elements, ef_construction=200, M=16)  # 初始化索引结构
    
    # 将向量和它们的ID（即它们在原始列表中的位置）添加到索引中
    p.add_items(embeddings, np.arange(num_elements))  # 添加数据到索引
    
    # 保存索引到二进制文件
    p.save_index(index_file)  # 将构建好的索引保存到磁盘
    print(f"HNSWlib 索引已保存到 {index_file}")  # 打印保存成功的提示
    
    # 保存元数据（用于通过ID映射回原始的详细信息）
    with open(meta_file, 'w', encoding='utf-8') as f:  # 以写入模式打开元数据文件
        json.dump(data_list, f, ensure_ascii=False, indent=2)  # 将原始数据列表以JSON格式写入文件，保持中文并格式化
    print(f"元数据已保存到 {meta_file}")  # 打印元数据保存成功的提示


# 4. 查询相似字段

# 全局变量，用于缓存索引和元数据，避免重复加载
p_query = None  # 查询用的HNSW索引对象
metadata = None # 查询用的元数据列表
MODEL_DIMENSION = 768 # shibing624/text2vec-base-chinese 模型的向量维度

def search_similar_fields(query_text, k=3, index_file="datawork_hnsw.index", meta_file="datawork_meta.json"):
    """
    根据文本查询，在HNSW索引中搜索最相似的字段。

    :param query_text: 用户输入的查询字符串。
    :param k: 希望返回的最相似结果的数量。
    :param index_file: 索引文件的路径。
    :param meta_file: 元数据文件的路径。
    :return: 一个包含相似结果的列表，每个结果都是一个字典。
    """
    global p_query, metadata # 声明使用全局变量

    # 检查向量化模型是否已加载
    if model is None:
        print("模型未加载，无法执行查询。")
        return []

    # 懒加载：仅在第一次查询时加载索引和元数据文件
    if p_query is None:
        try:
            print(f"正在加载索引文件 {index_file}...")
            p_query = hnswlib.Index(space='cosine', dim=MODEL_DIMENSION)  # 初始化索引对象
            p_query.load_index(index_file)  # 加载索引文件
        except Exception as e:
            print(f"加载索引文件失败: {e}")
            print("请先运行脚本生成索引文件。")
            return []

    if metadata is None:
        try:
            print(f"正在加载元数据文件 {meta_file}...")
            with open(meta_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f) # 加载元数据
        except Exception as e:
            print(f"加载元数据文件失败: {e}")
            return []

    # 1. 将用户的查询文本转换为向量
    query_vector = model.encode([query_text]) # 编码查询文本

    # 2. 在HNSW索引中执行k-近邻搜索
    # knn_query返回两个数组：(匹配项的ID, 匹配项的距离)
    labels, distances = p_query.knn_query(query_vector, k=k) # 执行查询

    # 3. 处理并格式化返回结果
    results = [] # 初始化结果列表
    for label, dist in zip(labels[0], distances[0]): # 遍历查询结果
        match = metadata[label] # 根据ID从元数据中获取详细信息
        results.append({ # 构建结果字典
            "similarity": 1 - dist,  # 将余弦距离转换为相似度（1 - 距离）
            "clazz": match['clazz'],  # 匹配到的类
            "field": match['field'],  # 匹配到的字段
            "content": match['content']  # 匹配到的字段描述
        }) # 结束结果字典构建
    
    return results # 返回格式化后的结果列表


def build_hnsw_index():
    # 定义datawork目录的路径
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本文件所在的绝对目录
    datawork_dir = os.path.join(base_dir, "datawork")  # 构建datawork目录的完整路径
    
    if not os.path.exists(datawork_dir):  # 检查datawork目录是否存在
        print(f"目录未找到: {datawork_dir}")  # 如果不存在，打印错误信息
    else:  # 如果目录存在
        # 1. 扫描并整理数据
        print("正在扫描 datawork 文件...")  # 打印开始扫描的提示
        json_data = scan_and_process_datawork(datawork_dir)  # 调用函数执行扫描和数据处理
        print(f"共找到 {len(json_data)} 个有效条目。")  # 打印找到的条目总数
        
        # 2. 存入 HNSWlib
        if json_data:  # 检查是否有数据需要处理
            save_to_hnsw(json_data)  # 调用函数，将处理好的数据生成索引并保存
            
# 主程序执行入口
if __name__ == "__main__":  # 确保以下代码只在直接运行此脚本时执行
    # 如果需要重新构建索引，请取消此行注释
    # print("--- 开始构建索引 ---")
    # build_hnsw_index()
    # print("--- 索引构建完成 ---\n")

    # --- 查询示例 ---
    print("--- 开始查询示例 ---")
    user_query = "订单结算客户" # 定义一个用户查询
    similar_fields = search_similar_fields(user_query, k=20) # 调用查询函数

    if similar_fields: # 如果有返回结果
        print(f"\n与 '{user_query}' 最相似的字段是:") # 打印提示
        for field in similar_fields: # 遍历结果
            print(
                f"  - 相似度: {field['similarity']:.4f}, " # 打印相似度
                f"表/类: {field['clazz']}, " # 打印表/类
                f"字段: {field['field']}, " # 打印字段
                f"描述: {field['content']}" # 打印描述
            ) # 结束打印