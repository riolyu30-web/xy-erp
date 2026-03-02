import os
import sys

# 将项目根目录添加到 sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
from fastmcp import FastMCP  # 导入FastMCP框架
import json  # 导入JSON库
import random # 导入random库 用于生成随机数
import string # 导入string库 用于处理字符串
from datetime import datetime, timedelta # 导入datetime库 用于处理日期和时间
from services.llm_manager import dashscope_chat_json
from neo4j import GraphDatabase

neo4j_mcp = FastMCP(name="neo4j")  # 创建计算服务MCP实例

from dotenv import load_dotenv # 导入 dotenv 库
load_dotenv() # 加载根目录下的 .env 文件

# 预定义的物料列表
MATERIAL_LIST = [
    "300克玖龙粉灰卡787*1092", "250克玖龙粉灰卡889*1194", "金枫300克粉灰卡FSC787*1092",
    "理文170克白牛咭787*1092", "金枫300克粉灰卡889*1194", "海龙250克粉灰卡889*1194",
    "2075水性光油", "PMS Warm Grey 1U（水墨）", "PMS 2757U( BLUE )（水墨）",
    "PMS 072U（水墨）", "东洋四色 红", "100037824包装箱344*328*182",
    "100037821包装箱516*368*351", "300534749包装箱天盖982*523*97", "3882-03 右保护卡包装箱551*348*330"
]

# 预定义的姓氏和名字列表
SURNAMES = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨"]
GIVEN_NAMES = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟"]

# 预定义的产品名称列表
PRODUCT_NAMES = [
    "TM-FY2526 SK-II Vday Dressup M礼盒", "JD-FY2526 SK-II Vday Dressup M礼盒", 
    "JD POP-FY2526 SK-II Vday Dressup M礼盒", "VIP-FY2526 SK-II Vday Dressup M礼盒", 
    "DY-FY2526 SK-II Vday Dressup M礼盒", "DS-FY2526 SK-II Vday Dressup M礼盒(DS)", 
    "Zurich Heart Rate monitor心率仪外盒", "Zurich Heart Rate monitor心率仪内卡", 
    "Zurich Heart Rate monitor心率仪使用指南", "Zurich Heart Rate monitor心率仪内盒", 
    "Zurich Heart Rate monitor心率仪说明书", "爱唯110ml玫瑰花瓣精华液(升级版） 专用E坑内托", 
    "爱唯110ml玫瑰花瓣精华液(升级版） 专用E坑内托", "JESS名后 110ml玫瑰花瓣精华液（2026新版）专用彩盒", 
    "JESS名后 110ml玫瑰花瓣精华液（2026新版）专用彩盒", "FSC13026337 HCG卡1T包装盒(135x70x25mm)350g单铜过光胶屈臣氏PHFV03", 
    "FSC13026338 HCG条1包装盒(125x60x21mm)350g单铜过光胶屈臣氏MYFV06", "FSC13026339 HCG卡1T包装盒(135x70x25mm)350g单铜过光胶屈臣氏MYFV06", 
    "FSC13026340 HCG笔1T包装盒(195x55x23mm)350g单铜过光胶屈臣氏MYFV06", "2026年新年贺卡（三福）（V1.0）", 
    "26年新年贺卡（V1.0）-渠道通用", "26年新年贺卡（V1.0）-WOW COLOUR", 
    "2026京东新年礼盒贺卡（V1.0）", "Core Coeur Iconique 14pcs Lid 2025 心型盒盖", 
    "2025 14pcs heart box-Base 心形盒底", "5 ply heart shape candy pad 威化纸", 
    "25 3x8 BASE 地盒", "GTR 8PCS Candy Pad 25 威化纸", 
    "LID - GOLD 2025 8PCS Asia 金色天盖", "LID - ALL DARK CHOCOLATE 2025 8PCS Asia 黑巧克力天盖", 
    "LID - ALL MILK CHOCOLATE 2020 8PCS Asia 牛奶巧克力天盖", "Gold 2025 15pcs Candy Pad-威化纸", 
    "FSC13026336 HCG笔1T包装盒(195x55x23mm)350g单铜过光胶屈臣氏PHFV03", "FSC13026328 HCG笔1T包装盒(195x55x23mm)350g单铜过光胶屈臣氏THFV07", 
    "FSC13026327 HCG卡1T包装盒(135x70x25mm)350g单铜过光胶屈臣氏THFV07", "FSC13026335 LH笔5T包装盒(195x60x60mm)350g单铜过光胶屈臣氏PHFV03", 
    "睡前舒缓型儿童护眼贴10片包装盒(新版)", "成人护眼贴润目舒缓型纸盒（10片装）", 
    "时代萱妍赋活舒缓精华霜50g-彩盒", "时代萱妍赋活舒缓精华霜50g-内托", 
    "植物医生 100ml青蒿舒缓祛痘调理乳（调整版）专用彩盒", "植物医生100ML青蒿舒缓祛痘调理乳专用E坑内托", 
    "植物医生120ml青蒿舒缓祛痘调理水专用彩盒", "植物医生120ml青蒿舒缓祛痘调理水专用E坑内托", 
    "植物医生120g青蒿净澈清肌洁面乳专用彩盒", "DR PLANT雪莲水感透亮凝露120ml-彩盒(一物一码)(2025B)", 
    "DR PLANT雪莲水感透亮精华乳100ml-彩盒(一物一码)(2025B)", "DR PLANT雪莲水感透亮精华液40ml-彩盒(一物一码)(2025B)", 
    "DR PLANT雪莲水感透亮精华霜50g-彩盒(一物一码)(2025B)", "DR PLANT 紫灵芝多效驻颜提拉面膜20ml+20ml-彩盒（2024B)", 
    "DR PLANT 紫灵芝多效驻颜提拉面膜20ml+20ml-内卡"
]

