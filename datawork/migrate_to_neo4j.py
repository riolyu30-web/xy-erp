import os
import sys

# from numpy._core import records

# 添加父目录到 sys.path 以便导入 services
current_dir = os.path.dirname(os.path.abspath(__file__)) # 获取当前文件所在目录
parent_dir = os.path.dirname(current_dir) # 获取父目录 (erp-service)
sys.path.append(parent_dir) # 将父目录加入系统路径
# from services.R import *
from dotenv import load_dotenv # 导入 dotenv 库
root_dir = os.path.dirname(parent_dir) # 获取项目根目录
load_dotenv() # 加载根目录下的 .env 文件

import re
from neo4j import GraphDatabase
import psycopg2
import pandas as pd
import json
import services.auth_service as auth_service
import requests
import json # 导入json库

# ================= 配置区 =================
# Neo4j 配置 (请根据你的实际情况修改)
NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"  # 替换为你刚才设置的密码

# Supabase (Postgres) 配置
PG_CONN_STR = "postgresql://192.168.0.33:5432/xy_erp_fwz_ai_test?user=root&password=123456"

# 从环境变量获取配置
BASE_URL = os.getenv("BASE_URL", "http://192.168.0.156:28002") 
# 文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEME_DIR =  os.path.join(os.path.dirname(BASE_DIR), 'scheme')
MCP_RELATION_PATH = os.path.join(os.path.dirname(BASE_DIR), 'mcp_relation.json')

    
def readJSON(access_token):
    """
    读取当前目录及子目录下的所有 JSON 文件，
    并将其内容存储到一个字典中，键为文件名（不包含扩展名），值为 JSON 内容。
    """
    print("开始读取 JSON 文件...")
    json_data = {}
    # 获取脚本所在目录 (datawork)
    
    for root, dirs, files in os.walk(SCHEME_DIR):
        for file in files:
        #file = files[0]
        #if file:
            if not file.lower().endswith('.json'):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 提取文件名（不包含扩展名）作为键
                    json_data[os.path.splitext(file)[0]] = data

                    records = getData(access_token, data)
                                           
                    if records:
                            print(f"  -> 获取到 {len(records)} 条数据，准备写入 Neo4j...")
                            # 获取节点 Label (从 mainTabClazz)
                            label_name = data.get('mainTabClazz', 'UnknownTable')
                            
                            # 获取 Schema 映射 (字段名 -> 中文含义)
                            # response 结构: { "fieldName": { "meaning": "xxx" }, ... }
                            schema_map = data.get('response', {})
                            
                            # 执行写入
                            save_to_neo4j(label_name, records, schema_map)
                    else:
                        print(f"  -> 接口返回数据为空")
                    

                    
            except json.JSONDecodeError:
                print(f"  [错误] 无法解析 JSON")


