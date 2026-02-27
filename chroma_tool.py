import os  # 导入操作系统模块，用于文件和目录操作
import json  # 导入JSON模块，用于读写JSON文件
import chromadb  # 导入ChromaDB客户端库
from text2vec import SentenceModel  # 从text2vec库导入SentenceModel，用于加载预训练模型并生成文本向量

# 注意：此脚本现在使用客户端-服务器模式，需要一个正在运行的 ChromaDB 实例。
# 您可以使用 Docker 启动一个： docker run -p 8000:8000 chromadb/chroma
# chroma run --port 8008 --host 0.0.0.0 --path ./chroma_data
CHROMA_PORT = 8008

# --- 数据处理和模型加载 (与 hnsw_tool.py 相同) ---

# 1. 轮询 datawork 目录下的JSON文件并整理数据结构
def scan_and_process_datawork(root_dir):  # 定义函数，用于扫描指定目录并处理数据
    datawork_json = []  # 初始化一个列表，用于存储处理后的数据
    for dirpath, _, filenames in os.walk(root_dir):  # 遍历目录树
        for filename in filenames:  # 遍历当前目录下的所有文件名
            if filename.endswith('.json'):  # 检查文件是否以.json结尾
                file_path = os.path.join(dirpath, filename)  # 构建文件的完整路径
                try:  # 捕获和处理可能发生的异常
                    with open(file_path, 'r', encoding='utf-8') as f:  # 以只读模式打开文件
                        data = json.load(f)  # 解析JSON文件内容
                    clazz = data.get('mainTabClazz', os.path.splitext(filename)[0])  # 获取clazz标识
                    if 'response' in data and isinstance(data['response'], dict):  # 检查'response'字段
                        for field, field_info in data['response'].items():  # 遍历'response'字典
                            content = field_info.get('name')  # 获取字段描述
                            if content:  # 确保内容不为空
                                # 使用 clazz 和 field 组合成一个稳定且唯一的ID
                                stable_id = f"{clazz}-{field}"
                                item = {  # 创建一个字典来存储信息
                                    "id": stable_id,  # 设置稳定、唯一的字符串ID
                                    "content": content,  # 设置字段描述内容
                                    "clazz": clazz,  # 设置所属的类
                                    "field": field  # 设置字段名
                                }  # 结束条目构建
                                datawork_json.append(item)  # 将字典添加到结果列表
                except Exception as e:  # 捕获异常
                    print(f"处理 {file_path} 时出错: {e}")  # 打印错误信息
    return datawork_json  # 返回包含所有处理后数据的列表

def get_model():
    # 2. 加载文本向量化模型
    print("正在加载模型 shibing624/text2vec-base-chinese (使用 text2vec)...")  # 打印模型加载提示
    try:  # 尝试加载模型
        model = SentenceModel('shibing624/text2vec-base-chinese')  # 实例化SentenceModel并加载模型
        return model  # 返回加载的模型实例
    except Exception as e:  # 捕获加载异常
        print(f"加载模型失败: {e}")  # 打印失败信息
        return None

# --- ChromaDB 操作 ---

# 3. 构建或更新 ChromaDB 集合
def build_chroma_collection(model, data_list, host='localhost', port=CHROMA_PORT, collection_name="scheme"):  # 定义构建集合的函数
    if not data_list:  # 检查数据列表是否为空
        print("没有数据可用于构建集合。")  # 打印提示
        return  # 提前退出

    if model is None:  # 检查模型是否加载成功
        print("模型未加载，无法生成向量。")  # 打印提示
        return  # 提前退出

    print(f"正在为 {len(data_list)} 个条目生成向量...")  # 打印向量生成提示
    contents = [item['content'] for item in data_list]  # 提取所有待处理的文本内容
    embeddings = model.encode(contents, show_progress_bar=True)  # 批量将文本编码为向量

    print(f"正在连接到 ChromaDB 服务器 (地址: {host}:{port})...")  # 打印连接数据库的提示
    client = chromadb.HttpClient(host=host, port=port)  # 创建一个连接到服务器的ChromaDB客户端实例

    print(f"正在获取或创建集合: {collection_name}...")  # 打印集合操作的提示
    collection = client.get_or_create_collection(name=collection_name)  # 获取或创建一个新的集合

    batch_size = 5000  # 设置每个批次的大小，以避免超出ChromaDB的最大限制
    total_items = len(data_list)  # 获取数据总数
    for i in range(0, total_items, batch_size):  # 遍历所有数据，步长为批次大小
        batch_end = min(i + batch_size, total_items)  # 计算当前批次的结束索引
        print(f"正在向集合中添加/更新条目 {i + 1} 到 {batch_end} (共 {total_items} 条)...")  # 打印当前批次处理的进度信息

        # 为当前批次准备数据
        batch_data = data_list[i:batch_end]  # 获取当前批次的数据列表
        batch_embeddings = embeddings[i:batch_end]  # 获取当前批次的向量
        batch_documents = [item['content'] for item in batch_data]  # 获取当前批次的文档内容
        batch_metadatas = [{"clazz": item['clazz'], "field": item['field']} for item in batch_data]  # 获取当前批次的元数据
        batch_ids = [item['id'] for item in batch_data]  # 获取当前批次的ID

        collection.upsert(  # 使用upsert方法添加或更新当前批次的数据
            embeddings=batch_embeddings.tolist(),  # 将numpy数组格式的向量转换为列表
            documents=batch_documents,  # 提供当前批次的原始文本文档
            metadatas=batch_metadatas,  # 提供当前批次的元数据
            ids=batch_ids  # 提供当前批次的唯一ID列表
        )  # 结束当前批次的upsert操作
    print("集合构建/更新完成。")  # 所有批次处理完成后打印最终提示