def generate_random_product_name():
    """从预定义的列表中随机选择一个产品名称"""
    return random.choice(PRODUCT_NAMES)

def generate_random_string(length=8):
    """生成指定长度的随机字符串（大写字母和数字）"""
    # 定义字符集为大写字母和数字
    letters_and_digits = string.ascii_uppercase + string.digits
    # 从字符集中随机选择指定长度的字符并拼接成字符串
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def generate_random_name():
    """随机生成一个中文姓名"""
    # 从预定义的姓氏列表中随机选择一个姓氏
    surname = random.choice(SURNAMES)
    # 从预定义的名字列表中随机选择1到2个字作为名字
    given_name = "".join(random.choices(GIVEN_NAMES, k=random.randint(1, 2)))
    # 拼接姓和名，返回完整的姓名
    return f"{surname}{given_name}"

def generate_random_number(digits: int):
    """生成指定位数的随机数字字符串，确保多位数时不以0开头"""
    # 检查位数是否为正数
    if digits <= 0:
        # 如果位数不合法，则返回空字符串
        return ""
    
    # 如果只有一位，可以为0
    if digits == 1:
        # 从 '0' 到 '9' 中随机选择一个数字
        return random.choice(string.digits)

    # 对于多位数，第一位从 '1' 到 '9' 中随机选择
    first_digit = random.choice('123456789')
    # 剩下的位数从 '0' 到 '9' 中随机选择
    remaining_digits = "".join(random.choices(string.digits, k=digits - 1))
    
    # 拼接第一位和剩下的数字，并返回结果
    return f"{first_digit}{remaining_digits}"

def generate_random_material():
    """从预定义的列表中随机选择一个物料"""
    # 从全局物料列表中随机选择一个元素并返回
    return random.choice(MATERIAL_LIST)


def generate_random_company_name():
    """随机生成一个公司名称，格式如 'X**公司' 或 'Y**厂'"""
    # 定义公司名称后缀列表
    suffixes = ["公司", "厂", "集团", "实业", "科技"]
    # 从 GIVEN_NAMES 列表中随机选择一个字作为公司名前缀
    prefix = random.choice(GIVEN_NAMES)
    # 从后缀列表中随机选择一个后缀
    suffix = random.choice(suffixes)
    # 按照 "前缀**后缀" 的格式拼接并返回公司名
    return f"{prefix}**{suffix}"


def generate_sequential_code(prefix: str, length: int = 3):
    """
    生成带固定前缀和随机序列号的编码
    :param prefix: 编码前缀 (e.g., "XY")
    :param length: 数字部分的长度
    """
    # 生成指定长度的随机数字字符串
    random_number = ''.join(random.choices(string.digits, k=length))
    
    # 拼接前缀和随机数字，返回最终的编码
    return f"{prefix}10000{random_number}"


