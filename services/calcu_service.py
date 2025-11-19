from fastmcp import FastMCP  # 导入FastMCP框架
import services.tool as tool  # 导入工具模块
from services.cache import cache_load  # 导入缓存服务
import pandas as pd  # 导入pandas数据处理库
from datetime import datetime  # 导入日期时间模块

calcu_mcp = FastMCP(name="calcu")  # 创建计算服务MCP实例


@calcu_mcp.tool()
def column_sum(access_token: str, column_name: str) -> str:
    """
    计算数据中某列的和。
    Args:
        access_token: 访问令牌
        column_name (str): 需要统计的列名。
    Returns:
        result (str): 数据某列的和。
    """
    data_list = cache_load(access_token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 转换为DataFrame
    result = tool.calculate_list_sum(df, column_name)  # 计算列的和
    return str(result)  # 返回结果字符串


@calcu_mcp.tool()
def column_mean(access_token: str, column_name: str) -> str:
    """
    计算数据中某列的平均值。
    Args:
        access_token: 访问令牌
        column_name (str): 需要统计的列名。
    Returns:
        result (str): 数据某列的平均值。
    """
    data_list = cache_load(access_token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 转换为DataFrame
    result = tool.calculate_list_mean(df, column_name)  # 计算列的平均值
    return str(result)  # 返回结果字符串


@calcu_mcp.tool()
def column_median(access_token: str, column_name: str) -> str:
    """
    计算数据中某列的中位数。
    Args:
        access_token: 访问令牌
        column_name (str): 需要统计的列名。
    Returns:
        result (str): 数据某列的中位数。
    """
    data_list = cache_load(access_token)  # 从缓存加载数据
    if not data_list:  # 检查数据是否存在
        return "error"  # 返回错误信息
    df = tool.csv_to_pd(data_list)  # 转换为DataFrame
    result = tool.calculate_list_median(df, column_name)  # 计算列的中位数
    return str(result)  # 返回结果字符串
