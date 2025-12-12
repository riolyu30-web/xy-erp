from fastmcp import FastMCP  # 导入FastMCP框架
import services.tool as tool  # 导入工具模块
from services.cache import cache_load, cache_save  # 导入缓存服务
import pandas as pd  # 导入Pandas库

csv_mcp = FastMCP(name="csv")  # 创建计算服务MCP实例


@csv_mcp.tool()
def get_data(token: str) -> str:
    """
    获取所有行，仅保留有效字段，用于最终数据分析
    Args:
        token: 表令牌或结果令牌   
    Returns:
        result(str): 当前计算的结果CSV格式。
    """
    data_list = cache_load(token)  # 从缓存加载数据     
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息   
    # 过滤CSV列，只保留非英文字母和数字组成的列名
    
    if data_list:
        df = tool.csv_to_pd(data_list)
        # 筛选列名：仅保留由非英文字母和数字组成的列
        filtered_columns = [col for col in df.columns if not (str(col).isalnum() and str(col).isascii())]
        df = df[filtered_columns]
        data_list = tool.pd_to_csv(df)
    
    return data_list  # 转换为CSV格式返回

@csv_mcp.tool()
def get_sample(token: str) -> str:
    """
    获取全部字段与前三条数据样本，用于确认字段是否正确
    Args:
        token: 表令牌或结果令牌   
    Returns:
        result(str): 当前计算的结果CSV格式样本
    """
    data_list = cache_load(token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息   
    # 过滤CSV列，只保留非英文字母和数字组成的列名
    
    if data_list:
        lines = data_list.splitlines()
        if len(lines) > 3:
            lines = lines[:3]
        data_list = "\n".join(lines)
    
    return data_list  # 转换为CSV格式返回

@csv_mcp.tool()
def group_aggregate(token: str, group_column: str, agg_column: str, agg_function: str = "sum") -> str:
    """
    按指定列分组并对另一列进行聚合计算。
    Args:
        token: 表令牌或结果令牌   
        group_column (str): 分组列名。
        agg_column (str): 聚合列名。
        agg_function (str): 聚合函数,可选值,sum, mean, count, min, max。
    Returns:
        result_token: 成功返回分组聚合结果令牌/ error失败
    """
    data_list = cache_load(token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.group_and_aggregate(
        df, group_column, agg_column, agg_function)  # 执行分组聚合
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        key = "分组聚合结果_" + token
        cache_save(key, csv_result)  # 缓存保存结果
        return key
    return "error"  # 返回错误信息


@csv_mcp.tool()
def add_operation_column(token: str, col1: str, col2: str, operation: str = "+") -> str:
    """
    计算两列之间的运算并添加新列。
    Args:
        token: 表令牌或结果令牌   
        col1 (str): 第一列名。
        col2 (str): 第二列名。
        operation (str): 运算符，可选值：+, -, *, /。
    Returns:
        result_token: 成功返回运算结果令牌/ error失败
    """
    data_list = cache_load(token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.calculate_columns_operation(
        df, col1, col2, operation)  # 执行列运算
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        key = "运算结果_" + token
        cache_save(key, csv_result)  # 缓存保存结果
        return key
    return "error"  # 返回错误信息


@csv_mcp.tool()
def add_ratio_column(token: str, target_column: str) -> str:
    """
    计算某列的占比并添加新列。
    Args:
        token: 表令牌
        target_column (str): 目标列名。
    Returns:
        result_token: 成功返回占比结果令牌/ error失败
    """
    data_list = cache_load(token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 将CSV字符串转换为DataFrame
    result_df = tool.calculate_ratio(df, target_column)  # 执行比例计算
    if result_df is not None:  # 检查结果是否有效
        csv_result = tool.pd_to_csv(result_df)  # 将DataFrame转换为CSV字符串
        key = "占比结果_" + token
        cache_save(key, csv_result)  # 缓存保存结果
        return key
    return "error"  # 返回错误信息


@csv_mcp.tool()
def sort_data(token: str, column_name: str, ascending: bool = True) -> str:
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
        result_token: 成功返回合并后的结果令牌/ error失败
    """
    data_csv = cache_load(token)  # 从缓存加载CSV数据             
    if not data_csv or selected_column_list == "":  # 检查数据是否存在
        return "error"  # 返回错误信息
    column_list = selected_column_list.split(",")  # 转换为列表
    # 调用工具函数过滤CSV列
    filtered_csv = tool.set_csv_header(data_csv, column_list)
    if filtered_csv:  # 检查过滤结果是否有效
        key = "过滤结果_" + token
        cache_save(key, filtered_csv)  # 缓存保存过滤后的结果
        return key  # 返回成功
    return "error"  # 返回错误信息

@csv_mcp.tool()
def merge_data(token1: str, token2: str ) -> str:
    """
    合并两个表的数据，用于多维度交叉分析
    Args:
        token1: 第一个表令牌/结果令牌，主表
        token2: 第二个表令牌/结果令牌，从表
    Returns:
        result_token: 成功返回合并后的结果令牌/ error失败
    """
    data_csv1 = cache_load(token1)  # 从缓存加载第一个表的CSV数据
    data_csv2 = cache_load(token2)  # 从缓存加载第二个表的CSV数据
    if not data_csv1 or not data_csv2:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df1 = tool.csv_to_pd(data_csv1)  # 将第一个表的CSV字符串转换为DataFrame
    df2 = tool.csv_to_pd(data_csv2)  # 将第二个表的CSV字符串转换为DataFrame
    
    # 自动推断关联键并合并
    sample_size = 10
    d1 = df1.sample(min(sample_size, len(df1))) if len(df1) > sample_size else df1 
    d2 = df2.sample(min(sample_size, len(df2))) if len(df2) > sample_size else df2 
 
    # 暴力比对每一列的内容 
    possible_matches = [] 
    for c1 in d1.columns: 
        # 跳过全是空的列 
        if d1[c1].dtype == object or pd.api.types.is_numeric_dtype(d1[c1]): 
            # 跳出不是Id结尾的列，或包含特定关键词的列
            if not c1.endswith("Id") or "Updater" in c1 or "Creator" in c1 or "Tenant" in c1 or "Parent" in c1:
                continue

            set1 = set(d1[c1].dropna().astype(str)) 
            if not set1: continue 
            
            for c2 in d2.columns: 
                # 跳出不是Id结尾的列，或包含特定关键词的列
                if not c2.endswith("Id") or "Updater" in c2 or "Creator" in c2 or "Tenant" in c2 or "Parent" in c2:
                    continue

                set2 = set(d2[c2].dropna().astype(str)) 
                if not set2: continue 
                
                # 计算交集（重合的部分） 
                intersection = len(set1 & set2) 
                # 如果重合度很高（比如超过较小集合的 50%） 
                if intersection > 0: 
                    ratio = intersection / min(len(set1), len(set2)) 
                    if ratio > 0.5: # 门槛可以自己调，0.5代表有一半数据是对得上的 
                        possible_matches.append({ 
                            "left_on": c1, 
                            "right_on": c2, 
                            "ratio": ratio
                        }) 
    
    # 执行合并
    if possible_matches:
        # 按重合度排序取最佳匹配
        best_match = sorted(possible_matches, key=lambda x: x['ratio'], reverse=True)[0]
        print(possible_matches)
        # 使用找到的最佳关联键进行合并，使用左连接保留主表数据
        df = pd.merge(df1, df2, left_on=best_match['left_on'], right_on=best_match['right_on'], how='left')
     
        csv_string = tool.pd_to_csv(df)

        if csv_string:
            # 构造新的 key
            key = f"合并结果_{token1}"          
            if cache_save(key, csv_string):
                return key # 返回生成的 key
    else:
        return "error"

