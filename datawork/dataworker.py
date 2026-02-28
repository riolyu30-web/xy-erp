import os # 导入os模块，用于与操作系统交互
import json # 导入json模块，用于处理JSON数据
import shutil # 导入shutil模块，用于文件操作
from re import L
import sys
# 将项目根目录添加到sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import services.tool as tool
import services.auth_service as auth_service 

def rename_json_files_in_directory(): # 定义一个函数来重命名目录中的JSON文件
    script_dir = os.path.dirname(os.path.abspath(__file__)) # 获取当前脚本文件所在的目录路径
    for root, dirs, files in os.walk(script_dir): # 遍历指定目录及其所有子目录
        for filename in files: # 遍历当前目录下的所有文件
            if filename.endswith('.json'): # 检查文件是否以.json结尾
                file_path = os.path.join(root, filename) # 构造文件的完整路径
                try: # 尝试执行以下代码块，以处理可能发生的错误
                    with open(file_path, 'r', encoding='utf-8') as f: # 以只读模式和UTF-8编码打开文件
                        data = json.load(f) # 从文件中加载JSON数据
                    
                    main_tab_clazz = data.get('mainTabClazz') # 从JSON数据中获取'mainTabClazz'的值
                    
                    if main_tab_clazz: # 检查'mainTabClazz'是否存在且不为空
                        new_filename = f"{main_tab_clazz}.json" # 根据'mainTabClazz'的值创建新的文件名
                        new_file_path = os.path.join(root, new_filename) # 构造新文件的完整路径
                        
                        if os.path.abspath(file_path) != os.path.abspath(new_file_path): # 确保新旧文件路径不完全相同
                            if not os.path.exists(new_file_path): # 检查新文件名是否已经存在于目录中
                                os.rename(file_path, new_file_path) # 如果不存在，则重命名文件
                                print(f"重命名: '{filename}' -> '{new_filename}'") # 打印重命名成功的信息
                            else: # 如果新文件已经存在
                                print(f"跳过: 新文件名 '{new_filename}' 已存在，原文件 '{filename}'") # 打印跳过重命名的信息
                        else: # 如果新旧文件名相同
                             print(f"跳过: 文件名 '{filename}' 已经是正确的，无需重命名。") # 打印无需重命名的信息
                    else: # 如果'mainTabClazz'不存在或为空
                        print(f"跳过: '{filename}' 中缺少 'mainTabClazz' 键或其值为空.") # 打印跳过文件的信息
                except json.JSONDecodeError: # 捕获JSON解码错误
                    print(f"错误: '{filename}' 不是一个有效的JSON文件.") # 打印文件非有效JSON的错误信息
                except Exception as e: # 捕获其他所有类型的异常
                    print(f"处理 '{filename}' 时发生错误: {e}") # 打印处理文件时发生的未知错误

