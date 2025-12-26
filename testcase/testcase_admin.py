
import sys # 导入sys模块
import os # 导入os模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将上上级目录添加到系统路径
from datetime import datetime, timedelta # 导入日期时间模块
from services.auth_service import auth_login # 导入登录认证模块
from services.tool import fetch_data  # 导入工具函数
import json # 导入json模块


def find_all_staff_test(access_token: str):  # 定义测试函数
    """
    测试 /staff/findList
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
    fetch_data("员工表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def find_department_test(access_token: str):  # 定义测试函数
    """
    测试 /group/findList
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
    fetch_data("部门表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def find_role_test(access_token: str):  # 定义测试函数
    """
    测试 /role/findList
    """
    # 构建请求URL
    url = "/role/findList"  # API地址

    # 构建请求体数据
    data = {
        
        "roleClazz": "XY_USERCENTER_ROLE",  # 固定参数
        
        "roleDefaultType": "POST",  # 固定参数
        
        
        "orderBys": [  # 排序规则
            
        ]  # 排序结束
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "roleId": {"name": "表ID"},  # 字段映射
        
        "roleName": {"name": "岗位名称"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "表ID": "岗位表ID",  # 字段含义
        
        "岗位名称": "岗位表智能节点名"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("岗位表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)


if __name__ == "__main__":
    access_token = auth_login()  # 获取访问令牌
    
    find_all_staff_test(access_token)  # 调用测试函数
    
    find_department_test(access_token)  # 调用测试函数
    
    find_role_test(access_token)  # 调用测试函数
    