def generate_random_datetime(start_date_str=None, end_date_str=None):
    """
    在指定时间范围内生成一个随机的日期和时间
    :param start_date_str: 开始日期字符串 (e.g., "2026-01-01 00:00:00")
    :param end_date_str: 结束日期字符串 (e.g., "2026-12-31 23:59:59")
    :return: 格式化后的随机日期时间字符串
    """
    # 定义日期时间格式
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 如果未提供开始日期，则默认为2026年的第一天
    if start_date_str is None:
        start_date = datetime(2026, 1, 1)
    else:
        # 将开始日期字符串解析为datetime对象
        start_date = datetime.strptime(start_date_str, date_format)
        
    # 如果未提供结束日期，则默认为2026年的最后一天
    if end_date_str is None:
        end_date = datetime(2026, 12, 31, 23, 59, 59)
    else:
        # 将结束日期字符串解析为datetime对象
        end_date = datetime.strptime(end_date_str, date_format)
    
    # 计算时间范围的总秒数
    time_delta = end_date - start_date
    total_seconds = int(time_delta.total_seconds())
    
    # 生成一个随机的秒数
    random_seconds = random.randint(0, total_seconds)
    
    # 计算随机的日期时间
    random_date = start_date + timedelta(seconds=random_seconds)
    
    # 将随机日期时间格式化为指定的字符串格式并返回
    return random_date.strftime(date_format)


# Neo4j 配置 (请根据你的实际情况修改)
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")  # 替换为你刚才设置的密码
# 定义全局路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATAWORK_DIR = os.path.join(BASE_DIR, "datawork")
MCP_RELATION_PATH = os.path.join(BASE_DIR, "mcp_relation.json")

def load_datawork_meta():
    """加载datawork目录下的元数据，返回属性映射和表名映射"""
    attr_map = {}
    table_map = {}
    # 遍历datawork目录
    for root, dirs, files in os.walk(DATAWORK_DIR):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        main_tab = data.get('mainTabClazz')
                        table_name = data.get('table_name', main_tab)
                        
                        if main_tab:
                            table_map[main_tab] = table_name
                            
                            # 映射属性名到mainTabClazz
                            resp = data.get('response', {})
                            for attr in resp.keys():
                                attr_map[attr] = main_tab
                except Exception:
                    continue
    return attr_map, table_map