def check_json_files_integrity(): # 定义一个函数来检查JSON文件的完整性
    print("\n--- 开始检查JSON文件完整性 ---") # 打印检查开始的提示信息
    script_dir = os.path.dirname(os.path.abspath(__file__)) # 获取当前脚本文件所在的目录路径
    table_name_map = {} # 创建一个空字典来存储table_name及其文件路径
    main_tab_clazz_map = {} # 创建一个空字典来存储mainTabClazz及其文件路径

    for root, dirs, files in os.walk(script_dir): # 遍历指定目录及其所有子目录
        for filename in files: # 遍历当前目录下的所有文件
            if filename.endswith('.json'): # 检查文件是否以.json结尾
                file_path = os.path.join(root, filename) # 构造文件的完整路径
                try: # 尝试执行以下代码块
                    with open(file_path, 'r', encoding='utf-8') as f: # 以只读模式和UTF-8编码打开文件
                        data = json.load(f) # 加载JSON数据
                    
                    table_name = data.get('table_name') # 获取'table_name'的值
                    main_tab_clazz = data.get('mainTabClazz') # 获取'mainTabClazz'的值
                    base_filename, _ = os.path.splitext(filename) # 获取不带扩展名的文件名

                    # 检查 table_name 是否为空
                    if not table_name: # 如果'table_name'为空或不存在
                        print(f"警告: 文件 '{file_path}' 的 'table_name' 为空。") # 打印警告信息
                    else: # 如果'table_name'存在
                        if table_name not in table_name_map: # 如果'table_name'不在字典中
                            table_name_map[table_name] = [] # 为其创建一个空列表
                        table_name_map[table_name].append(file_path) # 将文件路径添加到列表中

                    # 检查文件名是否与 mainTabClazz 不匹配
                    if main_tab_clazz and base_filename != main_tab_clazz: # 如果'mainTabClazz'存在且文件名与其不匹配
                        print(f"警告: 文件 '{file_path}' 的文件名 ('{base_filename}') 与 'mainTabClazz' ('{main_tab_clazz}') 不匹配。") # 打印警告信息
                    
                    if main_tab_clazz: # 如果'mainTabClazz'存在
                        if main_tab_clazz not in main_tab_clazz_map: # 如果'mainTabClazz'不在字典中
                            main_tab_clazz_map[main_tab_clazz] = [] # 为其创建一个空列表
                        main_tab_clazz_map[main_tab_clazz].append(file_path) # 将文件路径添加到列表中

                except json.JSONDecodeError: # 捕获JSON解码错误
                    print(f"错误: '{filename}' 不是一个有效的JSON文件。") # 打印文件非有效JSON的错误信息
                except Exception as e: # 捕获其他所有类型的异常
                    print(f"处理 '{filename}' 时发生错误: {e}") # 打印处理文件时发生的未知错误

    print("\n--- 开始检查重复值 ---") # 打印检查重复值的提示信息
    # 检查重复的 table_name
    for name, paths in table_name_map.items(): # 遍历table_name字典
        if len(paths) > 1: # 如果一个table_name出现在多个文件中
            print(f"警告: 'table_name' ('{name}') 在多个文件中重复出现:") # 打印重复警告
            for path in paths: # 遍历文件路径
                print(f"  - {path}") # 打印文件路径

    # 检查重复的 mainTabClazz
    for clazz, paths in main_tab_clazz_map.items(): # 遍历mainTabClazz字典
        if len(paths) > 1: # 如果一个mainTabClazz出现在多个文件中
            print(f"警告: 'mainTabClazz' ('{clazz}') 在多个文件中重复出现:") # 打印重复警告
            for path in paths: # 遍历文件路径
                print(f"  - {path}") # 打印文件路径

    print("--- JSON文件完整性检查完成 ---") # 打印检查完成的提示信息

