from fastmcp import FastMCP  # 导入FastMCP框架
from services.tool import fetch_data  # 导入工具函数
from datetime import datetime, timedelta # 导入日期时间模块
import json  # 导入JSON库
business_mcp = FastMCP(name="business")  # 创建计算服务MCP实例


@business_mcp.tool()  # 注册工具
def find_client(access_token: str) -> str:  # 定义工具函数
    """
    客户表，获取所有客户
    
    Args:
        access_token: 访问令牌
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 构建请求URL
    url = "/client/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "customerClazz": "XY_USERCENTER_ORGANIZATION",  # 固定参数
        
        
        "orderBys": [  # 排序规则
            
        ]  # 排序结束
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "customerId": {"name": "客户ID"},  # 字段映射
        
        "customerLocationCity": {"name": "所在市"},  # 字段映射
        
        "customerLocationDistrict": {"name": "所在区域"},  # 字段映射
        
        "customerLocationProvince": {"name": "所在省"},  # 字段映射
        
        "customerName": {"name": "客户名称"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "客户ID": "客户表Pk",  # 字段含义
        
        "所在市": "客户表所在市",  # 字段含义
        
        "所在区域": "客户表所在区域",  # 字段含义
        
        "所在省": "客户表所在省",  # 字段含义
        
        "客户名称": "客户表全称名称"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("客户表", url, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@business_mcp.tool()  # 注册工具
def find_contract(access_token: str) -> str:  # 定义工具函数
    """
    合同表，获取所有合同信息
    
    Args:
        access_token: 访问令牌
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 构建请求URL
    url = "/contract-detail/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "contractDetailClazz": "CONTRACT_DETAIL",  # 固定参数
        
        "contractDetailContractClazz": "CONTRACT",  # 固定参数
        
        
        "orderBys": [  # 排序规则
            
        ]  # 排序结束
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "contractDetailContractId": {"name": "合同ID"},  # 字段映射
        
        "contractDetailContractTotalAmountIncludingTax": {"name": "含税总金额"},  # 字段映射
        
        "contractDetailId": {"name": "主键ID"},  # 字段映射
        
        "contractDetailPlannedOutputQuantity": {"name": "计划产出数量"},  # 字段映射
        
        "contractDetailPlannedTimeRequired": {"name": "计划需时(小时)"},  # 字段映射
        
        "contractDetailQuotationUnitPriceIncludingTax": {"name": "含税报价单价"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "合同ID": "合同明细PK",  # 字段含义
        
        "含税总金额": "合同明细含税总金额",  # 字段含义
        
        "主键ID": "合同明细主键ID",  # 字段含义
        
        "计划产出数量": "合同明细计划产出数量",  # 字段含义
        
        "计划需时(小时)": "合同明细计划需时(小时)",  # 字段含义
        
        "含税报价单价": "合同明细含税报价单价"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("合同表", url, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@business_mcp.tool()  # 注册工具
def find_biz_order(access_token: str) -> str:  # 定义工具函数
    """
    订单表，获取所有订单
    
    Args:
        access_token: 访问令牌
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 构建请求URL
    url = "/biz-order-detail/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "bizOrderDetailBizOrderClazz": "BUSINESS_ORDER",  # 固定参数
        
        "bizOrderDetailClazz": "BUSINESS_ORDER_DETAIL",  # 固定参数
        
        
        "orderBys": [  # 排序规则
            
        ]  # 排序结束
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "bizOrderDetailBizOrderDeliveryDate": {"name": "交货日期"},  # 字段映射
        
        "bizOrderDetailBizOrderExternalState": {"name": "上流程状态", "values": {"0": "未开始", "1": "进行中", "2": "异常", "3": "结束", "4": "中止", "5": "关闭"}},  # 字段映射
        
        "bizOrderDetailBizOrderId": {"name": "业务订单ID"},  # 字段映射
        
        "bizOrderDetailBizOrderIsUrgent": {"name": "是否加急", "values": {"true": "是", "false": "否"}},  # 字段映射
        
        "bizOrderDetailBizOrderProductionShiftId": {"name": "生产班次ID"},  # 字段映射
        
        "bizOrderDetailBizOrderReceiptDate": {"name": "单据日期"},  # 字段映射
        
        "bizOrderDetailBizOrderSettleCustId": {"name": "结算客户ID"},  # 字段映射
        
        "bizOrderDetailBizOrderTotalWt": {"name": "总重量"},  # 字段映射
        
        "bizOrderDetailId": {"name": "主键ID"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "交货日期": "业务订单明细交货日期",  # 字段含义
        
        "上流程状态": "业务订单明细上流程状态位。0-未开始；1-进行中；2-异常；3-结束；4-中止；5-关闭",  # 字段含义
        
        "业务订单ID": "业务订单明细PK",  # 字段含义
        
        "是否加急": "业务订单明细是否加急",  # 字段含义
        
        "生产班次ID": "业务订单明细生产班次ID",  # 字段含义
        
        "单据日期": "业务订单明细单据日期",  # 字段含义
        
        "结算客户ID": "业务订单明细结算客户ID",  # 字段含义
        
        "总重量": "业务订单明细总重量",  # 字段含义
        
        "主键ID": "业务订单明细主键ID"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("订单表", url, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@business_mcp.tool()  # 注册工具
def get_source(access_token: str) -> str:  # 定义工具函数
    """
    关联表，通过订单找合同信息
    
    Args:
        access_token: 访问令牌
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 构建请求URL
    url = "/proof/linkFindList"  # API地址
    # 构建请求体数据
    data = {
        
        "linkSource": "",  # 固定参数
        
        "linkTarget": "",  # 固定参数
        
        "linkTypeCode": "source",  # 固定参数
        
        "linkClazz": "CONTRACT_DETAIL-BUSINESS_ORDER_DETAIL",  # 固定参数
        
        
        "orderBys": [  # 排序规则
            
        ]  # 排序结束
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "linkId": {"name": "主键ID"},  # 字段映射
        
        "linkSource": {"name": "源节点id"},  # 字段映射
        
        "linkSourceIds": {"name": "源节点ids"},  # 字段映射
        
        "linkTarget": {"name": "目标节点id"},  # 字段映射
        
        "linkTargetIds": {"name": "目标节点ids"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "主键ID": "主键ID",  # 字段含义
        
        "源节点id": "源节点id(-查询入参-)",  # 字段含义
        
        "源节点ids": "源节点ids(-查询入参-)",  # 字段含义
        
        "目标节点id": "目标节点id(-查询入参-)",  # 字段含义
        
        "目标节点ids": "目标节点ids(-查询入参-)"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("关联表", url, data, access_token, filtered_fields, meaning_list)  # 返回数据  
