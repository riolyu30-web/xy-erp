import os  # 导入操作系统模块，用于文件和目录操作
import json  # 导入JSON模块，用于读写JSON文件
import chromadb  # 导入ChromaDB客户端库
from text2vec import SentenceModel  # 从text2vec库导入SentenceModel，用于加载预训练模型并生成文本向量
from services.llm_manager import dashscope_chat_json
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
                            content = field_info.get('meaning')  # 获取字段描述
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
        similarity = 1 - distances[i]  # 计算相似度
        formatted_results.append({  # 构建结果字典
                "similarity": similarity,  # 设置相似度
                "clazz": metadatas[i]['clazz'],  # 从元数据中获取clazz
                "field": metadatas[i]['field'],  # 从元数据中获取field
                "content": documents[i]  # 获取原始文档内容
            })  # 结束结果字典构建
    return formatted_results  # 返回格式化后的结果列表

def search_similar_fields_in_batch(model, fields, k=100, host='localhost', port=CHROMA_PORT, collection_name="scheme"):
    """
    接收一个字段数组，为每个字段查询相似结果，并返回一个字典。
    """
    # 初始化一个空字典来存储所有字段的查询结果
    all_results = {}
    # 遍历传入的字段数组
    for field_query in fields:
        # 为当前字段调用单次查询函数
        similar_fields = search_similar_field_chroma(model, field_query, k, host, port, collection_name)
        # 将查询结果存入字典，键为字段名
        all_results[field_query] = similar_fields

   

    # 获取当前脚本的绝对目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 构建mcp_relation.json的路径
    mcp_relation_path = os.path.join(base_dir, "mcp_relation.json")
    
    # 存储所有有关联关系的clazz对
    related_clazz_pairs = set()

    # 读取mcp_relation.json并解析关联关系
    if os.path.exists(mcp_relation_path):
        try:
            with open(mcp_relation_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 处理 parent 列表
                if "parent" in data and isinstance(data["parent"], list):
                    for item in data["parent"]:
                        s = item.get("s")
                        t = item.get("t")
                        if s and t:
                            related_clazz_pairs.add(tuple(sorted((s, t))))
                            
                # 处理 relation 列表 (如果存在)
                if "link" in data and isinstance(data["link"], list):  # 检查 link 键是否存在且值为列表
                    for item in data["link"]:  # 遍历 link 列表中的每一项
                        s = item.get("s")  # 获取源节点 s
                        t = item.get("t")  # 获取目标节点 t
                        if s and t:  # 如果源节点和目标节点都存在
                            related_clazz_pairs.add(tuple(sorted((s, t))))  # 将排序后的元组添加到集合中去重
        except Exception as e:
             print(f"读取或解析 mcp_relation.json 失败: {e}")

    # 统计所有结果中每个clazz出现的次数，用于后续过滤
    clazz_counts = {}
    # 遍历所有字段的查询结果
    for items in all_results.values():
        # 使用集合记录当前字段结果中已出现的clazz，避免单字段重复计数
        seen_clazz = set()
        # 遍历当前字段的每个结果项
        for item in items:
            # 获取当前结果项的clazz值
            c = item.get('clazz')
            # 如果clazz存在且当前字段未记录过
            if c and c not in seen_clazz:
                # 将该clazz的计数加1
                clazz_counts[c] = clazz_counts.get(c, 0) + 1
                # 标记该clazz在当前字段已出现
                seen_clazz.add(c)

    # 筛选出出现次数大于1的clazz，且这些clazz之间存在关联关系
    valid_clazzes = set()
    
    # 获取所有出现次数大于1的clazz
    potential_clazzes = [c for c, count in clazz_counts.items() if count > 1]

    print(clazz_counts)
    
    # 检查这些clazz是否在关联关系中
    for i in range(len(potential_clazzes)):
        for j in range(i + 1, len(potential_clazzes)):
            c1 = potential_clazzes[i]
            c2 = potential_clazzes[j]
            # 检查c1和c2是否有关联
            if tuple(sorted((c1, c2))) in related_clazz_pairs:
                valid_clazzes.add(c1)
                valid_clazzes.add(c2)

    # 如果存在有效的关联clazz，则进行排序，优先保留这些clazz的数据，并只保留前三
    if valid_clazzes:
        # 遍历结果字典的每个键
        for key in all_results:
            # 获取当前字段的结果列表
            items = all_results[key]
            
            # 1. 按照优先级排序 
            # 逻辑: 相似度 > 0 按 相似度高到低排序; 相似度 <= 0 执行原逻辑(valid_clazzes优先, 出现次数多优先)
            items.sort(key=lambda x: (
                0, -x.get('similarity', 0), 0
            ) if x.get('similarity', 0) > 0 else (
                1, 
                0 if x.get('clazz') in valid_clazzes else 1, 
                -clazz_counts.get(x.get('clazz'), 0)
            ))
            
            # 2. 去重: 每个clazz只保留第一个出现的
            unique_items = []
            seen_clazzes_in_list = set()
            for item in items:
                clazz = item.get('clazz')
                if clazz not in seen_clazzes_in_list:
                    unique_items.append(item)
                    seen_clazzes_in_list.add(clazz)
            
            # 3. 过滤: 只保留在valid_clazzes中的项 (根据用户最新要求: "然后再过滤掉不在valid_clazzes的")
            # 注意: 如果不需要强制过滤掉不在valid中的，可以去掉这一步。但用户明确说 "然后再过滤掉不在valid_clazzes的"
            final_items = [item for item in unique_items if item.get('clazz') in valid_clazzes]
            
            # 如果过滤后为空(可能没有valid的)，是否要保留原有的？
            # 根据用户指令 "改为 每个clazz只保留第一个 然后再过滤掉不在valid_clazzes的"
            # 严格执行: 结果可能为空。但为了体验，如果为空，可能还是保留前几个比较好？
            # 暂时严格按照指令执行。如果结果为空，说明没有关联关系匹配上。
            
            # 如果valid_clazzes本身就为空(前面判断了if valid_clazzes)，那么这里肯定为空。
            # 但外层有 if valid_clazzes: 保护。
            
            # 只保留前5个 (保留原有的截取逻辑，虽然去重过滤后可能很少了)
            all_results[key] = final_items[:5]

    print(json.dumps(all_results, ensure_ascii=False, indent=4))

    #fields_str = "、".join(fields) # 将字段列表用顿号连接成一个字符串
    system_prompt = """你是擅长大数据的数据分析专家，能在尽量共相同表的前提下，为每个查询需求配置最合适的字段(无需带表名)，返回JSON格式的键值对，严格遵守格式如:{"best":{"合同创建人":"contractDetailContractCreator","业务订单明细更新时间":"bizOrderDetailBizOrderUpdateTime"}}""" 
    #print(system_prompt)
    # 使用 f-string 将多个部分拼接成最终的提示字符串
    data = dashscope_chat_json(system_prompt,json.dumps(all_results, ensure_ascii=False, indent=4),model="qwen-plus")
    if data and "best" in data:
        print(data["best"])
        return {"message": data["best"]}
    else:
        return {"error": all_results}


    # 返回包含所有结果的字典
    #return all_results


# 5. 根据指定的 clazz 和 field 查找相似字段
def get_similar_fields(model, clazz, field, k=3, host='localhost', port=CHROMA_PORT, collection_name="scheme"):
    """
    通过指定的 clazz 和 field，找到其对应的描述，并以此为基础查询最相似的其他字段。
    """
    try:  # 捕获数据库连接和查询异常
        client = chromadb.HttpClient(host=host, port=port)  # 创建一个连接到服务器的ChromaDB客户端实例
        collection = client.get_collection(name=collection_name)  # 获取指定的集合
    except Exception as e:  # 捕获异常
        print(f"连接数据库或获取集合失败: {e}")  # 打印错误
        return []  # 返回空列表

    # 使用 where 过滤器精确查找对应的条目
    retrieved = collection.get(
        where={"$and": [{"clazz": clazz}, {"field": field}]},
        limit=1
    )

    # 检查是否找到了文档
    if not retrieved or not retrieved['documents']:
        print(f"在集合中未找到 clazz='{clazz}' 和 field='{field}' 对应的条目。")
        return []

    # 获取找到的第一个文档的描述作为查询文本
    query_text = retrieved['documents'][0]
    print(f"找到条目 '{clazz}.{field}'，使用其描述 '{query_text}' 进行相似性查询...")

    # 复用现有的相似性搜索函数
    return search_similar_fields_chroma(model, query_text, k=k, host=host, port=port, collection_name=collection_name)

def build_chroma():
    # --- 步骤一：构建索引 (如果需要，取消注释来运行) ---
    print("--- 开始构建 ChromaDB 集合 ---")
    model = get_model() # 统一加载模型
    if not model:
        return # 模型加载失败则退出

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 获取当前脚本的绝对目录
    datawork_dir = os.path.join(base_dir, "datawork")  # 构建datawork目录的路径
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

    user_query = "订单结算客户"  # 定义一个用户查询
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

def search_similar_field(user_query:str):
    model = get_model() # 统一加载模型
    if not model:
        return None# 模型加载失败则退出
    similar_fields = search_similar_field_chroma(model, user_query, k=10)  # 调用查询函数
    return similar_fields


# --- 主程序执行入口 ---
if __name__ == "__main__":  # 确保以下代码只在直接运行此脚本时执行
    build_chroma()
    #search()

