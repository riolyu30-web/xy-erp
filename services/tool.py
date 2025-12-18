from jinja2.utils import F
import pandas as pd
from datetime import datetime
from io import StringIO
from datetime import datetime  # 导入日期时间模块
import tempfile  # 导入临时文件模块
import uuid  # 导入UUID模块
import os  # 导入操作系统模块
from qiniu import Auth, put_file, put_data  # 导入七牛云SDK
import base64  # 导入base64模块
from services.supabase_manager import SupabaseManager  
import requests  # 导入requests模块用于HTTP请求
import json  # 导入json模块用于处理JSON数据
from services.cache import cache_save  # 导入缓存服务
from dotenv import load_dotenv  # 从dotenv模块导入load_dotenv函数用于加载环境变量
# 加载环境变量
load_dotenv()  # 加载.env文件中的环境变量

# 从环境变量获取配置
BASE_URL = os.getenv("BASE_URL", "http://192.168.0.156:28002")  # 获取基础URL

def fetch_data(api_name:str, url: str, data: dict, access_token: str, filtered_fields:dict, meaning_dict: dict = None, debug_mode: bool = False, params: dict = None) -> dict:
    """
    通用工具方法：发送API请求并过滤返回数据中的指定字段
    
    Args:
        api_name: 别名
        url: API请求地址
        data: 请求体数据
        access_token: 访问令牌
        filtered_fields: 需要保留的字段列表，可以是字符串列表、字典列表或字典
        meaning_dict_str: 字段含义字典字符串（可选）
        params: 请求参数（可选）
        
    Returns:
        dict: 包含过滤后数据的响应对象，数据格式为CSV字符串
    """
    try:
        url = f"{BASE_URL}{url}?access_token={access_token}"

        # 发送POST请求
        if params:
            response = requests.post(url, params=params, json=data)
        else:
            response = requests.post(url, json=data)
            
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析响应数据
        result = response.json()
        
        # 检查响应中是否包含data字段
        if "data" not in result:
            return {"error": "没有权限"}
        
        # 提取数据列表
        data_list = result["data"]
        
        
        #print(json.dumps(data_list[0], ensure_ascii=False))
        # 仅保留指定字段
        filtered_list = []
        for item in data_list:
            filtered_item = {}
            
            # 处理不同类型的filtered_fields
            if isinstance(filtered_fields, dict):
                # 如果是字典，使用键作为字段名，值可能是字符串或包含name和value映射的字典
                for field_key, field_config in filtered_fields.items():
                    if field_key in item:
                        # 获取原始值
                        raw_value = item[field_key]
                        
                        # 判断配置类型
                        if isinstance(field_config, dict):
                            # 如果是字典配置，获取显示的列名
                            csv_header = field_config.get("name", field_key)
                            
                            # 检查是否有值映射配置
                            if "values" in field_config and isinstance(field_config["values"], dict):
                                # 尝试进行值映射，将原始值转为字符串后查找，找不到则用原始值
                                str_val = str(raw_value).lower() # 统一转小写字符串匹配（针对true/false）
                                # 这里为了兼容性，可以尝试直接匹配或转字符串匹配
                                mapping = field_config["values"]
                                # 优先尝试直接匹配，然后尝试字符串匹配
                                if raw_value in mapping:
                                    filtered_item[csv_header] = mapping[raw_value]
                                elif str_val in mapping:
                                    filtered_item[csv_header] = mapping[str_val]
                                else:
                                    filtered_item[csv_header] = raw_value
                            else:
                                # 没有映射配置，直接使用原始值
                                filtered_item[csv_header] = raw_value
                        else:
                            # 如果配置只是字符串，直接作为列名
                            filtered_item[field_config] = raw_value           
            filtered_list.append(filtered_item)
        
        # 将结果数组转换为DataFrame，然后使用pd_to_csv方法转换为CSV字符串
        if not filtered_list:
            return {"error": "没有数据，请尝试其他参数"}
        
        # 创建DataFrame
        df = pd.DataFrame(filtered_list)
        df = df.dropna(axis='columns', how='all') # 删除所有值都为空的列  

        if df.empty:
            return {"error": "没有数据，请尝试其他接口"}

        # 使用pd_to_csv方法转换为CSV字符串
        csv_string = pd_to_csv(df)
        if csv_string:
            meaning_dict_str = ""        # 替换列名
            if meaning_dict:
                meaning_dict = {k: v for k, v in meaning_dict.items() if k in df.columns} # 只保留df中存在的列                
                meaning_dict_str = json.dumps(meaning_dict, ensure_ascii=False)
            key = f"{api_name}_{access_token}"
            if debug_mode:
                print(f"测试用例: {api_name}")
                print(f"原始数据: {filtered_list[0]}")
                print(f"数据条数: {len(filtered_list)}")
                print("\n".join(csv_string.splitlines()[:5]))
                return {"table_token": key, "field_meaning": meaning_dict_str, "sample": csv_string.splitlines()[:3]} 
            elif cache_save(key, csv_string): # 缓存数据
                return {"table_token": key,"field_meaning": meaning_dict_str,} 
            else:
                return {"error": "缓存异常，请暂停服务告知用户"}
        # 返回CSV字符串
        return {"error": "没有数据，请尝试其他接口"}
        
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        return {"error": "请求异常，请暂停服务告知用户"}
    except json.JSONDecodeError as e:
        # 处理JSON解析异常
        return {"error": "解析异常，请尝试其他接口"}
    except Exception as e:
        # 处理其他异常
        return {"error": str(e)}