def load_relations():
    """加载mcp_relation.json中的所有关系，构建有向图和邻接表"""
    adj = {} # 邻接表，用于BFS遍历（无向，方便找到连通性）
    directed_edges = set() # 存储有向边集合 (u, v)
    
    if os.path.exists(MCP_RELATION_PATH):
        try:
            with open(MCP_RELATION_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 遍历所有类型的关系
                for rel_type, rels in data.items():
                    for r in rels:
                        s = r.get('s')
                        t = r.get('t')
                        if s and t:
                            # 记录有向边
                            directed_edges.add((s, t))
                            
                            # 构建无向图用于搜索
                            if s not in adj: adj[s] = []
                            if t not in adj: adj[t] = []
                            if t not in adj[s]: adj[s].append(t)
                            if s not in adj[t]: adj[t].append(s)
        except Exception:
            pass
    return adj, directed_edges

def find_relation_path_logic(attributes: list[str]) -> dict:
    """
    根据输入的属性名数组，查找对应表之间的关系路径
    输入：属性名数组
    输出：路径编码-中文简述 字典
    """
    # 1. 加载元数据
    attr_map, table_map = load_datawork_meta()
    
    # 2. 找到属性名对应的 mainTabClazz
    tables = []
    for attr in attributes:
        if attr in attr_map:
            tables.append(attr_map[attr])
            
    # 去重并保持顺序
    seen = set()
    unique_tables = []
    for t in tables:
        if t not in seen:
            unique_tables.append(t)
            seen.add(t)
            
    print(unique_tables)

    # 如果找不到足够的表，返回提示
    if len(unique_tables) < 0:
        return {"error": "Need at least two distinct tables identified from attributes.", "identified_tables": unique_tables}
    if len(unique_tables) == 1:
        return {"message": unique_tables[0]}
        
    # 3. 加载关系数据
    adj, directed_edges = load_relations()
    
    # 4. 查找所有节点对之间的路径
    from itertools import combinations
    
    result = {}
    limit = 5
    max_depth = 12 # 防止过深
    
    # 对每对节点进行路径查找
    for start_node, end_node in combinations(unique_tables, 2):
        queue = [[start_node]]
        found_paths = []
        iterations = 0
        MAX_ITERATIONS = 50000
        
        while queue and len(found_paths) < limit and iterations < MAX_ITERATIONS:
            iterations += 1
            path = queue.pop(0)
            node = path[-1]
            
            if node == end_node:
                # 检查路径方向一致性
                is_valid_direction = True
                if len(path) > 1:
                    # 检查是否全部是正向 (A->B->C)
                    all_forward = True
                    for i in range(len(path) - 1):
                        if (path[i], path[i+1]) not in directed_edges:
                            all_forward = False
                            break
                    
                    # 检查是否全部是反向 (A<-B<-C)
                    all_backward = True
                    for i in range(len(path) - 1):
                        if (path[i+1], path[i]) not in directed_edges:
                            all_backward = False
                            break
                            
                    # 只有全正向或全反向才算方向一致
                    if not all_forward and not all_backward:
                        is_valid_direction = False
                
                if is_valid_direction:
                    # 仅保留经过全部unique_tables的节点的路径
                    if all(t in path for t in unique_tables):
                        found_paths.append(path)
                continue
                
            if len(path) >= max_depth:
                continue
                
            if node in adj:
                for neighbor in adj[node]:
                    if neighbor not in path:
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)
                        
        # 格式化当前对的路径
        for path in found_paths:
            # 生成路径编码
            path_code = "-".join(path)
            # 生成中文简述
            path_desc = "-".join([table_map.get(n, n) for n in path])
            result[path_code] = path_desc
    print(result)       
    if not result:
        return {"error": f"No path found between identified tables: {unique_tables}"}
    
    system_prompt= """
    你是ERP数据分析专家，擅长分析数据结构，选择最优路径找到答案
    用户会提供路径集合，请按常规业务逻辑分析并推荐最优路径 返回最佳路径编号
    输出格式为JSON:
    { "best":"XXXXX-XXX-XXX"}   
    """

    data = dashscope_chat_json(system_prompt, json.dumps(result, ensure_ascii=False, indent=4))
    if data and "best" in data:
        print(data["best"])
        return {"message": data["best"]}
    else:
        return {"error": "None"}

def select(start_clazz:str,end_clazz:str):
    """
    查询 Neo4j 数据库中的关系
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:        
        # 定义一个f-string格式的Cypher查询字符串
        for i in range(1,5):
            query = f"""
            MATCH  (a:`{start_clazz}`),(b:`{end_clazz}`)
            MATCH p = (a)-[*{i}]-(b)
            RETURN p
            """
            print(query)
            result = session.run(query) # 执行Cypher查询
            paths_data = [] # 创建一个空列表，用于存储所有序列化后的路径数据
            # 迭代处理查询返回的每一条记录
            for record in result:
                # 调用辅助函数序列化路径并添加到列表中
                paths_data.append(serialize_path(record['p']))
            # 检查列表是否包含数据
            if paths_data:
                print(json.dumps(paths_data[0], indent=2, ensure_ascii=False))
                return paths_data
        return None

def select_one(clazz:str):
    """
    根据clazz查询单个节点，只返回一个结果
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        query = f"MATCH (n:`{clazz}`) RETURN n"
        print(query)
        result = session.run(query)
        # 获取所有结果
        records = list(result)
        
        if records:
            formatted_results = []
            for record in records:
                node = record['n']
                # 每个节点都包装成统一的格式
                formatted_results.append({
                    "nodes": [{
                        "id": node.element_id,
                        "labels": list(node.labels),
                        "properties": dict(node)
                    }],
                    "relationships": []
                })
            return formatted_results
        return None


def select_list(clazz_list: list[str]):
    """
    输入list<str> 生产 按顺序的节点 查询语句
    """
    if not clazz_list or len(clazz_list) == 1:
        return select_one(clazz_list[0])

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        # 动态构建链式查询语句
        # 假设 clazz_list = ['A', 'B', 'C']
        # 目标: MATCH p = (n0:`A`)-[*1..4]-(n1:`B`)-[*1..4]-(n2:`C`) RETURN p
        
        parts = []
        for i, clazz in enumerate(clazz_list):
            parts.append(f"(n{i}:`{clazz}`)")
            
        # 使用 -[*1..4]- 连接各个节点，参考 select 方法中的 range(1,5)
        pattern = "-[*1..4]-".join(parts)
        
        query = f"""
        MATCH p = {pattern}
        RETURN p
        """
        print(query)
        result = session.run(query)
        paths_data = []
        
        for record in result:
            paths_data.append(serialize_path(record['p']))
            
        if paths_data:
            #print(json.dumps(paths_data[0], indent=2, ensure_ascii=False))
            return paths_data
            
        return None


