
import sys # 导入sys模块
import os # 导入os模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将上上级目录添加到系统路径
from datetime import datetime, timedelta # 导入日期时间模块
from services.auth_service import auth_login # 导入登录认证模块
from services.tool import fetch_data,get_ids  # 导入工具函数
import json # 导入json模块


def find_client_test(access_token: str):  # 定义测试函数
    """
    测试 /client/findList
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
    fetch_data("客户表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def find_contract_test(access_token: str,biz_order_detail_ids: list):  # 定义测试函数
    """
    测试 /contract-detail/findList
    """
    # 构建请求URL
    url = "/contract-detail/findList"  # API地址

    # 构建请求体数据
    data = {
        
        "contractDetailClazz": "CONTRACT_DETAIL",  # 固定参数
        
        "contractDetailContractClazz": "CONTRACT",  # 固定参数
        
        "contractDetailIds": biz_order_detail_ids,
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
    fetch_data("合同表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def find_biz_order_test(access_token: str):  # 定义测试函数
    """
    测试 /biz-order-detail/findList
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
    result = fetch_data("订单表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

    data_list = result["data"]

    ids = get_ids(data_list,"主键ID")
    result = get_source_test(access_token,ids)
    data_list = result["data"]
    ids = get_ids(data_list,"源节点id")
    find_contract_test(access_token,ids)


def get_source_test(access_token: str,biz_order_detail_ids: list):  # 定义测试函数
    """
    测试 /proof/linkFindList
    """
    # 构建请求URL
    url = "/proof/linkFindList"  # API地址

    # 构建请求体数据
    data = {
        
        "linkTargetIds": biz_order_detail_ids,
        
        "linkTypeCode": "source",  # 固定参数
        
        #"linkClazz": "CONTRACT_DETAIL-BUSINESS_ORDER_DETAIL",  # 固定参数
        
    }  # 数据字典结束

    print(data)
    

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
    return fetch_data("关联表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)


if __name__ == "__main__":
    access_token = auth_login()  # 获取访问令牌
    
    #find_client_test(access_token)  # 调用测试函数
    
    #find_contract_test(access_token)  # 调用测试函数
    
    find_biz_order_test(access_token)  # 调用测试函数
    
    #get_source_test(access_token)  # 调用测试函数
    