def get_ids(data_list, key):
    """
    从数据列表中提取指定key的值列表

    Args:
        data_list: 数据列表
        key: 要提取的key

    Returns:
        ids: 提取到的value列表
    """
    if not data_list or not isinstance(data_list, list):
        return []
    ids = []
    for data in data_list:
        if key in data and data[key]:
            ids.append(data[key])
    return ids


def set_data(source_list, result_list, source_key, source_value, result_key, result_value):
    """
    将result_list中的result_key和result_value的值设置到source_list中

    Args:
        source_list: 源数据列表
        result_list: 结果数据列表
        source_key: 源数据列表中的key
        source_value: 源数据列表中的value
        result_key: 结果数据列表中的key
        result_value: 结果数据列表中的value
    """
    key_to_value = {}
    if result_list and isinstance(result_list, list):
        for result in result_list:
            if result_key in result and result_value in result:
                key_to_value[result[result_key]] = result[result_value]

        for source in source_list:
            if source_key in source:
                key = source[source_key]
                if key in key_to_value:
                    source[source_value] = key_to_value[key]
                else:
                    source[source_value] = "未知"
    return source_list


def append_data(source_list, result_list, source_key, result_key):
    """
    将result_list中每个对象的result_key和result_key匹配 ，如果匹配到，将result_key对应字典添加到source_list的对象中
    Args:
        source_list: 源数据列表
        result_list: 结果数据列表
        source_key: 源数据列表中的key
        result_key: 结果数据列表中的key
    """
    key_to_dict = {}
    if result_list and isinstance(result_list, list):
        # 构建result_key到对象的映射字典
        for result in result_list:
            if result_key in result:
                key_to_dict[result[result_key]] = result

        # 遍历source_list,将匹配到的result对象合并进去
        for source in source_list:
            if source_key in source:
                key = source[source_key]
                if key in key_to_dict:
                    # 将匹配到的result对象的所有字段添加到source对象中
                    source.update(key_to_dict[key])

    return source_list


def clear_data(data_list, mapping):
    """
    仅保留data_list的每个元素里面mapping指定的字段，并根据mapping重命名字段

    Args:
        data_list: 数据列表
        mapping: 字段映射字典，格式为 {"原字段名": "新字段名"}

    Returns:
        清理后的数据列表
    """
    if not data_list or not isinstance(data_list, list):
        return data_list

    result = []
    for item in data_list:
        if not isinstance(item, dict):
            result.append(item)
            continue

        new_item = {}
        for old_key, new_key in mapping.items():
            if old_key in item:
                new_item[new_key] = item[old_key]
        result.append(new_item)

    return result


def export_to_excel(data_list, prefix="数据"):
    """
    将数据导出到Excel文件

    参数:
    data_list -- 要导出的数据列表
    prefix -- Excel文件名前缀
    """
    try:
        if data_list and len(data_list) > 0:
            df = pd.DataFrame(data_list)

            # 创建Excel文件
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            excel_filename = f"{prefix}_{timestamp}.xlsx"
            df.to_excel(excel_filename, index=False)
            return excel_filename
        else:
            return None
    except Exception as e:
        return None