def check_json_data_complete():
    access_token = auth_service.auth_login()
    print("\n--- 开始检查JSON数据完整性 ---")
    
    report = {
        "no_data": [],
        "incomplete_params": [],
        "complete": []
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(script_dir):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                    
                    api_name = json_data.get('api_name')
                    request_payload = json_data.get('request', {})
                    response_keys = json_data.get('response', {}).keys()
                    main_tab_clazz = json_data.get('mainTabClazz', 'N/A')

                    if not api_name:
                        continue

                    print(f"正在检查: {api_name} ({main_tab_clazz})")
                    
                    api_data = tool.get_data(api_name, request_payload, access_token)
                    
                    total_keys_count = len(response_keys)

                    if not api_data:
                        print(f"  -> 结果: 无数据")
                        report["no_data"].append(f"{main_tab_clazz} (0%)")
                    else:
                        first_item = api_data[0]
                        
                        present_keys = [key for key in response_keys if key in first_item]
                        missing_keys = [key for key in response_keys if key not in first_item]
                        
                        present_keys_count = len(present_keys)
                        
                        completeness_rate = (present_keys_count / total_keys_count * 100) if total_keys_count > 0 else 100
                        
                        report_entry = f"{main_tab_clazz} ({completeness_rate:.0f}%)"

                        if missing_keys:
                            print(f"  -> 结果: 参数不齐")
                            print(f"     完整率: {completeness_rate:.0f}% ({present_keys_count}/{total_keys_count})")
                            print(f"     存在的字段: {', '.join(present_keys) if present_keys else '无'}")
                            print(f"     缺少的字段: {', '.join(missing_keys)}")
                            report["incomplete_params"].append(report_entry)
                        else:
                            print(f"  -> 结果: 参数完整")
                            report["complete"].append(report_entry)
                except Exception as e:
                    print(f"处理文件 {filename} 时出错: {e}")

    print("\n--- 检查报告 ---")
    print(f"总计 - 无数据: {len(report['no_data'])} | 参数不齐: {len(report['incomplete_params'])} | 参数完整: {len(report['complete'])}")
    
    print("\n--- 无数据列表 ---")
    print(", ".join(report['no_data']) if report['no_data'] else "无")
    
    print("\n--- 参数不齐列表 ---")
    print(", ".join(report['incomplete_params']) if report['incomplete_params'] else "无")
    
    print("\n--- 参数完整列表 ---")
    print(", ".join(report['complete']) if report['complete'] else "无")
    print("\n--- 检查结束 ---") 


def check_json_name_complete():
    print("\n--- 开始检查JSON字段命名规范 ---")
    
    report = {
        "non_compliant": [],
        "compliant": []
    }
    total_meanings_checked = 0
    total_meanings_non_compliant = 0

    script_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(script_dir):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                    
                    table_name = json_data.get('table_name')
                    response_obj = json_data.get('response', {})
                    meanings_to_check = [v['meaning'] for v in response_obj.values() if isinstance(v, dict) and 'meaning' in v and v['meaning']]
                    main_tab_clazz = json_data.get('mainTabClazz', 'N/A')

                    print(f"正在检查: {filename} ({main_tab_clazz})")

                    if not table_name or not meanings_to_check:
                        print(f"  -> 结果: 跳过 (无table_name或无带'meaning'的response字段)")
                        report["compliant"].append(f"{main_tab_clazz} (100%)")
                        continue
                    
                    print(f"  -> 前缀应为: '{table_name}'")

                    incorrect_meanings = [meaning for meaning in meanings_to_check if not meaning.startswith(table_name)]
                    
                    total_meanings_count = len(meanings_to_check)
                    correct_meanings_count = total_meanings_count - len(incorrect_meanings)

                    total_meanings_checked += total_meanings_count
                    total_meanings_non_compliant += len(incorrect_meanings)
                    
                    compliance_rate = (correct_meanings_count / total_meanings_count * 100) if total_meanings_count > 0 else 100
                    
                    report_entry = f"{main_tab_clazz} ({compliance_rate:.0f}%)"

                    if incorrect_meanings:
                        print(f"  -> 结果: 命名不规范")
                        print(f"     合规率: {compliance_rate:.0f}% ({correct_meanings_count}/{total_meanings_count})")
                        print(f"     不合规的'meaning': {', '.join(incorrect_meanings)}")
                        report["non_compliant"].append(report_entry)
                    else:
                        print(f"  -> 结果: 命名规范")
                        report["compliant"].append(report_entry)

                except Exception as e:
                    print(f"处理文件 {filename} 时出错: {e}")

    print("\n--- 命名规范检查报告 ---")
    overall_non_compliance_rate = (total_meanings_non_compliant / total_meanings_checked * 100) if total_meanings_checked > 0 else 0
    print(f"总计 - 不规范接口: {len(report['non_compliant'])} | 规范接口: {len(report['compliant'])} | 字段整体不合规率: {overall_non_compliance_rate:.2f}%")
    
    print("\n--- 命名不规范列表 ---")
    print(", ".join(report['non_compliant']) if report['non_compliant'] else "无")
    
    print("\n--- 命名规范列表 ---")
    print(", ".join(report['compliant']) if report['compliant'] else "无")
    print("\n--- 检查结束 ---")

def make_data_scheme():
    import re
    print("\n--- 开始生成数据可达性方案 (Scheme) ---")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_base_dir = os.path.join( os.path.dirname(script_dir), 'scheme')
    
    os.makedirs(output_base_dir, exist_ok=True)
    print(f"方案将保存在: {output_base_dir}")

    access_token = auth_service.auth_login()
    if not access_token:
        print("错误: 获取 access_token 失败，无法继续。")
        return

    for root, dirs, files in os.walk(script_dir):

        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                print(f"\n正在处理: {file_path}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                    
                    api_name = json_data.get('api_name')
                    request_payload = json_data.get('request', {})
                    response_schema = json_data.get('response', {})
                    table_name = json_data.get('table_name')

                    if not api_name or not response_schema:
                        print("  -> 跳过: 缺少 'api_name' 或 'response' 部分。")
                        continue

                    api_data = tool.get_data(api_name, request_payload, access_token)
                    
                    first_item = None
                    if api_data:
                        first_item = api_data[0]
                        print(f"  -> 成功获取到 {len(api_data)} 条数据，将使用第一条进行对比。")
                    else:
                        print("  -> 警告: 未获取到任何数据。所有字段将标记为不可达。")

                    for key, value in response_schema.items():
                        if isinstance(value, dict):
                            # Set reachability
                            if first_item and key in first_item:
                                value['reachable'] = True
                            else:
                                value['reachable'] = False
                            
                            # Generate name field
                            name = ""
                            meaning = value.get('meaning', '')
                            if table_name and meaning and meaning.startswith(table_name):
                                suffix = meaning[len(table_name):]
                                match = re.search(r'[ (（。]', suffix)
                                if match:
                                    name = table_name + suffix[:match.start()]
                                else:
                                    name = table_name + suffix
                            value['name'] = name
                    
                    
                    relative_dir = os.path.relpath(root, script_dir)
                    output_dir = os.path.join(output_base_dir, relative_dir)
                    os.makedirs(output_dir, exist_ok=True)
                    
                    output_file_path = os.path.join(output_dir, filename)
                    
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=4)
                    
                    print(f"  -> 成功生成方案文件: {output_file_path}")

                except Exception as e:
                    print(f"  -> 处理文件 {filename} 时出错: {e}")

    print("\n--- 数据可达性方案生成完毕 ---")

def check_relation_complete(file_path):
    import os
    import json
    print("\n--- 开始检查关系完整性 ---")
    
    missing_files = set()
    wrong_files = set()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scheme_dir = os.path.join(os.path.dirname(script_dir), 'scheme')
    
    if not os.path.exists(scheme_dir):
        print(f"错误: 'scheme' 目录不存在于 {os.path.dirname(script_dir)}")
        return

    # 遍历scheme目录及其所有子目录，获取所有存在的json文件名
    existing_scheme_files = set()
    for root, dirs, files in os.walk(scheme_dir):
        for file in files:
            if file.endswith('.json'):
                existing_scheme_files.add(file)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '_CO' in line:
                    continue
                
                nodes = line.split('-')
                if len(nodes)==2:

                    for node in nodes:

                        if node == "undefined" or not node:
                            continue
                        
                        json_file_name = f"{node}.json"
                        
                        # 检查json文件名是否存在于已找到的文件集合中
                        if json_file_name not in existing_scheme_files:
                            missing_files.add(node)
                else:
                    wrong_files.add(line)

    except FileNotFoundError:
        print(f"错误: 在 {file_path} 未找到输入文件")
        return
    except Exception as e:
        print(f"处理文件时出错: {e}")
        return

    if missing_files:
        print("\n--- 发现缺失的Scheme文件 ---")
        for missing_file in sorted(list(missing_files)):
            print(f"{missing_file}")
    else:
        print("\n--- 关系完整性检查通过，所有节点都有对应的Scheme文件 ---")
    if wrong_files:
        print("\n--- 发现错误的关系 ---")
        for wrong_file in sorted(list(wrong_files)):
            print(f"{wrong_file}")
    else:
        print("\n--- 关系完整性检查通过，所有关系格式正确 ---")        
    print("\n--- 关系完整性检查完成 ---")

def make_relation_json(file_path):
    import json
    import os
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '_CO' in line:
                    continue
                parts = line.split('-')
                if len(parts) > 1:
                    for i in range(len(parts) - 1):
                        links.append({"s": parts[i], "t": parts[i+1]})
    except FileNotFoundError:
        print(f"错误: 在 {file_path} 未找到输入文件")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join( os.path.dirname(script_dir), 'mcp_relation.json')
    
    # 获取输入文件的文件名作为键
    key_name = os.path.splitext(os.path.basename(file_path))[0]

    # 读取现有的JSON数据
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            output_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        output_data = {}

    # 添加或更新键值对
    output_data[key_name] = links

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"成功更新 {output_path}")
    except IOError as e:
        print(f"写入输出文件时出错: {e}")

