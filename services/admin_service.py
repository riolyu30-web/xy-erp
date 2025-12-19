from fastmcp import FastMCP  # 导入FastMCP框架
from services.tool import fetch_data  # 导入工具函数
from datetime import datetime, timedelta # 导入日期时间模块
import json  # 导入JSON库
admin_mcp = FastMCP(name="admin")  # 创建计算服务MCP实例


@admin_mcp.tool()  # 注册工具
def find_all_staff(access_token: str) -> str:  # 定义工具函数
    """
    员工表，获取员工信息
    
    若需查询部门下员工,要调用csv_merge合并表，左表:员工表，右表:部门表，左键:部门ID，右键:部门ID
    
    Args:
        access_token: 访问令牌
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 构建请求URL
    url = "/staff/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "staffClazz": "STAFF",  # 固定参数
        
        "groupDefaultType": "TEAM",  # 固定参数
        
        
        "orderBys": [  # 排序规则
            
        ]  # 排序结束
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "staffDepartmentId": {"name": "部门ID"},  # 字段映射
        
        "staffFullName": {"name": "名字"},  # 字段映射
        
        "staffPostId": {"name": "岗位_id"},  # 字段映射
        
        "staffSex": {"name": "性别", "values": {"1": "男", "2": "女", "3": "中性别"}}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "部门ID": "关联到部门表，表示员工所属部门",  # 字段含义
        
        "名字": "员工员工全名",  # 字段含义
        
        "岗位_id": "关联到岗位表，表示员工所属岗位",  # 字段含义
        
        "性别": "员工性别"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("员工表", url, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@admin_mcp.tool()  # 注册工具
def find_department(access_token: str) -> str:  # 定义工具函数
    """
    部门表，获取所有部门信息
    
    若需查询部门下员工,要调用csv_merge合并表，左表:员工表，右表:部门表，左键:部门ID，右键:部门ID
    
    Args:
        access_token: 访问令牌
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 构建请求URL
    url = "/group/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "groupClazz": "XY_USERCENTER_GROUP",  # 固定参数
        
        "groupDefaultType": "DEPARTMENT",  # 固定参数
        
        
        "orderBys": [  # 排序规则
            
        ]  # 排序结束
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "groupId": {"name": "部门ID"},  # 字段映射
        
        "groupName": {"name": "部门名字"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "部门ID": "ID",  # 字段含义
        
        "部门名字": "智能节点名"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("部门表", url, data, access_token, filtered_fields, meaning_list)  # 返回数据  