def convert_to_csv(data_list):
    """
    将数据转换为CSV格式字符串

    参数:
    data_list -- 要转换的数据列表
    """
    try:
        if data_list and len(data_list) > 0:
            df = pd.DataFrame(data_list)
            csv_str = df.to_csv(index=False, encoding='utf-8')
            return csv_str
        else:
            return None
    except Exception as e:
        return None


def pd_to_csv(df):
    """
    将DataFrame转换为CSV格式字符串。
    Args:
        df (pd.DataFrame): 要转换的DataFrame。
    Returns:
        str: CSV格式字符串。
    """
    csv_str = df.to_csv(index=False, encoding='utf-8')
    return csv_str


def csv_to_pd(csv_str):
    """ 
    将CSV格式字符串转换为DataFrame。
    Args:
        csv_str (str): CSV格式字符串。
    Returns:
        pd.DataFrame: 转换后的DataFrame。   
    """
    buffer = StringIO(csv_str)
    df = pd.read_csv(buffer, sep=',')
    return df


def calculate_list_sum(df, column_name):
    """
    计算DataFrame中某个列表的和。

    Args:
        data_list (list): 要转换为DataFrame的数据列表。
        column_name (str): 要计算总和的列名。

    Returns:
        float或int: 该列的总和，如果出现异常则返回None。
    """
    try:
        if df is not None and column_name in df.columns:
            return df[column_name].sum()
        else:
            return 0
    except Exception as e:
        return 0


def calculate_list_mean(df, column_name):
    """
    计算DataFrame中某个列的平均值。

    Args:
        df (pd.DataFrame): 要处理的DataFrame。
        column_name (str): 要计算平均值的列名。

    Returns:
        float: 该列的平均值，如果出现异常则返回0。
    """
    try:
        if df is not None and column_name in df.columns:
            return df[column_name].mean()
        else:
            return 0
    except Exception as e:
        return 0


def calculate_list_median(df, column_name):
    """
    计算DataFrame中某个列的中位数。

    Args:
        df (pd.DataFrame): 要处理的DataFrame。
        column_name (str): 要计算中位数的列名。

    Returns:
        float: 该列的中位数，如果出现异常则返回0。
    """
    try:
        if df is not None and column_name in df.columns:
            return df[column_name].median()
        else:
            return 0
    except Exception as e:
        return 0


def group_and_aggregate(df, group_column, agg_column, agg_function='sum'):
    """
    按指定列对DataFrame进行分组，并对另一列进行聚合操作，形成新的DataFrame。

    Args:
        df (pd.DataFrame): 要处理的DataFrame。
        group_column (str): 用于分组的列名。
        agg_column (str): 用于聚合操作的列名。
        agg_function (str): 聚合函数，默认为 'sum'，可取值如 'mean', 'count', 'min', 'max' 等。

    Returns:
        pd.DataFrame: 分组聚合后的新DataFrame。
    """
    if group_column == agg_column:
        return None
    if df is not None and group_column in df.columns and agg_column in df.columns:
        if agg_function == 'sum':
            result = df.groupby(group_column)[agg_column].sum().reset_index()
        elif agg_function == 'mean':
            result = df.groupby(group_column)[agg_column].mean().reset_index()
        elif agg_function == 'count':
            result = df.groupby(group_column)[agg_column].count().reset_index()
        elif agg_function == 'min':
            result = df.groupby(group_column)[agg_column].min().reset_index()
        elif agg_function == 'max':
            result = df.groupby(group_column)[agg_column].max().reset_index()
        else:
            result = None
        return result
    else:
  
        return None


def calculate_columns_operation(df, col1, col2, operation='+'):
    """
    计算DataFrame中两列的和、差、积或商，并添加新列存储结果。

    Args:
        df (pd.DataFrame): 要处理的DataFrame。
        col1 (str): 参与运算的第一列的列名。
        col2 (str): 参与运算的第二列的列名。
        operation (str): 运算类型，可取值 '+', '-', '*', '/'，默认为 '+'。

    Returns:
        pd.DataFrame: 包含新计算列的DataFrame，如果出现异常则返回原始DataFrame。
    """
    try:
        column_name = f"{col1}{operation}{col2}"
        if df is not None and col1 in df.columns and col2 in df.columns:
            if operation == '+':
                df[column_name] = df[col1] + df[col2]
            elif operation == '-':
                df[column_name] = df[col1] - df[col2]
            elif operation == '*':
                df[column_name] = df[col1] * df[col2]
            elif operation == '/':
                df[column_name] = df[col1] / df[col2]
        return df
    except Exception as e:
        return df


