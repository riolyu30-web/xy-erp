import os
import sys

# 将项目根目录添加到 sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
from fastmcp import FastMCP  # 导入FastMCP框架
import json  # 导入JSON库
from services.llm_manager import dashscope_chat_json
from neo4j import GraphDatabase

neo4j_mcp = FastMCP(name="neo4j")  # 创建计算服务MCP实例

from dotenv import load_dotenv # 导入 dotenv 库
load_dotenv() # 加载根目录下的 .env 文件
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

            
if __name__ == "__main__":

    result = find_relation_path_logic(["bizOrderDetailAuditStatus", "contractDetailBriefName","prdRetDetBusDivisId"])
    print(json.dumps(result, ensure_ascii=False, indent=4))

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