# 定义一个辅助函数，用于将Neo4j的Path对象序列化为字典
def serialize_path(path):
            # 初始化一个包含节点和关系列表的字典
            serialized = {"nodes": [], "relationships": []}
            # 遍历路径中的所有节点
            for node in path.nodes:
                # 将节点ID、标签和所有属性添加进节点列表
                serialized["nodes"].append({
                    "id": node.element_id, # 获取节点的唯一ID
                    "labels": list(node.labels), # 获取节点的所有标签
                    "properties": dict(node) # 获取节点的所有属性
                })
            # 遍历路径中的所有关系
            for rel in path.relationships:
                # 将关系ID、类型、起始节点ID、结束节点ID和所有属性添加进关系列表
                serialized["relationships"].append({
                    "id": rel.element_id, # 获取关系的唯一ID
                    "type": rel.type, # 获取关系的类型
                    "start_node_id": rel.start_node.element_id, # 获取起始节点的ID
                    "end_node_id": rel.end_node.element_id, # 获取结束节点的ID
                    "properties": dict(rel) # 获取关系的所有属性
                })
            # 返回序列化后的字典
            return serialized

def find_data_by_path(path: str):
        """
        查询 Neo4j 数据库中的关系
        """
        node_list = path.split("-")
       
        current_node_list = list(node_list)
        full_results = None
        if len(current_node_list) ==1 :
            full_results = select_one(path)
        else:           
            while len(current_node_list) >= 2:
                print(f"尝试查询路径: {current_node_list}")
                full_results = select_list(current_node_list)
                if full_results:
                    break
                print("未找到数据，尝试减少一个节点继续查找...")
                current_node_list.pop()
                       
        if full_results:
            merged_results = [] 
            for path in full_results:
                merged_props = {}
                # path 是一个字典，包含 'nodes' 和 'relationships'
                for node in path.get('nodes', []):
                    # 合并节点属性，后出现的节点属性会覆盖前面的（如果有重复key）
                    if 'properties' in node:
                        merged_props.update(node['properties'])
                merged_results.append(merged_props)
            return {"message": merged_results}            
        return {"error": "未找到数据"}            


# 定义一个更新节点属性的函数
def update_node_properties(clazz: str, match_properties: dict, update_properties: dict):
    """
    根据匹配条件更新节点属性
    :param clazz: 节点标签 (e.g., "BUSINESS_ORDER_DETAIL")
    :param match_properties: 用于查找节点的属性字典 (e.g., {"bizOrderNo": "SO202311280001"})
    :param update_properties: 要更新的属性字典 (e.g., {"bizOrderDetailAuditStatus": "AUDITED"})
    """
    # 检查匹配属性字典是否为空
    if not match_properties:
        # 如果为空，则返回错误信息，因为无法定位要更新的节点
        return {"error": "match_properties cannot be empty."}

    # 使用配置的URI、用户名和密码创建Neo4j数据库驱动实例
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    # 创建一个数据库会话，使用'with'确保会话在使用后自动关闭
    with driver.session() as session:
        # 为每个匹配属性生成一个Cypher WHERE子句部分
        where_clauses = [f"n.{key} = ${key}" for key in match_properties.keys()]
        # 将所有WHERE子句用'AND'连接成一个完整的WHERE条件字符串
        where_statement = " AND ".join(where_clauses)

        # 使用f-string构建完整的Cypher查询语句
        query = f"""
        MATCH (n:`{clazz}`)
        WHERE {where_statement}
        SET n += $update_props
        RETURN n
        """
        
        # 将匹配属性和更新属性解包合并到一个新的字典中，作为查询参数
        parameters = {**match_properties, "update_props": update_properties}
        
        # 在控制台打印将要执行的Cypher查询语句，便于调试
        print(f"Executing query: {query}")