def calculate_ratio(df, target_column):
    """
    计算DataFrame中某个列的占比，并添加新列存储结果。

    Args:
        df (pd.DataFrame): 要处理的DataFrame。
        target_column (str): 要计算占比的列名。

    Returns:
        pd.DataFrame: 包含占比列的DataFrame，如果出现异常则返回原始DataFrame。
    """
    try:
        column_name = f"{target_column}_占比"
        if df is not None and not df.empty and target_column in df.columns:
            total = df[target_column].sum()
            if total == 0:
                df[column_name] = 0.0
            else:
                df[column_name] = (df[target_column] / total * 100).round(2)
        return df
    except Exception as e:
        return df


def sort_data(df, column_name, ascending=True):
    """
    按指定列对DataFrame进行升序或降序排序。

    Args:
        df (pd.DataFrame): 要排序的DataFrame。
        column_name (str): 用于排序的列名。
        ascending (bool): 是否升序排序，默认为True（升序），False为降序。

    Returns:
        pd.DataFrame: 排序后的DataFrame，如果出现异常则返回原始DataFrame。
    """
    try:
        if df is not None and column_name in df.columns:
            sorted_df = df.sort_values(by=column_name, ascending=ascending)
            return sorted_df
        else:
            return df
    except Exception as e:
        return df


def read_har(har_file_path):
    """
    读取HAR文件并提取网络请求信息
    
    Args:
        har_file_path (str): HAR文件路径
        
    Returns:
        list: 包含请求信息的字典列表，每个字典包含url、method、postData、response字段
    """
    import json  # 导入json模块用于文件读取
    
    try:
        # 打开并读取HAR文件
        with open(har_file_path, 'r', encoding='utf-8') as file:
            # 解析HAR文件内容
            har_data = json.load(file)
        
        # 检查HAR文件结构是否正确
        if 'log' not in har_data:
            print("HAR文件格式错误：缺少log字段")
            return []
        
        # 获取log下的entries列表
        entries = har_data.get('log', {}).get('entries', [])
        
        # 检查entries是否为列表
        if not isinstance(entries, list):
            print("HAR文件格式错误：entries不是列表类型")
            return []
        
        # 存储提取的请求信息
        extracted_requests = []
        
        # 遍历entries列表
        for entry in entries:
            # 检查entry是否包含request和response字段
            if not isinstance(entry, dict):
                continue
                
            # 获取request和response对象
            request = entry.get('request')
            response = entry.get('response')
            
            # 检查request和response是否存在
            if not request or not response:
                continue
            
            # 获取请求方法
            method = request.get('method', '').upper()
            
            # 只处理GET和POST请求
            if method not in ['GET', 'POST']:
                continue
            
            # 提取请求信息
            request_info = {
                'url': request.get('url', ''),  # 请求URL
                'method': method,  # 请求方法
                'postData': '',  # POST数据
                'response': ''  # 响应内容
            }
            
            # 提取POST数据（如果存在）
            if method == 'POST' and 'postData' in request:
                post_data = request['postData']
                if isinstance(post_data, dict) and 'text' in post_data:
                    request_info['postData'] = post_data['text']
            
            # 提取响应内容
            if 'content' in response:
                content = response['content']
                if isinstance(content, dict) and 'text' in content:
                    request_info['response'] = content['text']
            
            # 添加到结果列表
            extracted_requests.append(request_info)
        
        # 打印提取结果统计
        print(f"成功从HAR文件中提取了 {len(extracted_requests)} 个请求")
        
        # 保存提取结果到JSON文件
        output_file = har_file_path.replace('.har', '_extracted.json')
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(extracted_requests, file, ensure_ascii=False, indent=4)
        
        print(f"提取结果已保存到: {output_file}")
        
        # 返回提取的请求信息列表
        return extracted_requests
        
    except FileNotFoundError:
        # 文件不存在异常处理
        print(f"HAR文件未找到: {har_file_path}")
        return []
    except json.JSONDecodeError:
        # JSON解析异常处理
        print(f"HAR文件格式错误，无法解析JSON: {har_file_path}")
        return []
    except Exception as e:
        # 其他异常处理
        print(f"读取HAR文件时发生错误: {str(e)}")
        return []