def save_to_neo4j(label, records, schema_map):
        """
        将数据写入 Neo4j
        :param label: 节点 Label (例如 CUST_STATEMENT_DET)
        :param records: 数据列表 (List[Dict])
        :param schema_map: 字段含义映射 (Dict)
        """

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        # 验证连接是否可用
        driver.verify_connectivity()
        print("✅ 连接成功！Neo4j 服务运行正常且可访问。")
        
        # 简单查询测试
        with driver.session() as session:
            # 1. 确定主键
            pk_field = None
            
            # 优先从 Schema 中查找 is_primary=True 的字段
            if schema_map:
                for field_name, props in schema_map.items():
                    if isinstance(props, dict) and props.get('is_primary') is True:
                        pk_field = field_name
                        break
            
            if not pk_field:
                # 优先寻找 'id' 字段，如果没有则寻找以 'Id' 结尾的第一个字段，或者 'code'
                pk_field = 'id'
                sample = records[0] if records else {}
                if 'id' not in sample:
                    # 尝试智能推断主键
                    for key in sample.keys():
                        if key.lower().endswith('id') and 'parent' not in key.lower():
                            pk_field = key
                            break
            
            #print(f"  -> 使用主键字段: {pk_field}")
            
            # 1.5 创建唯一性约束 (优化查询性能)
            try: # 尝试创建约束
                # 构建创建唯一性约束的 Cypher 语句，使用 IF NOT EXISTS 防止报错
                constraint_query = f"CREATE CONSTRAINT `{label}_pk` IF NOT EXISTS FOR (n:`{label}`) REQUIRE n.`{pk_field}` IS UNIQUE"
                session.run(constraint_query) # 执行创建约束
                print(f"  ✅ [优化] 已检查/创建唯一性约束: {label}.{pk_field}") # 打印成功信息
            except Exception as e: # 捕获创建约束时的异常
                print(f"  ⚠️ [警告] 创建约束失败 (可能是旧版本Neo4j或权限不足): {e}") # 打印警告信息

            # 2. 构造 Cypher 语句
            # 使用 UNWIND 批量插入
            # 注意：Neo4j Label 不能包含特殊字符，这里假设 mainTabClazz 是合法的
            
            cypher = f"""
            UNWIND $rows AS row
            MERGE (n:`{label}` {{ `{pk_field}`: row.`{pk_field}` }})
            SET n += row
            """
            
            # 3. 执行
            try:
                # 预处理数据：将复杂对象转为字符串，避免 Neo4j 报错
                cleaned_rows = []
                for row in records:
                    cleaned = {}
                    for k, v in row.items():
                        # 只保留 schema 中定义的字段，或者全部保留？
                        # 这里选择全部保留，但要确保格式正确
                        if isinstance(v, (dict, list)):
                            cleaned[k] = json.dumps(v, ensure_ascii=False)
                        else:
                            cleaned[k] = v
                    cleaned_rows.append(cleaned)

                # 批量写入逻辑
                batch_size = 2000 # 设置每批次处理的数据量
                total = len(cleaned_rows) # 获取总数据量
                print(f"  🚀 开始批量写入，总数: {total}, 批次大小: {batch_size}") # 打印开始信息
                
                for i in range(0, total, batch_size): # 遍历数据，按批次处理
                    batch = cleaned_rows[i : i + batch_size] # 获取当前批次的数据
                    session.run(cypher, rows=batch) # 执行当前批次的写入
                    print(f"    -> 进度: {min(i + batch_size, total)} / {total}") # 打印进度
                
                print(f"  ✅ 成功完成所有写入 (Label: {label})") # 打印完成信息
                
                # 4. (可选) 为字段添加中文注释属性? 
                # 目前 Neo4j 属性只能存储值，不能存储"字段含义"。
                # "字段含义"通常作为元数据存储，或者在前端展示时映射。
                
            except Exception as e:
                print(f"  ❌ Neo4j 写入异常: {e}")



def getData(access_token,data):
                try:
                    url = data["api_name"]

                    params = data["request"]
                    
                    url = f"{BASE_URL}{url}?access_token={access_token}"

                    # 发送POST请求
                    if params:
                        response = requests.post(url, json=params)
                        
                    response.raise_for_status()  # 检查请求是否成功
                    
                    # 解析响应数据
                    result = response.json()
                    
                    # 检查响应中是否包含data字段
                    if "data" not in result:
                        return {"error": "没有权限"}
                    
                    # 提取数据列表
                    return result["data"]
                except Exception as e:
                    print(f"  ❌ 获取数据异常: {e}")
                    return None

def create_relations_from_link_table(source_label, target_label, rel_type, link_data, source_key="sourceId", target_key="targetId"):
    # 检查是否有关系数据，如果没有则直接返回
    if not link_data:
        # 打印警告信息
        print("⚠️ 没有关系数据，跳过")
        # 结束函数执行
        return

    # 过滤无效数据：linkSource 或 linkTarget 为空的数据
    valid_link_data = [
        item for item in link_data 
        if item.get('linkSource') is not None and item.get('linkTarget') is not None
    ]
    
    invalid_count = len(link_data) - len(valid_link_data)
    if invalid_count > 0:
        print(f"  ⚠️ 发现 {invalid_count} 条无效关系数据 (source 或 target 为空)，已跳过")
        
    link_data = valid_link_data
    if not link_data:
        print("  ⚠️ 过滤后无有效关系数据，跳过")
        return

    # 连接到 Neo4j 数据库
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    # 打印开始创建关系的信息
    print(f"🚀 开始批量创建关系: ({source_label}) -[{rel_type}]-> ({target_label})，共 {len(link_data)} 条")
    
    # 设置每批处理的大小
    batch_size = 5000
    # 获取关系数据的总数
    total = len(link_data)
    
    # 定义 Cypher 查询语句
    cypher = f"""
    UNWIND $batch AS item
    MERGE (s:`{source_label}` {{`{source_key}`: item.linkSource}})
    MERGE (t:`{target_label}` {{`{target_key}`: item.linkTarget}})
    MERGE (s)-[:`{rel_type}`]->(t)
    """
    
    # 创建一个会话来执行查询
    with driver.session() as session:
        # 分批处理数据
        for i in range(0, total, batch_size):
            # 获取当前批次的数据
            batch = link_data[i : i + batch_size]
            # 执行 Cypher 查询
            session.run(cypher, batch=batch)
            # 打印处理进度
            print(f"    -> 进度: {min(i + batch_size, total)} / {total}")
            
    # 打印关系导入完成的信息
    print(f"  ✅ 关系导入完成")
    # 关闭数据库连接
    driver.close()


