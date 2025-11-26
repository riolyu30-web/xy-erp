import requests
import json
from typing import Dict, List, Any, Optional

def call_pay_settle_interface(access_token: str, pay_settle_det_pay_settle_from_receipt_date: str, 
                             pay_settle_det_pay_settle_to_receipt_date: str, supplier_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    调用应付结算接口，获取应付结算相关数据
    
    Args:
        access_token: 访问令牌
        pay_settle_det_pay_settle_from_receipt_date: 开始收款日期
        pay_settle_det_pay_settle_to_receipt_date: 结束收款日期
        supplier_name: 供应商名称(可选)
    
    Returns:
        List[Dict[str, Any]]: 应付结算数据列表
    """
    # 构建请求URL
    base_url = "http://192.168.0.251:9087"
    endpoint = "/pay-settle-det/paySettleDet_payableDet_suppStatementDet_matArrDet_ProcOrderDet_PurRequDet_PutBomNodeQuantity_BizOrderDetail__WorkOrderLeft/findList"
    url = f"{base_url}{endpoint}?access_token={access_token}"
    
    # 构建请求参数
    post_data = {
        "paySettleDetPaySettleClazz": "PAY_SETTLE",
        "paySettleDetPaySettleTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "paySettleDetPaySettleIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "paySettleDetClazz": "PAY_SETTLE_DET",
        "paySettleDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "paySettleDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "matArrDetClazz": "MAT_ARR_DET",
        "matArrDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "matArrDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "matArrDetMatArrClazz": "MAT_ARR",
        "matArrDetMatArrTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "matArrDetMatArrIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "procOrderDetClazz": "PROCUREMENT_ORDER_DETAIL",
        "procOrderDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "procOrderDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "procOrderDetProcOrderClazz": "PROCUREMENT_ORDER",
        "procOrderDetProcOrderTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "procOrderDetProcOrderIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "workOrderClazz": "WORK_ORDER",
        "workOrderTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "workOrderIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "bizOrderDetailClazz": "BUSINESS_ORDER_DETAIL",
        "bizOrderDetailTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "bizOrderDetailIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "bizOrderDetailBizOrderClazz": "BUSINESS_ORDER",
        "bizOrderDetailBizOrderTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "bizOrderDetailBizOrderIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "purRequDetClazz": "PURCHASE_REQUISITION_DETAIL",
        "purRequDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "purRequDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "purRequDetPurRequClazz": "PURCHASE_REQUISITION",
        "purRequDetPurRequTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "purRequDetPurRequIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "matClazz": "MATERIAL",
        "matTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "matIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "bomNodeClazz": "BOM_PROCESS",
        "bomNodeTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "bomNodeIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "bomNodeQuantityClazz": "MATERIAL-BOM_PROCESS",
        "bomNodeQuantityTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "bomNodeQuantityIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "purFrtDetPurFrtClazz": "PURCHASE_FORECASTING",
        "purFrtDetPurFrtTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "purFrtDetPurFrtIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "purFrtDetClazz": "PURCHASE_FORECASTING_DET",
        "purFrtDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "purFrtDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "mktFrtDetMktFrtClazz": "MARKET_FORECASTING",
        "mktFrtDetMktFrtTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "mktFrtDetMktFrtIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "mktFrtDetClazz": "MARKET_FORECASTING_DET",
        "mktFrtDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "mktFrtDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "suppStatementDetSuppStatementClazz": "SUPP_STATEMENT",
        "suppStatementDetSuppStatementTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "suppStatementDetSuppStatementIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "suppStatementDetClazz": "SUPP_STATEMENT_DET",
        "suppStatementDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "suppStatementDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "payableDetPayableClazz": "PAYABLE",
        "payableDetPayableTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "payableDetPayableIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "payableDetClazz": "PAYABLE_DET",
        "payableDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",
        "payableDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",
        "orderBys": [
            {
                "field": "paySettleDetPaySettleReceiptDate",
                "order": "DESC"
            }
        ],
        "paySettleDetPaySettleFromReceiptDate": pay_settle_det_pay_settle_from_receipt_date,
        "paySettleDetPaySettleToReceiptDate": pay_settle_det_pay_settle_to_receipt_date
    }
    
    # 如果提供了供应商名称，添加到请求参数中
    if supplier_name:
        post_data["paySettleDetPaySettleSupplierName"] = supplier_name
    
    try:
        # 发送POST请求
        response = requests.post(url, json=post_data)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析响应数据
        result = response.json()
        
        # 检查响应状态
        if result.get("code") == 0 and "data" in result:
            return result["data"]
        else:
            print(f"API请求失败: {result.get('msg', '未知错误')}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {str(e)}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON解析异常: {str(e)}")
        return []

def get_ids(data: List[Dict[str, Any]], key: str) -> List[str]:
    """
    从数据列表中提取指定键的所有值
    
    Args:
        data: 数据列表
        key: 要提取的键名
    
    Returns:
        List[str]: 提取的值列表
    """
    ids = []
    for item in data:
        if key in item and item[key] is not None:
            ids.append(item[key])
    return list(set(ids))  # 去重

def append_data(main_data: List[Dict[str, Any]], append_data: List[Dict[str, Any]], 
               main_key: str, append_key: str) -> List[Dict[str, Any]]:
    """
    将附加数据按ID绑定到主数据
    
    Args:
        main_data: 主数据列表
        append_data: 要附加的数据列表
        main_key: 主数据中的键名
        append_key: 附加数据中的键名
    
    Returns:
        List[Dict[str, Any]]: 合并后的数据列表
    """
    # 创建附加数据的映射表
    append_map = {}
    for item in append_data:
        if append_key in item and item[append_key] is not None:
            append_map[item[append_key]] = item
    
    # 将附加数据合并到主数据
    for main_item in main_data:
        if main_key in main_item and main_item[main_key] in append_map:
            # 合并数据，如果有冲突，主数据优先
            merged_item = {**append_map[main_item[main_key]], **main_item}
            main_item.update(merged_item)
    
    return main_data

def get_pay_settle_data(access_token: str, pay_settle_det_pay_settle_from_receipt_date: str, 
                       pay_settle_det_pay_settle_to_receipt_date: str, supplier_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    获取应付结算数据的主方法
    
    Args:
        access_token: 访问令牌
        pay_settle_det_pay_settle_from_receipt_date: 开始收款日期
        pay_settle_det_pay_settle_to_receipt_date: 结束收款日期
        supplier_name: 供应商名称(可选)
    
    Returns:
        List[Dict[str, Any]]: 应付结算数据列表
    """
    # 调用入口接口获取数据
    pay_settle_data = call_pay_settle_interface(
        access_token,
        pay_settle_det_pay_settle_from_receipt_date,
        pay_settle_det_pay_settle_to_receipt_date,
        supplier_name
    )
    
    return pay_settle_data