def transform_json(json_file_path):
    """
    读取JSON文件中的gridCols列表，将colFieldName作为键，systemColName作为值形成字典

    Args:
        json_file_path (str): JSON文件路径

    Returns:
        dict: 转换后的字典，如果出现异常则返回空字典
    """
    import json  # 导入json模块用于文件读取

    try:
        # 打开并读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            # 解析JSON数据
            data = json.load(file)

        # 检查是否存在gridCols字段
        if 'gridCols' not in data:
            print(f"JSON文件中未找到gridCols字段")
            return {}

        # 获取gridCols列表
        grid_cols = data['gridCols']

        # 检查gridCols是否为列表
        if not isinstance(grid_cols, list):
            print(f"gridCols不是列表类型")
            return {}

        # 创建结果字典
        result_dict = {}

        # 遍历gridCols列表
        for col in grid_cols:
            # 检查每个元素是否为字典且包含必要字段
            if isinstance(col, dict) and 'colFieldName' in col and 'systemColName' in col:
                # 以colFieldName为键，systemColName为值
                result_dict[col['colFieldName']] = col['systemColName']

        # 打印处理结果
        print(result_dict)
        # 保存到文件
        output_file_path = json_file_path.replace('.json', '_transformed.json')
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=4)

        # 生成测试网页版
        _generate_test_html(result_dict, json_file_path)

        # 返回转换后的字典
        return ",".join(result_dict.values())

    except FileNotFoundError:
        # 文件不存在异常处理
        print(f"文件未找到: {json_file_path}")
        return {}
    except json.JSONDecodeError:
        # JSON解析异常处理
        print(f"JSON文件格式错误: {json_file_path}")
        return {}
    except Exception as e:
        # 其他异常处理
        print(f"处理JSON文件时发生错误: {str(e)}")
        return {}


def json_to_csv(data_list, column_mapping):
    """
    将列表数据转换为CSV格式字符串，使用字典映射列名，去除全空列和重复列

    Args:
        data_list (list): 要转换的数据列表
        column_mapping (dict): 列名映射字典，键为数据中的字段名，值为CSV中的列名

    Returns:
        str: CSV格式字符串，如果出现异常则返回空字符串
    """
    import csv  # 导入csv模块用于CSV处理
    from io import StringIO  # 导入StringIO用于字符串缓冲

    try:
        # 检查输入参数有效性
        if not data_list or not isinstance(data_list, list):
            print("数据列表为空或不是列表类型")
            return ""

        # 检查字典映射有效性
        if not column_mapping or not isinstance(column_mapping, dict):
            print("列名映射字典为空或不是字典类型")
            return ""

        # 去除重复的列名映射
        unique_mapping = {}
        seen_values = set()
        for key, value in column_mapping.items():
            # 如果列名未出现过，则保留
            if value not in seen_values:
                unique_mapping[key] = value
                seen_values.add(value)

        # 收集所有行数据用于检测空列
        all_rows = []

        # 遍历数据列表收集数据
        for item in data_list:
            # 检查每个数据项是否为字典
            if not isinstance(item, dict):
                continue

            # 创建CSV行数据
            csv_row = {}

            # 根据去重后的映射字典转换数据
            for source_key, csv_column in unique_mapping.items():
                # 从数据项中获取值
                if source_key in item:
                    csv_row[csv_column] = item[source_key]
                else:
                    # 如果字段不存在，设置为空字符串
                    csv_row[csv_column] = ""

            # 添加到所有行数据中
            all_rows.append(csv_row)

        # 检测并去除全空列
        if all_rows:
            # 获取所有列名
            all_columns = list(unique_mapping.values())

            # 检测每列是否全为空
            non_empty_columns = []
            for column in all_columns:
                # 检查该列是否有非空值
                has_non_empty = any(
                    str(row.get(column) or "").strip() != ""
                    for row in all_rows
                )
                # 如果有非空值，保留该列
                if has_non_empty:
                    non_empty_columns.append(column)

            # 创建字符串缓冲区
            output = StringIO()

            # 创建CSV写入器（仅使用非空列）
            writer = csv.DictWriter(output, fieldnames=non_empty_columns)

            # 写入CSV头部
            writer.writeheader()

            # 写入数据行（仅包含非空列）
            for row in all_rows:
                # 过滤出非空列的数据
                filtered_row = {col: row.get(col, "")
                                for col in non_empty_columns}
                writer.writerow(filtered_row)

            # 获取CSV字符串
            csv_string = output.getvalue()

            # 关闭字符串缓冲区
            output.close()

            # 返回CSV字符串
            return csv_string
        else:
            # 没有有效数据
            print("没有有效数据可转换")
            return ""

    except Exception as e:
        # 异常处理
        print(f"转换CSV时发生错误: {str(e)}")
        return ""