def remove_relation(input_file,cancel_txt):
    # cancel_txt 是一个包含多个ID的字符串，每个ID占一行
    # 使用 splitlines() 方法将字符串按行分割，并去除每行首尾的空白字符
    # 最后，使用集合推导式创建一个包含所有非空ID的集合，以提高查找效率
    cancel_ids = {line.strip() for line in cancel_txt.strip().splitlines() if line.strip()}

    # 创建一个空列表，用于存储需要保留的行
    lines_to_keep = []
    # 打开input_file文件，使用'r'模式以只读方式打开，并指定编码为'utf-8'
    with open(input_file, 'r', encoding='utf-8') as f:
        # 遍历文件中的每一行
        for line in f:
            # 去除当前行的首尾空白字符
            stripped_line = line.strip()
            # 如果行为空，则跳过当前循环
            if not stripped_line:
                continue
            
            # 使用'-'作为分隔符来分割当前行
            parts = stripped_line.split('-')
            isKeep = True
            for node in parts:
                if node in cancel_ids:
                    isKeep = False
                    break
            if isKeep:
                lines_to_keep.append(stripped_line)

    # 再次打开input_file文件，但这次使用'w'模式以写入方式打开，这将清空文件内容
    with open(input_file, 'w', encoding='utf-8') as f:
        # 遍历lines_to_keep列表中的每一行
        for line in lines_to_keep:
            # 将行内容写入文件，并在末尾添加换行符
            f.write(line + '\n')

