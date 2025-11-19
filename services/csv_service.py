from fastmcp import FastMCP  # 导入FastMCP框架
import services.tool as tool  # 导入工具模块
from services.cache import cache_load, cache_save  # 导入缓存服务

csv_mcp = FastMCP(name="csv")  # 创建计算服务MCP实例


@csv_mcp.tool()
def get_data(access_token: str) -> str:
    """
    获取最终计算结果
    Args:
        access_token: 访问令牌
    Returns:
        result(str): 当前计算的结果CSV格式。
    """
    data_list = cache_load(access_token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    return data_list  # 转换为CSV格式返回


@csv_mcp.tool()
def group_aggregate(access_token: str, group_column: str, agg_column: str, agg_function: str = "sum") -> str:
    """
    按指定列分组并对另一列进行聚合计算。
    Args:
        access_token: 访问令牌
        group_column (str): 分组列名。
        agg_column (str): 聚合列名。
        agg_function (str): 聚合函数,可选值,sum, mean, count, min, max。
    Returns:
        result(str): success成功,调用csv_get_data获取结果 / error失败
    """
    data_list = cache_load(access_token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.group_and_aggregate(
        df, group_column, agg_column, agg_function)  # 执行分组聚合
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        cache_save(access_token, csv_result)  # 缓存保存结果
        return "success"
    return "error"  # 返回错误信息


@csv_mcp.tool()
def add_operation_column(access_token: str, col1: str, col2: str, operation: str = "+") -> str:
    """
    计算两列之间的运算并添加新列。
    Args:
        access_token: 访问令牌
        col1 (str): 第一列名。
        col2 (str): 第二列名。
        operation (str): 运算符，可选值：+, -, *, /。
    Returns:
        result(str): success成功,调用csv_get_data获取结果 / error失败
    """
    data_list = cache_load(access_token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.calculate_columns_operation(
        df, col1, col2, operation)  # 执行列运算
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        cache_save(access_token, csv_result)  # 缓存保存结果
        return "success"
    return "error"  # 返回错误信息


@csv_mcp.tool()
def add_ratio_column(access_token: str, target_column: str) -> str:
    """
    计算某列的占比并添加新列。
    Args:
        access_token: 访问令牌
        target_column (str): 目标列名。
    Returns:
        result(str): success成功,调用csv_get_data获取结果 / error失败
    """
    data_list = cache_load(access_token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.calculate_ratio(df, target_column)  # 执行比例计算
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        cache_save(access_token, csv_result)  # 缓存保存结果
        return "success"
    return "error"  # 返回错误信息


@csv_mcp.tool()
def sort_data(access_token: str, column_name: str, ascending: bool = True) -> str:
    """
    按指定列对数据进行排序。
    Args:
        access_token: 访问令牌
        column_name (str): 排序列名。
        ascending (bool): 是否升序排序，默认True。
    Returns:
        result(str): success成功,调用csv_get_data获取结果 / error失败
    """
    data_list = cache_load(access_token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.sort_data(df, column_name, ascending)  # 执行排序
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        cache_save(access_token, csv_result)  # 缓存保存结果
        return "success"
    return "error"  # 返回错误信息


@csv_mcp.tool()
def filter_data(access_token: str, selected_column_list: str) -> str:
    """
    选择保留的列名过滤CSV数据，仅保留指定列，以便更直观
    Args:
        access_token: 访问令牌
        selected_column_list (str): 选择保留的列名列表,用,隔开,例如:审核状态,订单状态,订单号
    Returns:
        result(str): success成功,调用get_data获取结果 / error失败
    """
    data_csv = cache_load(access_token)  # 从缓存加载CSV数据
    if not data_csv or selected_column_list is "":  # 检查数据是否存在
        return "error"  # 返回错误信息
    column_list = selected_column_list.split(",")  # 转换为列表
    # 调用工具函数过滤CSV列
    filtered_csv = tool.set_csv_header(data_csv, column_list)
    if filtered_csv:  # 检查过滤结果是否有效
        cache_save(access_token, filtered_csv)  # 缓存保存过滤后的结果
        return "success"  # 返回成功
    return "error"  # 返回错误信息