# 4. 从 ChromaDB 查询相似字段
def search_similar_field_chroma(model, query_text, k=3, host='localhost', port=CHROMA_PORT, collection_name="scheme"):  # 定义查询函数
    if model is None:  # 检查模型是否可用
        print("模型未加载，无法执行查询。")  # 打印提示
        return []  # 返回空列表

    try:  # 捕获数据库连接和查询异常
        client = chromadb.HttpClient(host=host, port=port)  # 创建一个连接到服务器的ChromaDB客户端实例
        collection = client.get_collection(name=collection_name)  # 获取指定的集合
    except Exception as e:  # 捕获异常
        print(f"连接数据库或获取集合失败: {e}")  # 打印错误
        print("请确保 ChromaDB 服务器正在运行，并且集合已创建。")  # 提示用户检查服务器和集合
        return []  # 返回空列表

    query_vector = model.encode([query_text])  # 将用户的查询文本编码为向量

    print(f"正在集合 '{collection_name}' 中查询...")  # 打印查询提示
    results = collection.query(  # 执行查询
        query_embeddings=query_vector.tolist(),  # 提供查询向量
        n_results=k  # 指定返回最相似结果的数量
    )  # 结束查询

    formatted_results = []  # 初始化格式化结果的列表
    # ChromaDB返回的结果是包含多个列表的字典，需要解包处理
    ids, distances, metadatas, documents = results['ids'][0], results['distances'][0], results['metadatas'][0], results['documents'][0]
    for i in range(len(ids)):  # 遍历返回的每个结果
        formatted_results.append({  # 构建结果字典
            "similarity": 1 - distances[i],  # 将余弦距离转换为相似度
            "clazz": metadatas[i]['clazz'],  # 从元数据中获取clazz
            "field": metadatas[i]['field'],  # 从元数据中获取field
            "content": documents[i]  # 获取原始文档内容
        })  # 结束结果字典构建
    return formatted_results  # 返回格式化后的结果列表

def clear_chroma(host='localhost', port=CHROMA_PORT, collection_name="scheme"):
    """
    删除指定的 ChromaDB 集合。
    """
    try:
        print(f"正在连接到 ChromaDB 服务器 (地址: {host}:{port})...")
        client = chromadb.HttpClient(host=host, port=port)

        print(f"正在尝试删除集合: {collection_name}...")
        client.delete_collection(name=collection_name)
        print(f"集合 '{collection_name}' 已成功删除。")

    except Exception as e:
        # 捕获并处理集合不存在的特定异常
        error_message = str(e)
        # 根据ChromaDB的实现，它可能会在集合不存在时引发异常，错误信息中通常包含 "does not exist"
        if "does not exist" in error_message.lower():
            print(f"集合 '{collection_name}' 不存在，无需删除。")
        else:
            print(f"删除集合时发生未知错误: {e}")
            print("请确保 ChromaDB 服务器正在运行。")

def build_chroma():
    # --- 步骤一：构建索引 (如果需要，取消注释来运行) ---
    print("--- 开始构建 ChromaDB 集合 ---")
    model = get_model() # 统一加载模型
    if not model:
        return # 模型加载失败则退出

    base_dir = os.path.dirname(os.path.abspath(__file__)) # 获取当前脚本的绝对目录
    datawork_dir = os.path.join(base_dir, "scheme")  # 构建datawork目录的路径
    if os.path.exists(datawork_dir):  # 检查目录是否存在
         json_data = scan_and_process_datawork(datawork_dir)  # 扫描并处理数据
         if json_data:  # 如果有数据
             build_chroma_collection(model, json_data)  # 构建ChromaDB集合
    else:
        print(f"目录未找到: {datawork_dir}")
    print("--- 集合构建完成 ---\n")

def search():
    # --- 步骤二：执行查询 ---
    print("--- 开始查询示例 ---")  # 打印查询示例开始的提示
    model = get_model() # 统一加载模型
    if not model:
        return # 模型加载失败则退出

    user_query = "研发实际需时"  # 定义一个用户查询
    similar_fields = search_similar_field_chroma(model, user_query, k=5)  # 调用查询函数

    if similar_fields:  # 检查是否有返回结果
        print(f"\n与 '{user_query}' 最相似的字段是:")  # 打印查询结果的标题
        for field in similar_fields:  # 遍历每一个相似字段结果
            print(  # 打印格式化的结果
                f"  - 相似度: {field['similarity']:.4f}, "  # 打印相似度分数
                f"表/类: {field['clazz']}, "  # 打印所属的表/类
                f"字段: {field['field']}, "  # 打印字段名
                f"描述: {field['content']}"  # 打印字段的描述
            )  # 结束打印

# --- 主程序执行入口 ---
if __name__ == "__main__":  # 确保以下代码只在直接运行此脚本时执行
    #clear_chroma()
    build_chroma()
    #search()

