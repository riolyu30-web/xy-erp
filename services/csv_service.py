from fastmcp import FastMCP  # 导入FastMCP框架
import services.tool as tool  # 导入工具模块
from services.cache import cache_load, cache_save  # 导入缓存服务
import pandas as pd  # 导入Pandas库

csv_mcp = FastMCP(name="csv")  # 创建计算服务MCP实例


@csv_mcp.tool()
def get_data(token: str) -> dict:
    """
    获取所有行，仅保留有效字段，用于最终数据分析
    Args:
        token: 表令牌或结果令牌   
    Returns:
        success: 成功返回所有有效数据行/ error: 失败原因
    """
    data_list = cache_load(token)  # 从缓存加载数据     
    if not data_list:  # 检查数据是否存在
        return {"error": "数据不存在，可能是缓存过期"}  # 返回错误信息   
    else:
        lines = data_list.splitlines()  # 按行分割数据
        if "结果" in token:
            count = len(lines) - 1  # 计算有效数据行            
            if count > 30:
                return {"sample": "\n".join(lines[:30]),"tips":f"仅返回前30条数据做参考，共{count}条有效数据"}  # 返回有效数据样本
            elif count == 0:
                return {"error": "结果数据为空"}  # 返回错误信息
            else:
                return "\n".join(lines)  # 返回有效数据样本
        else:
            return {"sample": "\n".join(lines[:5]),"tips":"仅返回前5条数据做参考,请执行数据运算后查看"}  # 5条有效字段数据样本