def get_link_data(access_token: str, relation_line: str):  # 定义测试函数
    """
    根据关系对象获取数据并创建链接
    """
    # 使用'-'作为分隔符来分割当前行
    parts = relation_line.split('-')
    if len(parts) == 2:
        source_clazz = parts[0] # 获取源节点标签
        target_clazz = parts[1] # 获取目标节点标签
        clazz = source_clazz+"-"+target_clazz # 获取关系名称，用于API调用
    else:
        print(f"{relation_line}") # 如果不完整，打印警告并跳过
        return # 返回        

    if not source_clazz or not target_clazz or not clazz: # 检查关系对象是否完整
        print(f"{relation_line}") # 如果不完整，打印警告并跳过
        return # 返回

    data = {} # 初始化数据字典
    # 构建请求URL
    data["api_name"] = "/proof/linkFindList"  # API地址

    # 构建请求体数据
    data["request"] = {
        "linkTypeCode": "source",  # 固定参数
        "linkClazz": clazz,  # 使用从对象中获取的关系名称
    }  # 数据字典结束
    link_records = tool.get_data(data["api_name"],data["request"],access_token) # 调用getData获取链接记录
    return link_records

def check_relaiton_data(input_file):
    """
    检查关系文件中的每一行，并统计成功和失败的组数。
    """
    access_token = auth_service.auth_login()
    if not access_token:
        print("错误: 获取 access_token 失败，无法继续。")
        return

    success_group = []
    failure_group = []

    with open(input_file, 'r', encoding='utf-8') as f:
        # 一次性读取所有行并去除空行
        lines = [line.strip() for line in f if line.strip()]

    print(f"🔍 开始检查 {len(lines)} 组关系...")

    for line in lines:
        data = get_link_data(access_token, line)
        if data:
            success_group.append(line)
        else:
            failure_group.append(line)

    print("\n--- 检查结果统计 ---")
    print(f"✅ 成功: {len(success_group)} 组")
    print(f"❌ 失败: {len(failure_group)} 组")

    if failure_group:
        print("\n失败的详细列表:")
        for item in failure_group:
            print(f"{item}") 