# 根据时间范围查找节点的函数
def find_nodes_by_time_range(clazz: str, attribute: str, start_time: str, end_time: str) -> list:
    """
    根据时间范围查找节点
    :param clazz: 节点标签
    :param attribute: 用于时间范围过滤的属性名
    :param start_time: 开始时间 (e.g., "2026-01-01 00:00:00")
    :param end_time: 结束时间 (e.g., "2026-12-31 23:59:59")
    """
    # 使用配置的URI、用户名和密码创建Neo4j数据库驱动实例
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    # 创建一个数据库会话，使用'with'确保会话在使用后自动关闭
    with driver.session() as session:
        # 如果开始时间或结束时间为空，则不进行时间过滤
        if not start_time or not end_time:
            query = f"""
            MATCH (n:`{clazz}`)
            RETURN n
            LIMIT 300
            """
            parameters = {}
        else:
            # 构建Cypher查询语句，用于匹配指定标签的节点，并根据时间属性进行过滤
            query = f"""
                MATCH (n:`{clazz}`) 
                WHERE n.{attribute} >= "{start_time}" AND n.{attribute} <= "{end_time}" 
                RETURN n
                """
            # 定义查询参数，防止Cypher注入
            parameters = {"start_time": start_time, "end_time": end_time}
        
        # 在控制台打印将要执行的Cypher查询语句和参数，便于调试
        print(f"Executing query: {query} with parameters: {parameters}")
        # 执行查询
        result = session.run(query, parameters)
        
        # 将结果转换为列表
        records = list(result)
        
        # 如果查询到记录
        if records:
            # 创建一个空列表，用于存放格式化后的结果
            formatted_results = []
            # 遍历每一条记录
            for record in records:
                # 获取记录中的节点对象
                node = record['n']
                # 将节点的属性字典添加到结果列表中
                formatted_results.append(dict(node))
            # 返回包含结果列表的消息字典
            return formatted_results
        # 如果没有找到数据，返回一个包含空列表的消息字典
        return []
        # 在控制台打印传递给查询的参数，便于调试
        print(f"With parameters: {parameters}")

        # 执行带参数的Cypher查询
        result = session.run(query, parameters)
        # 从查询结果中提取所有被更新的节点记录
        updated_nodes = [record['n'] for record in result]

        # 检查是否有节点被更新
        if updated_nodes:
            # 如果有，返回一个包含成功消息和更新后节点数据的字典
            return {"success": f"Updated {len(updated_nodes)} nodes.", "updated_nodes": [dict(node) for node in updated_nodes]}
        # 如果没有节点被更新
        else:
            # 返回一个表示没有找到匹配节点的消息
            return {"message": "No nodes found matching the criteria."}


def testcase1():
    result = find_relation_path_logic(["bizOrderDetailAuditStatus", "contractDetailBriefName","prdRetDetBusDivisId"])
    print(json.dumps(result, ensure_ascii=False, indent=4))


