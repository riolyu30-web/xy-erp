from os import name
from fastmcp import FastMCP  # 导入FastMCP框架
from services.tool import fetch_data  # 导入工具函数

admin_mcp = FastMCP(name="admin")  # 创建计算服务MCP实例

@admin_mcp.tool()
def find_all_staff(access_token: str) -> str:
    """
    获取员工列表，主表，字段为姓名、性别、手机号、是否临时工、入职时间
    1、需要班组字段请合并find_all_group
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 员工表令牌，字段为姓名、性别、手机号、是否临时工、入职时间
    """
    # 构建请求URL
    url = "/staff/findList"
     
    # 构建请求体数据
    data = {
        "orderBys": [
            {"field": "staffSerialNumber", "order": "ASC"},
            {"field": "staffCreateTime", "order": "DESC"},
            {"field": "staffUpdateTime", "order": "DESC"}
        ],
    }
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "staffName": {"name": "姓名"},
        "staffSex": {"name": "性别", "value": {"1": "男", "2": "女", "3": "未知"}},
        "staffPhone": {"name": "手机号"},
        "staffIsTemporary": {"name": "是否临时工", "value": {"true": "是", "false": "否"}},
        "staffHireDate": {"name": "入职时间"}
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("员工表", url, data, access_token, filtered_fields) 

@admin_mcp.tool()
def find_all_group(access_token: str) -> str:
    """
    获取班组列表，从表，字段为班组名称、班组编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 班组表令牌
    """
    # 构建请求URL
    url = "/group/findList"
     
    # 构建请求体数据
    data = {
        "orderBys": [
            {"field": "groupSerialNumber", "order": "ASC"},
            {"field": "groupCreateTime", "order": "DESC"},
        ],
    }
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "groupName": {"name": "班组名称"},
        "groupUserCode": {"name": "班组编码"},
        "groupInUsed": {"name": "是否启用", "value": {"true": "是", "false": "否"}},
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("班组表", url, data, access_token, filtered_fields) 