def find_all_relation():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取关系文件的绝对路径
    relation_path = os.path.join(os.path.dirname(script_dir), 'mcp_relation.json')
    # 定义输出文件路径
    output_path = os.path.join(os.path.dirname(script_dir), 'relation.txt')
    # 初始化邻接表用于存储图结构
    graph = {}
    # 初始化集合用于存储所有出现的节点
    nodes = set()
    # 初始化字典用于存储每个节点的入度
    in_degree = {}
    # 初始化正常路径计数器
    normal_count = 0
    # 初始化环路路径计数器
    cycle_count = 0

    # 以只读模式打开关系数据文件
    with open(relation_path, 'r', encoding='utf-8') as f:
        # 解析JSON文件内容
        data = json.load(f)
        # 提取link列表，若无效则为空
        link_list = data.get("link") if isinstance(data.get("link"), list) else []
        # 提取parent列表，若无效则为空
        parent_list = data.get("parent") if isinstance(data.get("parent"), list) else []
        # 合并两个列表以统一处理
        all_items = link_list + parent_list

        # 遍历所有关系项
        for item in all_items:
            # 提取起点s
            s = item.get("s")
            # 提取终点t
            t = item.get("t")
            # 校验起点和终点是否有效
            if s and t:
                # 初始化起点的邻接列表
                if s not in graph: graph[s] = []
                # 将终点加入起点的邻接列表
                graph[s].append(t)
                # 记录起点
                nodes.add(s)
                # 记录终点
                nodes.add(t)
                # 初始化起点入度
                if s not in in_degree: in_degree[s] = 0
                # 初始化终点入度
                if t not in in_degree: in_degree[t] = 0
                # 终点入度加1
                in_degree[t] += 1

    # 以写模式打开输出文件
    with open(output_path, 'w', encoding='utf-8') as out_f:
        # 定义递归函数用于深度优先搜索路径
        def dfs(u, current_path):
            # 声明使用外部统计变量
            nonlocal normal_count, cycle_count
            # 将当前节点加入路径
            current_path.append(u)
            # 获取当前节点的邻居列表
            neighbors = graph.get(u, [])
            # 如果没有邻居，说明到达路径末端
            if not neighbors:
                # 生成路径字符串
                path_str = "-".join(current_path)
                # 输出完整路径
                print(path_str)
                # 写入文件
                out_f.write(path_str + "\n")
                # 正常路径计数加1
                normal_count += 1
                # 返回上一层
                return

            # 遍历所有邻居节点
            for v in neighbors:
                # 检查是否形成环路
                if v in current_path:
                    # 生成带环路径字符串
                    path_str = "-".join(current_path + [v]) + " [CYCLE]"
                    # 输出带环路径提示
                    print(path_str)
                    # 写入文件
                    out_f.write(path_str + "\n")
                    # 环路路径计数加1
                    cycle_count += 1
                else:
                    # 递归继续搜索
                    dfs(v, current_path[:])

        # 寻找所有入度为0的节点作为根节点
        roots = [n for n in nodes if in_degree[n] == 0]
        # 如果没有根节点但有数据，说明全是环，取所有节点尝试
        if not roots and nodes: roots = list(nodes)

        # 遍历所有根节点开始搜索
        for root in roots:
            # 开始DFS搜索
            dfs(root, [])
            
        # 生成统计信息字符串
        summary = f"\nTotal Normal Paths: {normal_count}\nTotal Cycle Paths: {cycle_count}"
        # 输出统计信息
        print(summary)
        # 将统计信息写入文件
        out_f.write(summary + "\n")

def check_one_scheme_data(name:str):
    # 获取认证token
    access_token = auth_service.auth_login()
    # 检查token是否成功获取
    if not access_token:
        # 打印错误信息
        print("错误: 获取 access_token 失败，无法继续。")
        # 返回
        return

    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建scheme目录的路径
    scheme_dir = os.path.join(os.path.dirname(script_dir), 'scheme')
    # 初始化文件路径为空
    file_path = None
    # 目标文件名
    target_filename = f"{name}.json"

    # 遍历scheme目录查找文件
    for root, dirs, files in os.walk(scheme_dir):
        # 检查目标文件是否在当前目录的文件列表中
        if target_filename in files:
            # 找到文件，构建完整路径
            file_path = os.path.join(root, target_filename)
            # 停止遍历
            break

    # 打印正在查找的文件路径
    print(f"正在查找方案文件: {file_path}")

    # 检查文件是否存在
    if not os.path.exists(file_path):
        # 打印文件不存在的错误信息
        print(f"错误: 方案文件 '{file_path}' 不存在。")
        # 返回
        return

    # 尝试读取和解析JSON文件
    try:
        # 打开文件
        with open(file_path, 'r', encoding='utf-8') as f:
            # 加载JSON数据
            json_data = json.load(f)
    # 捕获异常
    except Exception as e:
        # 打印读取或解析错误的日志
        print(f"读取或解析JSON文件 '{file_path}' 时出错: {e}")
        # 返回
        return

    # 从JSON数据中获取api_name
    api_name = json_data.get('api_name')
    # 从JSON数据中获取request负载，默认为空字典
    request_payload = json_data.get('request', {})

    # 检查api_name是否存在
    if not api_name:
        # 打印缺少api_name的错误信息
        print(f"错误: 方案文件 '{file_path}' 中缺少 'api_name'。")
        # 返回
        return

    # 打印获取到的api_name
    print(f"从 '{name}.json' 中获取到 api_name: '{api_name}'")
    # 打印请求负载
    print(f"使用请求负载: {request_payload}")

    # 调用工具函数获取数据
    api_data = tool.get_data(api_name, request_payload, access_token)

    # 检查是否获取到数据
    if api_data:
        # 打印成功获取数据的消息
        print(f"成功从 API '{api_name}' 获取到 {len(api_data)} 条数据。")
        # 打印第一条数据作为示例
        #print("数据示例 (第一条):")
        # 使用json.dumps美化输出
        #print(json.dumps(api_data[0], indent=4, ensure_ascii=False))
    # 如果没有获取到数据
    else:
        # 打印未获取到数据的消息
        print(f"未能从 API '{api_name}' 获取到任何数据。")
    
    # 返回获取到的数据
    return api_data