def get_csv_header(csv_string):
    """
    从CSV格式字符串中提取列名列表

    Args:
        csv_string (str): CSV格式字符串

    Returns:
        header(str): 列名列表
    """
    import csv  # 导入csv模块用于CSV处理
    from io import StringIO  # 导入StringIO用于字符串缓冲

    try:
        # 检查输入参数有效性
        if not csv_string or not isinstance(csv_string, str):
            print("CSV字符串为空或不是字符串类型")
            return []

        # 创建字符串缓冲区
        input_buffer = StringIO(csv_string)

        # 创建CSV读取器
        csv_reader = csv.reader(input_buffer)

        # 读取第一行作为列名
        try:
            header_row = next(csv_reader)
            # 去除列名中的空白字符
            headers = [header.strip() for header in header_row]

            # 关闭字符串缓冲区
            input_buffer.close()

            # 返回列名列表
            return ",".join(headers)

        except StopIteration:
            # CSV为空或没有数据行
            print("CSV字符串为空或没有数据")
            input_buffer.close()
            return []

    except Exception as e:
        # 异常处理
        print(f"提取CSV列名时发生错误: {str(e)}")
        return []


def list_to_csv(data_list):
    """
    将列表数据转换为CSV格式字符串

    Args:
        data_list (list): 要转换的数据列表，支持以下格式：
                         - 字典列表：[{"name": "张三", "age": 25}, {"name": "李四", "age": 30}]
                         - 二维列表：[["name", "age"], ["张三", 25], ["李四", 30]]
                         - 简单列表：["张三", "李四", "王五"]

    Returns:
        str: CSV格式字符串，如果出现异常则返回空字符串
    """
    import csv  # 导入csv模块用于CSV处理
    from io import StringIO  # 导入StringIO用于字符串缓冲

    try:
        # 检查输入参数有效性
        if not data_list or not isinstance(data_list, list):
            print("数据列表为空或不是列表类型")  # 打印错误信息
            return ""  # 返回空字符串

        # 如果列表为空，返回空字符串
        if len(data_list) == 0:
            print("数据列表为空")  # 打印提示信息
            return ""  # 返回空字符串

        # 创建字符串缓冲区
        output = StringIO()  # 创建字符串输出缓冲区

        # 判断数据类型并处理
        if isinstance(data_list[0], dict):
            # 处理字典列表格式
            fieldnames = list(data_list[0].keys())  # 获取字典的键作为列名
            writer = csv.DictWriter(output, fieldnames=fieldnames)  # 创建字典CSV写入器
            writer.writeheader()  # 写入CSV头部
            writer.writerows(data_list)  # 写入所有数据行

        elif isinstance(data_list[0], (list, tuple)):
            # 处理二维列表格式
            writer = csv.writer(output)  # 创建CSV写入器
            writer.writerows(data_list)  # 写入所有数据行

        else:
            # 处理简单列表格式，转换为单列CSV
            writer = csv.writer(output)  # 创建CSV写入器
            for item in data_list:  # 遍历列表中的每个元素
                writer.writerow([item])  # 将每个元素作为单独的行写入

        # 获取CSV字符串
        csv_string = output.getvalue()  # 获取缓冲区中的CSV字符串

        # 关闭字符串缓冲区
        output.close()  # 关闭缓冲区释放资源

        # 返回CSV字符串
        return csv_string  # 返回生成的CSV字符串

    except Exception as e:
        # 异常处理
        print(f"转换CSV时发生错误: {str(e)}")  # 打印错误信息
        return ""  # 返回空字符串