def testcase2():
    result = {
    "CONTRACT_DETAIL-ORDER_NOTICE_DET-BUSINESS_ORDER_DETAIL-PRD_O_APY_DET-PRD_SAL_DET-PRD_RET_DET": "合同明细-订单通知单明细-业务订单明细-成品出库申请明细-成品 销货明细表-成品退货明细表",        
    "CONTRACT_DETAIL-BUSINESS_ORDER_DETAIL-PRD_O_APY_DET-TRANS_PLAN_DET-PRD_SAL_DET-PRD_RET_DET": "合同明细-业务订单明细-成品出库申请明细-厂车运输计划明细-成品 销货明细表-成品退货明细表",        
    "CONTRACT_DETAIL-BUSINESS_ORDER_DETAIL-PRD_O_APY_DET-PRD_SAL_DET-PRD_RET_DET": "合同明细-业务订单明细-成品出库申请明细-成品销货明细表-成品退货明细表",      
    "CONTRACT_DETAIL-BUSINESS_ORDER_DETAIL_CO-BUSINESS_ORDER_DETAIL-PRD_O_APY_DET-PRD_SAL_DET-PRD_RET_DET": "合同明细-BUSINESS_ORDER_DETAIL_CO-业务订单明细-成品出库申请明细-成品销货明细表-成品退货明细表",
    "CONTRACT_DETAIL-BUSINESS_ORDER_DETAIL_CO-BUSINESS_ORDER_DETAIL-PRD_O_APY_DET-TRANS_PLAN_DET-PRD_SAL_DET-PRD_RET_DET": "合同明细-BUSINESS_ORDER_DETAIL_CO-业务订单明细-成品出库申请明细-厂车运输计划明细-成品销货明细表-成品退货明细表"     
    }
    system_prompt= """
    你是ERP数据分析专家，擅长分析数据结构，选择最优路径找到答案
    用户会提供路径集合，请按常规业务逻辑分析并推荐最优路径，返回最佳路径编号
    输出格式为JSON:
    { "best":"XXXXX-XXX-XXX"}   
    """
    data = dashscope_chat_json(system_prompt, json.dumps(result, ensure_ascii=False, indent=4))
    if data and "best" in data:
        print(data["best"])
        node_list = data["best"].split("-")
        #node_list =["CONTRACT_DETAIL","BUSINESS_ORDER_DETAIL","PRD_O_APY_DET"]
        
        current_node_list = list(node_list)
        full_results = None
        
        while len(current_node_list) >= 2:
            print(f"尝试查询路径: {current_node_list}")
            full_results = select_list(current_node_list)
            if full_results:
                break
            print("未找到数据，尝试减少一个节点继续查找...")
            current_node_list.pop()
            
        if full_results:
            merged_results = []
            for path in full_results:
                merged_props = {}
                # path 是一个字典，包含 'nodes' 和 'relationships'
                for node in path.get('nodes', []):
                    # 合并节点属性，后出现的节点属性会覆盖前面的（如果有重复key）
                    if 'properties' in node:
                        merged_props.update(node['properties'])
                merged_results.append(merged_props)
            
            print(f"找到 {len(merged_results)} 条路径，合并属性如下：")
            for i, props in enumerate(merged_results):
                print(f"--- 路径 {i+1} 合并属性 ---")
                #print(json.dumps(props, ensure_ascii=False, indent=4))


def testcase3():
    result = select_one("BUSINESS_ORDER_DETAIL")
    print(json.dumps(result, ensure_ascii=False, indent=4))


def testcase4():
    """
    测试更新节点属性的功能
    """
    # 定义要匹配的节点标签
    clazz = "MAT_ARR_DET"
    # 定义用于定位节点的属性条件
    match_props = {"matArrDetMatArrSettlementSupplierId": "8a36a61f7b474051a4eda710460c2303"}
    # 定义需要更新的属性及其新值
    update_props = {"matArrDetActMaterialId": "AUDITED"}
    # 调用更新函数
    result = update_node_properties(clazz, match_props, update_props)
    # 打印更新结果，使用JSON格式化输出，确保中文字符正常显示
    print(json.dumps(result, ensure_ascii=False, indent=4))


def update_node_with_random_value_by_property(clazz: str, property_name: str, random_type: str, **kwargs):
    """
    根据节点标签和属性名查找节点，并为该属性赋予指定的随机类型值
    :param clazz: 节点标签
    :param property_name: 需要更新的属性名
    :param random_type: 随机值类型 (e.g., "string", "name", "number", "material", "company_name", "sequential_code")
    :param kwargs: 传递给随机值生成函数的可选参数 (e.g., length=10, prefix="AB")
    """
    # 使用配置的URI、用户名和密码创建Neo4j数据库驱动实例
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    # 创建一个数据库会话，使用'with'确保会话在使用后自动关闭
    with driver.session() as session:
        # 构建Cypher查询，查找所有具有指定标签的节点
        query_find = f"MATCH (n:`{clazz}`) RETURN n"
        # 执行查找查询
        nodes_to_update = session.run(query_find)
        
        # 初始化一个列表，用于存储更新后的节点数据
        updated_nodes_data = []
        # 遍历查询结果中的每个节点
        for record in nodes_to_update:
            # 获取节点对象
            node = record['n']
            
            # 根据 random_type 选择不同的随机值生成方法
            new_value = None
            if random_type == "string":
                # 如果随机类型是 "string"，调用 generate_random_string 函数
                new_value = generate_random_string(**kwargs)
            elif random_type == "name":
                # 如果随机类型是 "name"，调用 generate_random_name 函数
                new_value = generate_random_name()
            elif random_type == "number":
                # 如果随机类型是 "number"，调用 generate_random_number 函数
                new_value = generate_random_number(**kwargs)
            elif random_type == "material":
                # 如果随机类型是 "material"，调用 generate_random_material 函数
                new_value = generate_random_material()
            elif random_type == "company_name":
                # 如果随机类型是 "company_name"，调用 generate_random_company_name 函数
                new_value = generate_random_company_name()
            elif random_type == "datetime":
                # 如果随机类型是 "datetime"，调用 generate_random_datetime 函数
                new_value = generate_random_datetime(**kwargs)
            elif random_type == "sequential_code":
                # 如果随机类型是 "sequential_code"，调用 generate_sequential_code 函数
                new_value = generate_sequential_code(**kwargs)
            elif random_type == "product":
                # 如果随机类型是 "product"，调用 generate_random_product 函数
                new_value = generate_random_product_name()            
            else:
                # 如果 random_type 无效，则跳过当前节点的更新
                continue

            # 构建更新查询，使用节点ID来精确定位并设置新属性值
            query_update = f"""
            MATCH (n)
            WHERE elementId(n) = $node_id
            SET n.{property_name} = $new_value
            RETURN n
            """
            # 执行更新查询，并传递节点ID和新值作为参数
            result = session.run(query_update, node_id=node.element_id, new_value=new_value)
            # 获取更新后的节点记录
            updated_node_record = result.single()
            # 如果成功更新，则将更新后的节点属性字典添加到列表中
            if updated_node_record:
                updated_nodes_data.append(dict(updated_node_record['n']))
        
        # 返回包含所有更新后节点数据的字典
        return {"updated_nodes": updated_nodes_data}