def temp_get_ids():
    import json # 导入json模块，用于处理JSON数据
    import csv # 导入csv模块，用于处理CSV文件
    input_file = r'e:\tx-erp\erp-service\temp.json' # 定义输入JSON文件的路径
    output_file = r'e:\tx-erp\erp-service\temp.csv' # 定义输出CSV文件的路径

    with open(input_file, 'r', encoding='utf-8') as f: # 以只读模式打开JSON文件，使用utf-8编码
        data = json.load(f) # 加载JSON文件内容

    path_data_list = data.get('path_data_list', []) # 从JSON数据中获取'path_data_list'，如果不存在则返回空列表

    with open(output_file, 'w', newline='', encoding='utf-8') as f: # 以写入模式打开CSV文件，设置newline=''以避免空行
        writer = csv.writer(f) # 创建一个csv写入器
        writer.writerow(['bizOrderDetailId', 'prdOApyDetId', 'bizOrderDetailBizOrderId']) # 写入CSV文件的表头
        for item in path_data_list: # 遍历'path_data_list'中的每一个元素
            writer.writerow([ # 写入一行数据
                item.get('bizOrderDetailId'), # 获取'bizOrderDetailId'的值
                item.get('prdOApyDetId'), # 获取'prdOApyDetId'的值
                item.get('bizOrderDetailBizOrderId') # 获取'bizOrderDetailBizOrderId'的值
            ])

def temp_check_ids():
    import csv # 导入csv模块
    file1 = r'e:\tx-erp\erp-service\temp.csv' # 定义第一个CSV文件的路径
    file2 = r'e:\tx-erp\erp-service\temp2.csv' # 定义第二个CSV文件的路径

    with open(file1, 'r', encoding='utf-8') as f1: # 以只读模式打开第一个文件
        reader1 = csv.reader(f1) # 创建一个csv读取器
        next(reader1) # 跳过表头
        set1 = set(tuple(row) for row in reader1) # 读取所有行并转换为元组集合以便快速查找

    with open(file2, 'r', encoding='utf-8') as f2: # 以只读模式打开第二个文件
        reader2 = csv.reader(f2) # 创建一个csv读取器
        next(reader2) # 跳过表头
        for row in reader2: # 遍历第二个文件的每一行
            if tuple(row) not in set1: # 检查当前行是否存在于第一个文件的集合中
                print(row) # 如果不存在，则打印该行   

def check_ids(api_data, target_key, target_value): # 定义一个函数，接收一个数据列表、一个目标键和一个目标值
    # 使用列表推导式高效地筛选出符合条件的元素
    return [ # 返回一个列表
        item for item in api_data # 遍历api_data中的每一个项目
        if isinstance(item, dict) and item.get(target_key) == target_value # 检查项目是否为字典，并且其指定键的值是否等于目标值
    ]

def find_all_wrong_scheme():
    print("\n--- 正在扫描 Scheme 文件 (Datawork) ---")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建 wrong 目录
    wrong_dir = os.path.join(script_dir, "wrong")
    if not os.path.exists(wrong_dir):
        os.makedirs(wrong_dir)
        print(f"📁 已创建 wrong 目录: {wrong_dir}")
    else:
        print(f"📁 wrong 目录已存在: {wrong_dir}")

    found_files = []
    
    for root, dirs, files in os.walk(script_dir):
        # 跳过 wrong 目录本身，防止递归扫描
        if "wrong" in root:
            continue
            
        for filename in files:
            if not filename.endswith('.json'):
                continue
                
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                table_name = data.get('table_name')
                response = data.get('response', {})
                
                if not table_name or not response:
                    continue
                
                # 获取所有有效的 meaning
                meanings = [
                    v['meaning'] for v in response.values() 
                    if isinstance(v, dict) and v.get('meaning')
                ]
                
                if not meanings:
                    continue
                
                # 检查是否存在至少一个 meaning 以 table_name 开头
                has_valid_meaning = any(m.startswith(table_name) for m in meanings)
                
                if not has_valid_meaning:
                    found_files.append({
                        "path": file_path,
                        "filename": filename,
                        "table_name": table_name,
                        "meanings_sample": meanings[:3] # 取前3个作为样本
                    })
                    
                    # 复制文件到 wrong 目录
                    dest_path = os.path.join(wrong_dir, filename)
                    shutil.copy2(file_path, dest_path)
                    print(f"  -> 已复制: {filename}")
                    
            except Exception:
                continue
    
    if found_files:
        print(f"\n❌ 发现 {len(found_files)} 个文件，其字段 meaning 均不以 table_name 开头：")
        for item in found_files:
            print(f"\n📄 文件: {item['filename']}")
            print(f"   路径: {item['path']}")
            print(f"   表名: {item['table_name']}")
            print(f"   字段 Meaning 示例: {item['meanings_sample']} ...")
        print(f"\n⚠️ 所有不合规文件已备份至: {wrong_dir}")
    else:
        print("\n✅ 未发现问题文件，所有 Scheme 至少有一个字段符合命名规范。")
        