def get_link_data(access_token: str, relation_info: dict):  # 定义测试函数
    """
    根据关系对象获取数据并创建链接
    """
    source_clazz = relation_info.get("s") # 获取源节点标签
    target_clazz = relation_info.get("t") # 获取目标节点标签
    clazz = source_clazz+"-"+target_clazz # 获取关系名称，用于API调用

    if not source_clazz or not target_clazz or not clazz: # 检查关系对象是否完整
        print(f"  ⚠️ 解析关系对象失败，跳过: {relation_info}") # 如果不完整，打印警告并跳过
        return # 返回

    data = {} # 初始化数据字典
    # 构建请求URL
    data["api_name"] = "/proof/linkFindList"  # API地址

    # 构建请求体数据
    data["request"] = {
        "linkTypeCode": "source",  # 固定参数
        "linkClazz": clazz,  # 使用从对象中获取的关系名称
    }  # 数据字典结束

    source_key = get_key(source_clazz) # 获取源节点的键
    target_key = get_key(target_clazz) # 获取目标节点的键
    print(f"  🔑 源表 {source_clazz} 主键: {source_key}") # 打印源表主键
    print(f"  🔑 目标表 {target_clazz} 主键: {target_key}") # 打印目标表主键

    link_records = getData(access_token, data) # 调用getData获取链接记录
    if link_records: # 如果获取到记录
        print(f"  🚀 成功获取 {clazz} 源数据，总数: {len(link_records)}") # 打印成功信息和数量
        create_relations_from_link_table(source_clazz, target_clazz, clazz, link_records, source_key, target_key) # 创建表间关系
        return link_records
    else: # 如果没有获取到记录
        print(f"  🤷‍♂️ {clazz} 未获取到源数据") # 打印未获取到数据的提示



def parse_relation(relation: str):
    """
    解析关系字符串，返回源节点标签和目标节点标签列表
    """
    parts = relation.split('-')
    if len(parts) < 2:
        return None, None

    source_label = parts[0].strip()
    target_part = parts[1].strip()
    
    # 处理 Target 中可能有 '&' 的情况
    if '&' in target_part:
        #print(f"  ⚠️ 跳过复杂关系 (包含 '&'): {line}")
        return None, None
    
    return source_label, target_part   