def run_update_node_property_task(clazz: str, property_to_update: str, random_type: str, **kwargs):
    """
    封装节点属性更新任务，调用底层函数并打印结果
    :param clazz: 节点标签
    :param property_to_update: 需要更新的属性名
    :param random_type: 随机值类型
    :param kwargs: 传递给随机值生成函数的可选参数
    """
    # 调用核心函数执行更新
    result = update_node_with_random_value_by_property(clazz, property_to_update, random_type, **kwargs)
    # 打印将要执行的任务信息
    print(f"执行更新任务: 节点='{clazz}', 属性='{property_to_update}', 类型='{random_type}', 参数={kwargs}")


def testcase5():
    """
    测试为节点属性赋予随机值的功能（使用封装函数）
    """
    
    # 示例2: 生成两位随机数 (取消注释即可运行)
    # run_update_node_property_task(clazz, "procOrderDetProcOrderQuantity", "number", digits=2)
    
    # 示例3: 生成指定前缀的序列号 (取消注释即可运行)
    # run_update_node_property_task(clazz, property_to_update, "sequential_code", prefix="PO")
    
    # 示例4: 生成指定范围的随机日期 (取消注释即可运行)
    # run_update_node_property_task(clazz, "procOrderDetRequiredDate", "datetime", start_date_str="2026-03-01 00:00:00", end_date_str="2026-03-31 23:59:59")

    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailBizOrderUserCode", "sequential_code", prefix="BO",length=3)
    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailExternalNo", "sequential_code", prefix="PO",length=3)
    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailExternalNo", "string", length=8)
    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailExtMatCode", "sequential_code", prefix="PO",length=3)
    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailExtMatName", "product")
    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailBizOrderQuantity", "number", digits=4)
    run_update_node_property_task("PRD_RET_DET", "prdRetDetTotalQuantity", "number", digits=1)
    #run_update_node_property_task("PRD_O_APY_DET", "prdOApyDetCompleteQuantity", "number", digits=1)
    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailBizOrderReceiptDate", "datetime", start_date_str="2026-01-20 00:00:00", end_date_str="2026-02-01 23:59:59")
    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailBizOrderDeliveryDate", "datetime", start_date_str="2026-01-20 00:00:00", end_date_str="2026-02-01 23:59:59")
    run_update_node_property_task("BUSINESS_ORDER_DETAIL", "bizOrderDetailBizOrderDeliveryDate", "datetime", start_date_str="2026-02-05 00:00:00", end_date_str="2026-02-07 23:59:59")
    run_update_node_property_task("PRD_O_APY_DET", "prdOApyDetPrdOApyReceiptDate", "datetime", start_date_str="2026-02-01 00:00:00", end_date_str="2026-02-05 23:59:59")
    run_update_node_property_task("PRD_RET_DET", "prdRetDetPrdRetReceiptDate", "datetime", start_date_str="2026-02-07 00:00:00", end_date_str="2026-02-15 23:59:59")    




if __name__ == "__main__":
    testcase5()