def fix_all_wrong_scheme():
    print("\n--- 正在将 wrong 目录下的修复文件覆盖回原处 ---")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wrong_dir = os.path.join(script_dir, "wrong")
    
    if not os.path.exists(wrong_dir):
        print(f"❌ 错误: wrong 目录不存在 ({wrong_dir})")
        return

    # 获取 wrong 目录下所有 JSON 文件
    fixed_files = [f for f in os.listdir(wrong_dir) if f.endswith('.json')]
    
    if not fixed_files:
        print("⚠️ wrong 目录下没有找到 JSON 文件。")
        return

    print(f"📦 待处理文件数: {len(fixed_files)}")

    # 建立原文件索引：文件名 -> 完整路径
    # 因为原文件分散在 datawork 的各个子目录中，我们需要先找到它们在哪里
    original_files_map = {}
    for root, dirs, files in os.walk(script_dir):
        # 跳过 wrong 目录本身
        if "wrong" in root:
            continue
            
        for filename in files:
            if filename.endswith('.json'):
                # 如果有重名文件，这里会覆盖，但假设 datawork 下 json 文件名唯一
                original_files_map[filename] = os.path.join(root, filename)

    success_count = 0
    fail_count = 0

    for filename in fixed_files:
        src_path = os.path.join(wrong_dir, filename)
        
        if filename in original_files_map:
            dest_path = original_files_map[filename]
            try:
                shutil.copy2(src_path, dest_path)
                print(f"  ✅ 已覆盖: {filename} -> {os.path.relpath(dest_path, script_dir)}")
                success_count += 1
            except Exception as e:
                print(f"  ❌ 覆盖失败 {filename}: {e}")
                fail_count += 1
        else:
            print(f"  ⚠️ 未找到原文件路径，跳过: {filename} (可能原文件已被删除或改名)")
            fail_count += 1

    print(f"\n🎉 处理完成: 成功 {success_count} 个, 失败/跳过 {fail_count} 个")

if __name__ == "__main__": # 检查当前脚本是否是作为主程序运行
    # find_all_wrong_scheme()
    #fix_all_wrong_scheme()
    #rename_json_files_in_directory()

    #check_json_files_integrity()

    

    make_data_scheme()

    input_file = r'e:\tx-erp\erp-service\datawork\link.txt'
    #input_file = r'e:\tx-erp\erp-service\datawork\parent.txt'
    #check_relation_complete(input_file)

    cancel_txt="""
PURCHASE_FORECASTING
TYPE
APY
AUXILIARY_PROCESSES
BILLING_SOLUTION
CO
DEMO
DET
FATHER_WORK_ORDER
FIN_IN
I
META_SMART_LINK
MOULD
ORGANIZATION
PRD
PRODUCTION
STANDARDMATERIAL
SUIT
SUIT_ORDER_DETAIL
SUPPLIER
TABLE   
    """

    #remove_relation(input_file,cancel_txt)


    #check_relaiton_data(input_file)


    #make_relation_json(input_file)

    # 执行全路径查找并保存
    #find_all_relation()

    #api_data = check_one_scheme_data("PRD_O_APY_DET")

    #print(len(api_data))
    
    #print(check_ids(api_data,"prdOApyDetId","2502d9316cdd412cb6495bc6c93a396d"))
    #temp_get_ids()

    #temp_check_ids()

    #api_data = check_one_scheme_data("BUSINESS_ORDER")
    
    #print(check_ids(api_data,"bizOrderId","cd9edc8e48a24cb89ad0e29faf7e7174"))

    #api_data = check_one_scheme_data("BUSINESS_ORDER_DETAIL")
    
    #print(check_ids(api_data,"bizOrderDetailId","0247a5063cdd436c9fff5013975096dc"))