def set_csv_header(csv_string, column_list):
    """
    根据列名列表过滤CSV，保留指定列，删除其他列

    Args:
        csv_string (str): CSV格式的字符串
        column_list (list): 要保留的列名列表

    Returns:
        str: 过滤后的CSV格式字符串，如果出现异常则返回空字符串
    """
    import csv  # 导入csv模块用于CSV处理
    from io import StringIO  # 导入StringIO用于字符串缓冲

    try:
        # 检查输入参数有效性
        if not csv_string or not isinstance(csv_string, str):
            print("CSV字符串为空或不是字符串类型")
            return ""

        # 检查列名列表有效性
        if not column_list or not isinstance(column_list, list):
            print("列名列表为空或不是列表类型")
            return ""

        # 创建输入字符串缓冲区
        input_buffer = StringIO(csv_string)

        # 创建CSV读取器
        reader = csv.DictReader(input_buffer)

        # 获取原始列名
        original_headers = reader.fieldnames
        if not original_headers:
            print("CSV中没有找到列名")
            input_buffer.close()
            return ""

        # 过滤出存在的列名
        valid_columns = [col for col in column_list if col in original_headers]
        if not valid_columns:
            print("指定的列名在CSV中都不存在")
            input_buffer.close()
            return ""

        # 创建输出字符串缓冲区
        output_buffer = StringIO()

        # 创建CSV写入器（仅使用有效列）
        writer = csv.DictWriter(output_buffer, fieldnames=valid_columns)

        # 写入CSV头部
        writer.writeheader()

        # 读取并写入数据行（仅保留指定列）
        for row in reader:
            # 过滤出指定列的数据
            filtered_row = {col: row.get(col, "") for col in valid_columns}
            writer.writerow(filtered_row)

        # 获取过滤后的CSV字符串
        result_csv = output_buffer.getvalue()

        # 关闭字符串缓冲区
        input_buffer.close()
        output_buffer.close()

        # 返回过滤后的CSV字符串
        return result_csv

    except Exception as e:
        # 异常处理
        print(f"过滤CSV列时发生错误: {str(e)}")
        return ""

def send_supubase(image_content: str,  bucket: str = None)->dict:
    supabase_manager = SupabaseManager()
    return supabase_manager.upload_base64(bucket, image_content)

def send_qiniu(image_content: str, filename: str = None) -> dict:
    """
    上传图片到七牛云存储

    Args:
        image_content (str): 图片内容，可以是base64编码或文件路径
        filename (str): 可选的文件名，如果不提供则自动生成

    Returns:
        dict: 包含上传结果的字典，格式为 {"success": bool, "url": str, "error": str}
    """
    try:
        # 获取七牛云配置
        access_key = os.getenv('QINIU_ACCESS_KEY')  # 获取Access Key
        secret_key = os.getenv('QINIU_SECRET_KEY')  # 获取Secret Key
        bucket_name = os.getenv('QINIU_BUCKET_NAME')  # 获取存储空间名称
        domain = os.getenv('QINIU_DOMAIN')  # 获取域名

        # 检查配置是否完整
        if not all([access_key, secret_key, bucket_name]):  # 验证必要配置
            return {
                "success": False,
                "url": "",
                "error": "七牛云配置不完整，请检查环境变量"
            }

        # 构建鉴权对象
        q = Auth(access_key, secret_key)  # 创建认证对象

        # 生成文件名
        if not filename:  # 如果没有提供文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # 生成时间戳
            unique_id = str(uuid.uuid4())[:8]  # 生成短UUID
            filename = f"chart_{timestamp}_{unique_id}.png"  # 组合文件名

        # 生成上传Token
        token = q.upload_token(bucket_name, filename, 3600)  # 生成1小时有效期的token

        # 处理图片内容
        if image_content.startswith('data:image/'):  # 如果是base64格式
            # 去掉data:image/png;base64,前缀
            base64_data = image_content.split(',')[1]  # 提取base64数据
            image_data = base64.b64decode(base64_data)  # 解码为二进制数据

            # 直接上传二进制数据
            ret, info = put_data(token, filename, image_data)  # 上传数据到七牛云

        elif os.path.isfile(image_content):  # 如果是文件路径
            # 上传本地文件
            ret, info = put_file(token, filename, image_content)  # 上传文件到七牛云

        else:  # 如果是原始二进制数据
            # 假设是二进制数据
            ret, info = put_data(token, filename, image_content.encode(
            ) if isinstance(image_content, str) else image_content)  # 上传数据

        # 检查上传结果
        if info.status_code == 200:  # 上传成功
            # 构建图片URL
            if domain:  # 如果配置了域名
                image_url = f"{domain.rstrip('/')}/{filename}"  # 组合完整URL
            else:  # 如果没有配置域名
                # 使用默认域名格式
                image_url = f"http://your-bucket.qiniudn.com/{filename}"

            return {
                "success": True,
                "url": image_url,
                "filename": filename,
                "error": ""
            }
        else:  # 上传失败
            return {
                "success": False,
                "url": "",
                "error": f"上传失败，状态码: {info.status_code}, 错误信息: {info.text_body}"
            }

    except Exception as e:  # 捕获异常
        return {
            "success": False,
            "url": "",
            "error": f"上传失败: {str(e)}"
        }