def get_key(clazz: str):
    """
    根据 clazz (表名/Label) 查找对应的 JSON 文件，并返回 is_primary=true 的字段名 (主键)
    """
    # 假设 JSON 文件存储在 'json' 目录下，并且文件名与 clazz 一致 (区分大小写，或统一大写?)
    # 这里我们遍历目录来找，或者假设文件名就是 clazz + .json
    
    # 获取 datawork 目录 (migrate_to_neo4j.py 所在目录)
   
    # 搜索范围：datawork 下的所有子目录
    # 因为文件可能在 '仓库相关接口', '订单相关接口' 等子文件夹里
    json_file_path = None
    
    for root, dirs, files in os.walk(SCHEME_DIR):
        # 简单匹配: 忽略大小写
        for file in files:
            if file.lower() == f"{clazz}.json".lower():
                json_file_path = os.path.join(root, file)
                break
        if json_file_path:
            break
            
    if not json_file_path:
        #print(f"  ⚠️ 未找到 {clazz} 对应的 JSON 配置文件")
        # 默认返回 'id' 或者根据命名规则猜测
        # 比如 FIN_INSTORAGE -> finInstorageId ?
        # 还是先返回 'id' 比较稳妥
        return 'id'
    # 设置一个默认的父ID键名
    guessed_id = 'id'        
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 遍历 response 字段寻找 is_primary == true
        response_schema = data.get('response', {})
        for field_name, props in response_schema.items():
            if props.get('is_primary') == True:
                #print(f"  -> 找到主键: {field_name} (for {clazz})")
                return field_name
        # 从JSON数据中获取 'api_name' 字段，如果不存在则返回空字符串
        api_name = data.get('api_name', "")
        # 检查 'api_name' 是否存在且以 '/' 开头
        if api_name and api_name.startswith('/'):
            # 移除 'api_name' 开头和结尾的 '/'，然后按 '/' 分割，并取第一个部分
            # 例如, "/biz-order/findList" -> "biz-order"
            name_part = api_name.strip('/').split('/')[0]
            
            # 按 '-' 分割字符串
            # 例如, "biz-order" -> ['biz', 'order']
            words = name_part.split('-')
            
            # 将分割后的单词列表转换为驼峰命名法
            # 例如, ['biz', 'order'] -> "bizOrder"
            camel_case_name = words[0] + "".join(word.capitalize() for word in words[1:])
            
            # 在驼峰命名的基础上拼接 "ParentId"
            # 例如, "bizOrder" -> "bizOrderParentId"
            guessed_id = f"{camel_case_name}Id"
        else:
            if '_' in clazz:
                components = clazz.lower().split('_')
                # 第一个单词小写，后面单词首字母大写
                camel_case = components[0] + ''.join(x.title() for x in components[1:])
            else:
                # 如果没有下划线，直接转小写? 或者保持原样? 通常是全小写
                camel_case = clazz.lower()
                
            guessed_id = f"{camel_case}Id"

    except Exception as e:
        print(f"  ⚠️ 读取/解析 {json_file_path} 失败: {e}")
        
    return guessed_id

def get_parent_key(clazz:str):

    json_file_path = None
    
    for root, dirs, files in os.walk(SCHEME_DIR):
        # 简单匹配: 忽略大小写
        for file in files:
            if file.lower() == f"{clazz}.json".lower():
                json_file_path = os.path.join(root, file)
                break
        if json_file_path:
            break
            
    if not json_file_path:
        # 如果找不到JSON配置文件，则打印警告信息
        # print(f"  ⚠️ 未找到 {clazz} 对应的 JSON 配置文件")
        # 默认返回 'parentId'
        return 'parentId'
        
    # 设置一个默认的父ID键名
    guessed_id = 'parentId'
    try:
        # 以只读模式打开JSON文件，并指定UTF-8编码
        with open(json_file_path, 'r', encoding='utf-8') as f:
            # 加载JSON文件内容
            data = json.load(f)
            
        # 从JSON数据中获取 'api_name' 字段，如果不存在则返回空字符串
        api_name = data.get('api_name', "")
        # 检查 'api_name' 是否存在且以 '/' 开头
        if api_name and api_name.startswith('/'):
            # 移除 'api_name' 开头和结尾的 '/'，然后按 '/' 分割，并取第一个部分
            # 例如, "/biz-order/findList" -> "biz-order"
            name_part = api_name.strip('/').split('/')[0]
            
            # 按 '-' 分割字符串
            # 例如, "biz-order" -> ['biz', 'order']
            words = name_part.split('-')
            
            # 将分割后的单词列表转换为驼峰命名法
            # 例如, ['biz', 'order'] -> "bizOrder"
            camel_case_name = words[0] + "".join(word.capitalize() for word in words[1:])
            
            # 在驼峰命名的基础上拼接 "ParentId"
            # 例如, "bizOrder" -> "bizOrderParentId"
            guessed_id = f"{camel_case_name}ParentId"
                
    except Exception as e:
        # 如果在读取或解析JSON文件时发生异常，则打印错误信息
        print(f"  ⚠️ 读取/解析 {json_file_path} 失败: {e}")
        # 出现异常时，将使用默认的 'parentId'
    
    # 返回推测出的或默认的父ID键名
    return guessed_id