@csv_mcp.tool()
def get_sample(token: str) -> dict:
    """
    获取全部字段与前三条数据样本，用于确认字段是否正确
    Args:
        token: 表令牌或结果令牌   
    Returns:
        success: 成功返回所有有效字段数据样本/ error: 失败原因
    """
    data_list = cache_load(token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return {"error": "数据不存在，可能是缓存过期"}  # 返回错误信息
    else:
        return {"sample": "\n".join(data_list.splitlines()[:5])}  # 5条有效字段数据样本 

@csv_mcp.tool()
def group_aggregate(token: str, group_column: str, agg_column: str, agg_function: str = "sum") -> dict:
    """
    按指定列分组并对另一列进行聚合计算。
    Args:
        token: 表令牌或结果令牌   
        group_column (str): 分组列名。
        agg_column (str): 聚合列名。
        agg_function (str): 聚合函数,可选值,sum, mean, count, min, max。
    Returns:
        success: 成功返回分组聚合结果令牌/ error: 失败原因
    """
    data_list = cache_load(token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return {"error": "数据不存在，可能是缓存过期"}  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.group_and_aggregate(
        df, group_column, agg_column, agg_function)  # 执行分组聚合
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        key = "分组聚合结果_" + token
        cache_save(key, csv_result)  # 缓存保存结果
        return {"success": key}  # 返回分组聚合结果令牌
    return {"error": "分组聚合失败"}  # 返回错误信息


@csv_mcp.tool()
def add_operation_column(token: str, col1: str, col2: str, operation: str = "+") -> dict:
    """
    计算两列之间的运算并添加新列。
    Args:
        token: 表令牌或结果令牌   
        col1 (str): 第一列名。
        col2 (str): 第二列名。
        operation (str): 运算符，可选值：+, -, *, /。
    Returns:
        success: 成功返回运算结果令牌/ error: 失败原因
    """
    data_list = cache_load(token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return {"error": "数据不存在，可能是缓存过期"}  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.calculate_columns_operation(
        df, col1, col2, operation)  # 执行列运算
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        key = "运算结果_" + token
        cache_save(key, csv_result)  # 缓存保存结果
        return {"success": key}  # 返回运算结果令牌
    return {"error": "运算失败"}  # 返回错误信息


@csv_mcp.tool()
def add_ratio_column(token: str, target_column: str) -> dict:
    """
    计算某列的占比并添加新列。
    Args:
        token: 表令牌
        target_column (str): 目标列名。
    Returns:
        success: 成功返回占比结果令牌/ error: 失败原因
    """
    data_list = cache_load(token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return {"error": "数据不存在，可能是缓存过期"}  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.calculate_ratio(df, target_column)  # 执行比例计算
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        key = "占比结果_" + token
        cache_save(key, csv_result)  # 缓存保存结果
        return {"success": key}  # 返回占比结果令牌
    return {"error": "占比计算失败"}  # 返回错误信息


@csv_mcp.tool()
def sort_data(token: str, column_name: str, ascending: bool = True) -> dict:
    """
    按指定列对数据进行排序。
    Args:
        token: 表令牌/结果令牌
        column_name (str): 排序列名。
        ascending (bool): 是否升序排序，默认True。
    Returns:
        result_token: 成功返回排序后的结果令牌/ error失败
    """
    data_list = cache_load(token)  # 从缓存加载数据           
    if not data_list:  # 检查数据是否存在   
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.sort_data(df, column_name, ascending)  # 执行排序
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        key = "排序结果_" + token
        cache_save(key, csv_result)  # 缓存保存结果
        return key
    return "error"  # 返回错误信息


@csv_mcp.tool()
def filter_data(token: str, selected_column_list: str) -> str:
    """
    选择保留的列名过滤CSV数据，仅保留指定列，以便更直观
    Args:
        token: 表令牌/结果令牌
        selected_column_list (str): 选择保留的列名列表,用,隔开,例如:审核状态,订单状态,订单号
    Returns:
        success: 成功返回过滤后的结果令牌/ error: 失败原因
    """
    data_csv = cache_load(token)  # 从缓存加载CSV数据             
    if not data_csv or selected_column_list == "":  # 检查数据是否存在
        return {"error": "数据不存在或未指定列名"}  # 返回错误信息
    column_list = selected_column_list.split(",")  # 转换为列表
    # 调用工具函数过滤CSV列
    filtered_csv = tool.set_csv_header(data_csv, column_list)
    if filtered_csv:  # 检查过滤结果是否有效
        key = "过滤结果_" + token
        cache_save(key, filtered_csv)  # 缓存保存过滤后的结果
        return {"success": key}  # 返回成功
    return {"error":"过滤数据失败,请尝试其他接口"}  # 返回错误信息  

@csv_mcp.tool()
def merge_data(token_left: str, token_right: str,key_left: str,key_right: str) -> str:
    """
    合并两个表的数据，用于多维度交叉分析
    Args:
        token_left: 主表令牌/结果令牌
        token_right: 从表令牌/结果令牌
        key_left: 主表关联键列名
        key_right: 从表关联键列名
    Returns:
        success: 成功返回合并后的结果令牌/ error: 失败原因
    """
    data_csv1 = cache_load(token_left) 
    if not data_csv1:  # 检查数据是否存在
        return {"error":"主表数据不存在，请提供其他主表令牌"}  # 返回错误信息
    data_csv2 = cache_load(token_right)  # 从缓存加载第二个表的CSV数据
    if not data_csv2:  # 检查数据是否存在
        return {"error":"从表数据不存在，请提供其他从表令牌"}  # 返回错误信息
    df1 = tool.csv_to_pd(data_csv1)  # 将第一个表的CSV字符串转换为DataFrame
    df2 = tool.csv_to_pd(data_csv2)  # 将第二个表的CSV字符串转换为DataFrame

     # 使用找到的最佳关联键进行合并，使用左连接保留主表数据
    df = pd.merge(df1, df2, left_on=key_left, right_on=key_right, how='left')
    df = df.dropna(axis='columns', how='all') # 删除所有值都为空的列  
    if df.empty:
        return {"error": "没有数据，请尝试其他接口"}

    csv_string = tool.pd_to_csv(df)

    if csv_string:
        # 构造新的 key
        key = f"合并结果_{token_left}"          
        if cache_save(key, csv_string):
            return {"success": key} # 返回生成的 key
    else:
        return {"error":"合并数据失败,请尝试其他接口"}