def jsons_to_json(json_file1_path, json_file2_path, output_file_path):
    """
    合并两个JSON文件，相同键使用第一个JSON的值，合并后保存为新JSON文件

    Args:
        json_file1_path (str): 第一个JSON文件路径（优先级高）
        json_file2_path (str): 第二个JSON文件路径
        output_file_path (str): 输出JSON文件路径

    Returns:
        dict: 包含操作结果的字典，格式为 {"success": bool, "message": str, "data": dict}
    """
    import json  # 导入json模块用于文件读写

    try:
        # 读取第一个JSON文件
        try:
            with open(json_file1_path, 'r', encoding='utf-8') as file1:  # 打开第一个JSON文件
                json1_data = json.load(file1)  # 解析JSON数据
        except FileNotFoundError:
            return {
                "success": False,
                "message": f"第一个JSON文件未找到: {json_file1_path}",
                "data": {}
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": f"第一个JSON文件格式错误: {json_file1_path}",
                "data": {}
            }

        # 读取第二个JSON文件
        try:
            with open(json_file2_path, 'r', encoding='utf-8') as file2:  # 打开第二个JSON文件
                json2_data = json.load(file2)  # 解析JSON数据
        except FileNotFoundError:
            return {
                "success": False,
                "message": f"第二个JSON文件未找到: {json_file2_path}",
                "data": {}
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": f"第二个JSON文件格式错误: {json_file2_path}",
                "data": {}
            }

        # 检查两个JSON数据是否都是字典类型
        if not isinstance(json1_data, dict):  # 验证第一个JSON是否为字典
            return {
                "success": False,
                "message": "第一个JSON文件根节点不是对象类型",
                "data": {}
            }

        if not isinstance(json2_data, dict):  # 验证第二个JSON是否为字典
            return {
                "success": False,
                "message": "第二个JSON文件根节点不是对象类型",
                "data": {}
            }

        # 合并JSON数据，第一个JSON的值优先
        merged_data = {}  # 创建合并后的数据字典

        # 先添加第二个JSON的所有键值对
        for key, value in json2_data.items():  # 遍历第二个JSON的键值对
            merged_data[key] = value  # 添加到合并数据中

        # 再添加第一个JSON的键值对，覆盖相同的键
        for key, value in json1_data.items():  # 遍历第一个JSON的键值对
            merged_data[key] = value  # 添加到合并数据中（会覆盖相同键）

        # 保存合并后的JSON文件
        try:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:  # 创建输出文件
                json.dump(merged_data, output_file,
                          ensure_ascii=False, indent=4)  # 写入合并后的数据
        except Exception as save_error:
            return {
                "success": False,
                "message": f"保存合并文件失败: {str(save_error)}",
                "data": {}
            }

        # 返回成功结果
        return {
            "success": True,
            "message": f"成功合并JSON文件，输出到: {output_file_path}",
            "data": merged_data
        }

    except Exception as e:
        # 异常处理
        return {
            "success": False,
            "message": f"合并JSON文件时发生错误: {str(e)}",
            "data": {}
        }


if __name__ == "__main__":
    print(transform_json(
        "E:\\tx-erp\\erp-backend\\api\\erp_production_schedule_list_v2.json"))