def renew():
    """
    清空 Neo4j 数据库中的所有数据和约束。
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) # 连接到Neo4j数据库
    with driver.session() as session: # 创建一个会话
        print("正在清空 Neo4j 数据库...") # 打印开始清空数据库的日志
        try:
            # 删除所有约束
            constraints = session.run("SHOW CONSTRAINTS") # 获取所有约束
            for record in constraints: # 遍历所有约束
                constraint_name = record["name"] # 获取约束名称
                session.run(f"DROP CONSTRAINT `{constraint_name}`") # 删除约束
            print("  ✅ 所有约束已删除。") # 打印约束删除成功的日志

            # 删除所有节点和关系
            session.run("MATCH (n) DETACH DELETE n") # 执行删除所有节点和关系的Cypher查询
            print("  ✅ 所有节点和关系已删除。") # 打印节点和关系删除成功的日志
            print("✅ Neo4j 数据库已清空。") # 打印数据库清空成功的日志
        except Exception as e: # 捕获异常
            print(f"❌ 清空数据库时出错: {e}") # 打印错误日志
    driver.close() # 关闭数据库连接


def rebuild_graph_database():
    """
    清空并完全重建 Neo4j 图数据库。
    """
    print("🚀 开始执行数据库重建任务...")
    
    # 1. 清空数据库
    renew()
    
    # 2. 获取访问令牌
    try:
        access_token = auth_service.get_access_token()
        print("  ✅ 成功获取 Access Token。")
    except Exception as e:
        print(f"  ❌ 获取 Access Token 失败: {e}")
        return # 如果没有令牌，则无法继续

    # 3. 导入所有节点数据
    print("\n--- 阶段 1: 导入节点数据 ---")
    readJSON(access_token)
    
    # 4. 创建父子关系
    print("\n--- 阶段 2: 创建父子关系 ---")
    create_parent()
    
    # 5. 创建其他所有关系
    print("\n--- 阶段 3: 创建其他业务关系 ---")
    if not os.path.exists(MCP_RELATION_PATH):
        print(f"  ⚠️ 关系配置文件未找到: {MCP_RELATION_PATH}，跳过此阶段。")
    else:
        try:
            with open(MCP_RELATION_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            relations = data.get("relations", [])
            if relations:
                for rel in relations:
                    get_link_data(access_token, rel)
            else:
                print("  🤷‍♂️ 未在配置文件中找到 'relations' 列表。")
        except Exception as e:
            print(f"  ❌ 读取或处理关系配置文件时出错: {e}")
            
    print("\n✅ 数据库重建任务完成！")


def create_parent():
    """
    读取 mcp_relation.json 文件中的 "parent_relations" 并创建父子关系
    """
    if not os.path.exists(MCP_RELATION_PATH): # 检查关系配置文件是否存在
        print(f"⚠️ 关系配置文件未找到: {MCP_RELATION_PATH}") # 如果文件不存在，则打印警告信息
        return # 结束函数执行

    print("开始创建父子关系...") # 打印任务开始的提示信息
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) # 初始化Neo4j数据库驱动

    try: # 使用try-except块来处理潜在的文件读取和JSON解析错误
        with open(MCP_RELATION_PATH, 'r', encoding='utf-8') as f: # 以只读模式打开JSON配置文件
            data = json.load(f) # 加载并解析JSON文件内容
        
        parent_relations = data.get("parent", []) # 从JSON数据中获取"parent_relations"列表，如果不存在则返回空列表
        
        if not parent_relations: # 检查父子关系列表是否为空
            print("  🤷‍♂️ JSON文件中没有找到'parent_relations'数据或列表为空。") # 如果列表为空，则打印提示信息
            return # 结束函数执行

        with driver.session() as session: # 创建一个数据库会话
            for rel_info in parent_relations: # 遍历每个父子关系定义
                child_clazz = rel_info.get("t") # 获取子节点的标签
                parent_clazz = rel_info.get("s") # 获取父节点的标签
                rel_type = "parent"# 获取关系类型

                if not child_clazz or not parent_clazz or not rel_type: # 检查关系定义是否完整
                    print(f"  ⚠️ 无效的父子关系定义，跳过: {rel_info}") # 如果定义不完整，则打印警告并跳过
                    continue # 继续下一个循环

                child_key = get_parent_key(child_clazz) # 定义子节点中指向父节点ID的属性名
                parent_key = get_key(parent_clazz) # 获取父节点的主键

                fetch_ids_query = f"MATCH (s:`{child_clazz}`) WHERE s.`{child_key}` IS NOT NULL RETURN elementId(s) AS id" # 构建查询以获取所有需要处理的子节点的ID
                result = session.run(fetch_ids_query) # 执行查询
                all_ids = [record["id"] for record in result] # 将查询结果转换为ID列表
                total = len(all_ids) # 获取需要处理的节点总数

                if total == 0: # 如果没有需要处理的节点
                    print(f"  ℹ️ 没有找到需要创建父子关系的节点: {child_clazz}") # 打印提示信息
                    continue # 继续下一个循环

                print(f"  🚀 开始处理: {child_clazz} -[{rel_type}]-> {parent_clazz} (总数: {total})") # 打印当前处理的关系和数量
                
                batch_size = 2000 # 设置每批处理的节点数量
                
                for i in range(0, total, batch_size): # 分批处理所有节点
                    batch_ids = all_ids[i : i + batch_size] # 获取当前批次的节点ID
                    
                    cypher = f"""
                    UNWIND $batch_ids AS sid
                    MATCH (s:`{child_clazz}`) WHERE elementId(s) = sid
                    MATCH (t:`{parent_clazz}`) WHERE t.`{parent_key}` = s.`{child_key}`
                    MERGE (s)-[:`{rel_type}`]->(t)
                    """ # 构建批量创建关系的Cypher查询
                    
                    try: # 使用try-except块处理数据库操作可能出现的错误
                        session.run(cypher, batch_ids=batch_ids) # 执行批量创建关系的操作
                        print(f"    -> 进度: {min(i + batch_size, total)} / {total}") # 打印处理进度
                    except Exception as e: # 捕获并处理异常
                        print(f"    ❌ 批次处理失败: {e}") # 打印批次处理失败的错误信息
                
                print(f"  ✅ 关系创建完成: {rel_type}") # 打印关系创建完成的提示

    except json.JSONDecodeError: # 捕获JSON解析错误
        print(f"  ❌ 无法解析JSON文件: {MCP_RELATION_PATH}") # 打印文件解析失败的错误信息
    except Exception as e: # 捕获其他所有异常
        print(f"  ❌ 处理父子关系时出错: {e}") # 打印通用错误信息
    finally: # 使用finally块确保数据库驱动被关闭
        if 'driver' in locals() and driver: # 检查driver是否已成功初始化
            driver.close() # 关闭数据库驱动连接



def create_relations(token):
    """
    读取 mcp_ralation.json 文件并创建 Neo4j 关系
    """
    if not os.path.exists(MCP_RELATION_PATH): # 检查JSON配置文件是否存在
        print(f"⚠️ 文件未找到: {MCP_RELATION_PATH}") # 如果不存在则打印警告
        return # 直接返回

    print("开始创建关系...") # 打印开始信息
    try: # 尝试读取和解析JSON文件
        with open(MCP_RELATION_PATH, 'r', encoding='utf-8') as f: # 以只读模式打开JSON文件
            data = json.load(f) # 解析JSON内容
        
        relations = data.get("link", []) # 从解析后的数据中获取"ralation"键对应的值，如果不存在则返回空列表
        
        if not relations: # 检查关系列表是否为空
            print("  🤷‍♂️ JSON文件中没有找到'ralation'数据或列表为空。") # 如果为空则打印提示
            return # 返回

        for relation_info in relations: # 遍历关系列表中的每个关系信息对象
            get_link_data(token, relation_info) # 调用get_link_data函数处理每个关系信息

    except json.JSONDecodeError: # 捕获JSON解析错误
        print(f"  ❌ 无法解析JSON文件: {MCP_RELATION_PATH}") # 打印JSON解析错误信息
    except Exception as e: # 捕获其他可能的异常
        print(f"  ❌ 处理关系文件时出错: {e}") # 打印通用错误信息
            
def clear_graph_database():
    """
    清空数据库数据
    警告：这将删除所有节点和关系！
    """
    print("⚠️ 正在清空 Neo4j 数据库...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        # 使用 DETACH DELETE 删除所有节点及其关系
        # 对于大数据量，建议分批删除，避免事务日志溢出
        
        # 简单粗暴版 (数据量小可用):
        # session.run("MATCH (n) DETACH DELETE n")
        
        # 稳健版 (分批删除):
        query = """
        CALL {
            MATCH (n)
            WITH n LIMIT 10000
            DETACH DELETE n
        } IN TRANSACTIONS OF 10000 ROWS
        """
        # 注意: CALL {} IN TRANSACTIONS 是 Neo4j 4.4+ 的语法
        # 如果版本较低，可以用简单的循环
        
        try:
            # 稳健版 (分批删除):
            # 使用 CALL {} IN TRANSACTIONS 分批提交，避免内存溢出
            query = """
            CALL () {
                MATCH (n)
                DETACH DELETE n
            } IN TRANSACTIONS OF 10000 ROWS
            """
            session.run(query)
            print("✅ 数据库已清空 (分批删除模式)")
        except Exception as e:
            print(f"  ❌ 分批清空失败: {e}")
            print("  -> 尝试回退到一次性删除...")
            try:
                session.run("MATCH (n) DETACH DELETE n")
                print("✅ 数据库已清空 (一次性删除模式)")
            except Exception as e2:
                print(f"  ❌ 一次性删除也失败: {e2}")
            
    driver.close()



def select_path(clazz_list):
    """
    接收一个节点标签数组，按顺序查询相邻两个标签之间的所有路径
    :param clazz_list: 节点标签列表，如 ['A', 'B', 'C']
    :return: 按顺序返回每段路径的详细信息列表
    """
    if not clazz_list or len(clazz_list) < 2: # 校验输入是否有效
        return []

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) # 创建 Neo4j 驱动连接
    full_results = [] # 存储所有片段的结果
    
    try: # 使用 try-finally 确保资源释放
        with driver.session() as session: # 创建数据库会话
            # 遍历标签数组，处理每一对相邻的标签
            for i in range(len(clazz_list) - 1):
                start_clazz = clazz_list[i] # 当前片段起点
                end_clazz = clazz_list[i+1] # 当前片段终点
                
                # 构建 Cypher 查询，查找 1-5 跳的路径（无向查询，忽略箭头方向）
                # 使用 -[...]-( 而不是 -[...]-> 确保能找到反向或混合方向的关联
                cypher = f"""
                MATCH p = (a:`{start_clazz}`)-[*1..5]-(b:`{end_clazz}`) 
                WITH p, [rel IN relationships(p) | type(rel)] AS path_signature 
                RETURN 
                    path_signature, 
                    collect(p) AS paths, 
                    count(p) AS number_of_paths
                """
                
                print(f"执行路径聚合查询: {start_clazz} -> {end_clazz}") # 打印日志
                result = session.run(cypher) # 执行 Cypher 查询
                
                segment_data = { # 当前片段的数据容器
                    "segment_index": i, # 片段序号
                    "start_clazz": start_clazz, # 起点标签
                    "end_clazz": end_clazz, # 终点标签
                    "connections": [] # 存储该片段的所有连接模式
                }
                
                for record in result: # 遍历查询结果的每一行
                    item = { # 构建结果项字典
                        "signature": record["path_signature"], # 获取路径签名（关系类型列表）
                        "count": record["number_of_paths"], # 获取该签名下的路径总数
                        "paths": [] # 初始化该签名下的路径详情列表
                    }
                    
                    # 遍历该分组下的所有路径对象
                    for path_obj in record["paths"]: 
                        # 调用 serialize_path 函数序列化路径（该函数需在作用域内可用）
                        item["paths"].append(serialize_path(path_obj)) 
                    
                    segment_data["connections"].append(item) # 将构建好的项加入片段连接列表
                
                full_results.append(segment_data) # 将当前片段数据加入总结果
                
            return full_results # 返回所有片段的聚合数据
            
    finally: # 无论是否发生异常
        driver.close() # 关闭数据库驱动连接




# 1. 辅助函数，将 neo4j driver 返回的结果转换为通用的图JSON格式。
def _format_records_to_graph_json(records):
    """
    将 neo4j driver 返回的 records 转换成通用的图JSON格式 (nodes/links)。
    这个格式对于前端可视化或进一步处理非常友好。
    """
    nodes = {}
    links = {}

    # 遍历查询返回的每一行记录
    for record in records:
        node_a = record['nodeA']
        node_b = record['nodeB']
        rel = record['r']

        # 如果节点还未被记录，则处理并添加到 nodes 字典中
        if node_a.element_id not in nodes:
            nodes[node_a.element_id] = {
                "id": node_a.element_id,
                "labels": list(node_a.labels),
                "properties": dict(node_a)
            }
        
        if node_b.element_id not in nodes:
            nodes[node_b.element_id] = {
                "id": node_b.element_id,
                "labels": list(node_b.labels),
                "properties": dict(node_b)
            }

        # 如果关系还未被记录，则处理并添加到 links 字典中
        if rel.element_id not in links:
            links[rel.element_id] = {
                "id": rel.element_id,
                "source": rel.start_node.element_id,
                "target": rel.end_node.element_id,
                "type": rel.type,
                "properties": dict(rel)
            }
            
    return {"nodes": list(nodes.values()), "links": list(links.values())}


# 2. 更新后的主函数，增加了 max_hops 参数并应用了路径长度限制
def useGDS(node_labels: list, max_hops: int = 8):
    """
    使用纯 Cypher 查询，找到连接一组给定标签的节点的最经济路径的近似解。
    :param node_labels: 一个包含节点标签字符串的列表。
    :param max_hops: 查找路径的最大深度（跳数），防止查询时间过长。
    :return: 包含节点和关系列表的字典，格式化为可用的JSON结构。
    """
    # 动态构建 MATCH 和 WITH 子句
    match_clauses = []
    with_clauses = []
    node_vars = []
    for i, label in enumerate(node_labels):
        node_var = f"n{i+1}"
        node_vars.append(node_var)
        
        match_clause = f"MATCH ({node_var}:{label})"
        with_vars = ", ".join(node_vars)
        with_clause = f"WITH {with_vars} LIMIT 1"
        
        match_clauses.append(match_clause)
        with_clauses.append(with_clause)

    sample_nodes_query_part = "\n".join(f"{m}\n{w}" for m, w in zip(match_clauses, with_clauses))

    # 构建完整的纯 Cypher 查询字符串（已应用路径长度限制）
    pure_cypher_query = f"""
    // 动态选择每种标签的一个样本节点
    {sample_nodes_query_part}

    // 将这些样本节点放入一个列表中
    WITH [{', '.join(node_vars)}] AS nodes_to_connect

    // 展开节点列表，生成所有唯一的节点对 (n1, n2)
    UNWIND nodes_to_connect AS n1
    UNWIND nodes_to_connect AS n2
    WITH * WHERE elementId(n1) < elementId(n2)

    // 对每一对节点，找到它们之间的所有最短路径（带有长度限制）
    // 使用 [*..{max_hops}] 来限制路径搜索深度，避免性能问题
    MATCH path = allShortestPaths((n1)-[*..{max_hops}]-(n2))

    // 将所有找到的路径“打散”，提取出其中所有的关系
    UNWIND relationships(path) AS r

    // 返回去重后的关系，以及关系的两端节点
    WITH DISTINCT r
    RETURN startNode(r) AS nodeA, r, endNode(r) AS nodeB
    """
    print(pure_cypher_query)
    # 执行查询并处理结果
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
        with driver.session() as session:
            result = session.run(pure_cypher_query)
            # 直接将 result 对象传递给辅助函数进行迭代处理
            return _format_records_to_graph_json(result)
    except Exception as e:
        print(f"执行纯 Cypher 查询时发生错误: {e}")
        return None

def  rebuild_graph_database():
    token  = auth_service.auth_login()
    #print(token)
    #readJSON(token)
    # 创建关系
    create_relations(token)
    #create_parent()    

def check_ids(api_data, target_key, target_value): # 定义一个函数，接收一个数据列表、一个目标键和一个目标值
    # 使用列表推导式高效地筛选出符合条件的元素
    return [ # 返回一个列表
        item for item in api_data # 遍历api_data中的每一个项目
        if isinstance(item, dict) and item.get(target_key) == target_value # 检查项目是否为字典，并且其指定键的值是否等于目标值
    ]

if __name__ == '__main__':
    #renameJSON()
    #clear_graph_database()
    rebuild_graph_database() 
  
    """
    relation_info =  {
            "s": "BUSINESS_ORDER_DETAIL",
            "t": "PRD_O_APY_DET"
    }
    token  = auth_service.auth_login()
    data = get_link_data(token, relation_info)
    print(len(data))
    print(check_ids(data,"linkSource","0247a5063cdd436c9fff5013975096dc"))
    """

   
