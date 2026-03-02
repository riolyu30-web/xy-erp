from fastmcp import FastMCP  # 导入FastMCP框架
from services.tool import fetch_data  # 导入工具函数
from datetime import datetime, timedelta # 导入日期时间模块
import json  # 导入JSON库
purchase_mcp = FastMCP(name="purchase")  # 创建计算服务MCP实例


@purchase_mcp.tool()  # 注册工具
def PURCHASE_REQUISITION_DETAIL(access_token: str,purRequDetFromCreateTime:str=None,purRequDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    采购申请明细表，采购申请
    
    Args:
        access_token: 访问令牌
        
        purRequDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        purRequDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "PURCHASE_REQUISITION_DETAIL"
    # 构建请求URL
    url = "/pur-requ-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "purRequDetPurRequClazz": "PURCHASE_REQUISITION_DETAIL",  # 固定参数
        
        "purRequDetClazz": "PURCHASE_REQUISITION",  # 固定参数
        
        
        "purRequDetFromCreateTime": purRequDetFromCreateTime,  # 动态参数
        
        "purRequDetToCreateTime": purRequDetToCreateTime,  # 动态参数
        
        "key": "PURCHASE_REQUISITION_DETAIL",
        "from": purRequDetFromCreateTime,
        "to": purRequDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "purRequDetActualTimeRequired": {"name": "采购申请明细表实际需时"},  # 字段映射
        
        "purRequDetAuditDate": {"name": "采购申请明细表审核时间"},  # 字段映射
        
        "purRequDetBriefName": {"name": "采购申请明细表简称"},  # 字段映射
        
        "purRequDetCompleteQuantity": {"name": "采购申请明细表完成数量"},  # 字段映射
        
        "purRequDetCompleteStatus": {"name": "采购申请明细表完成状态"},  # 字段映射
        
        "purRequDetEndTime": {"name": "采购申请明细表结束时间"},  # 字段映射
        
        "purRequDetId": {"name": "采购申请明细表PK"},  # 字段映射
        
        "purRequDetName": {"name": "采购申请明细表智能节点名"},  # 字段映射
        
        "purRequDetPlannedOutputQuantity": {"name": "采购申请明细表计划产出数量"},  # 字段映射
        
        "purRequDetPlannedTimeRequired": {"name": "采购申请明细表计划需时"},  # 字段映射
        
        "purRequDetPrintTimes": {"name": "采购申请明细表打印次数"},  # 字段映射
        
        "purRequDetPurRequActualTimeRequired": {"name": "采购申请明细表实际需时"},  # 字段映射
        
        "purRequDetPurRequAdjustmentTimeRequired": {"name": "采购申请明细表调整需时"},  # 字段映射
        
        "purRequDetPurRequBriefName": {"name": "采购申请明细表简称"},  # 字段映射
        
        "purRequDetPurRequCompleteQuantity": {"name": "采购申请明细表完成数量"},  # 字段映射
        
        "purRequDetPurRequCompleteStatus": {"name": "采购申请明细表完成状态"},  # 字段映射
        
        "purRequDetPurRequDeliveryDate": {"name": "采购申请明细表交货日期"},  # 字段映射
        
        "purRequDetPurRequPurchaseOrderQuantity": {"name": "采购申请明细表已开采购订单数量"},  # 字段映射
        
        "purRequDetPurRequPurchaseOrderState": {"name": "采购申请明细表已开采购订单状态"},  # 字段映射
        
        "purRequDetPurRequQuantity": {"name": "采购申请明细表任务数量"},  # 字段映射
        
        "purRequDetPurchaseOrderQuantity": {"name": "采购申请明细表已开采购订单数量"},  # 字段映射
        
        "purRequDetPurchaseOrderState": {"name": "采购申请明细表已开采购订单状态"},  # 字段映射
        
        "purRequDetQuantity": {"name": "采购申请明细表任务数量"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "采购申请明细表实际需时": "采购申请明细表实际需时(小时)",  # 字段含义
        
        "采购申请明细表审核时间": "采购申请明细表审核时间",  # 字段含义
        
        "采购申请明细表简称": "采购申请明细表简称",  # 字段含义
        
        "采购申请明细表完成数量": "采购申请明细表完成数量",  # 字段含义
        
        "采购申请明细表完成状态": "采购申请明细表完成状态",  # 字段含义
        
        "采购申请明细表结束时间": "采购申请明细表结束时间",  # 字段含义
        
        "采购申请明细表PK": "采购申请明细表PK",  # 字段含义
        
        "采购申请明细表智能节点名": "采购申请明细表智能节点名",  # 字段含义
        
        "采购申请明细表计划产出数量": "采购申请明细表计划产出数量",  # 字段含义
        
        "采购申请明细表计划需时": "采购申请明细表计划需时(小时)",  # 字段含义
        
        "采购申请明细表打印次数": "采购申请明细表打印次数",  # 字段含义
        
        "采购申请明细表实际需时": "采购申请明细表实际需时(小时)",  # 字段含义
        
        "采购申请明细表调整需时": "采购申请明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "采购申请明细表简称": "采购申请明细表简称",  # 字段含义
        
        "采购申请明细表完成数量": "采购申请明细表完成数量",  # 字段含义
        
        "采购申请明细表完成状态": "采购申请明细表完成状态",  # 字段含义
        
        "采购申请明细表交货日期": "采购申请明细表交货日期",  # 字段含义
        
        "采购申请明细表已开采购订单数量": "采购申请明细表已开采购订单数量",  # 字段含义
        
        "采购申请明细表已开采购订单状态": "采购申请明细表已开采购订单状态",  # 字段含义
        
        "采购申请明细表任务数量": "采购申请明细表任务数量",  # 字段含义
        
        "采购申请明细表已开采购订单数量": "采购申请明细表已开采购订单数量",  # 字段含义
        
        "采购申请明细表已开采购订单状态": "采购申请明细表已开采购订单状态",  # 字段含义
        
        "采购申请明细表任务数量": "采购申请明细表任务数量"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("采购申请明细表", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@purchase_mcp.tool()  # 注册工具
def PROCUREMENT_ORDER_DETAIL(access_token: str,procOrderDetFromCreateTime:str=None,procOrderDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    采购订单明细表，采购订单
    
    Args:
        access_token: 访问令牌
        
        procOrderDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        procOrderDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "PROCUREMENT_ORDER_DETAIL"
    # 构建请求URL
    url = "/procurement-order-detail/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "procOrderDetProcOrderClazz": "PROCUREMENT_ORDER_DETAIL",  # 固定参数
        
        "procOrderDetClazz": "PROCUREMENT_ORDER",  # 固定参数
        
        
        "procOrderDetFromCreateTime": procOrderDetFromCreateTime,  # 动态参数
        
        "procOrderDetToCreateTime": procOrderDetToCreateTime,  # 动态参数
        
        "key": "PROCUREMENT_ORDER_DETAIL",
        "from": procOrderDetFromCreateTime,
        "to": procOrderDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "procOrderDetActualTimeRequired": {"name": "采购订单明细表实际需时"},  # 字段映射
        
        "procOrderDetAdjustmentTimeRequired": {"name": "采购订单明细表调整需时"},  # 字段映射
        
        "procOrderDetAreaId": {"name": "采购订单明细表行政区域id"},  # 字段映射
        
        "procOrderDetBizOrderQuantity": {"name": "采购订单明细表已开销售订单数量"},  # 字段映射
        
        "procOrderDetBizOrderStatus": {"name": "采购订单明细表已开销售订单状态"},  # 字段映射
        
        "procOrderDetBizVersion": {"name": "采购订单明细表业务自定义版本号"},  # 字段映射
        
        "procOrderDetCompleteQuantity": {"name": "采购订单明细表完成数量"},  # 字段映射
        
        "procOrderDetCompleteStatus": {"name": "采购订单明细表完成状态"},  # 字段映射
        
        "procOrderDetGiftQty": {"name": "采购订单明细表赠品数量"},  # 字段映射
        
        "procOrderDetId": {"name": "采购订单明细表主键ID"},  # 字段映射
        
        "procOrderDetIqcQuantity": {"name": "采购订单明细表已开IQC的数量"},  # 字段映射
        
        "procOrderDetIqcStatus": {"name": "采购订单明细表已开IQC的状态"},  # 字段映射
        
        "procOrderDetIsManualModificationDate": {"name": "采购订单明细表是否手动修改计划生产时间"},  # 字段映射
        
        "procOrderDetLocUnitPrice": {"name": "采购订单明细表本币单价"},  # 字段映射
        
        "procOrderDetLocalAmount": {"name": "采购订单明细表本币金额"},  # 字段映射
        
        "procOrderDetLossQty": {"name": "采购订单明细表损耗"},  # 字段映射
        
        "procOrderDetPlannedOutputQuantity": {"name": "采购订单明细表计划产出数量"},  # 字段映射
        
        "procOrderDetPlannedTimeRequired": {"name": "采购订单明细表计划需时"},  # 字段映射
        
        "procOrderDetProcOrderCompleteQuantity": {"name": "采购订单明细表完成数量"},  # 字段映射
        
        "procOrderDetProcOrderCompleteStatus": {"name": "采购订单明细表完成状态"},  # 字段映射
        
        "procOrderDetProcOrderContName": {"name": "采购订单明细表联系人姓名"},  # 字段映射
        
        "procOrderDetProcOrderDelvSup": {"name": "采购订单明细表送货供应商"},  # 字段映射
        
        "procOrderDetProcOrderPlannedOutputQuantity": {"name": "采购订单明细表计划产出数量"},  # 字段映射
        
        "procOrderDetProcOrderPlannedTimeRequired": {"name": "采购订单明细表计划需时"},  # 字段映射
        
        "procOrderDetProcOrderQuantity": {"name": "采购订单明细表任务数量"},  # 字段映射
        
        "procOrderDetProcOrderStlFee": {"name": "采购订单明细表结算费用"},  # 字段映射
        
        "procOrderDetProcOrderStlPriceFmt": {"name": "采购订单明细表结算单价保留小数位"},  # 字段映射
        
        "procOrderDetProcOrderTotalFeeNt": {"name": "采购订单明细表总费用"},  # 字段映射
        
        "procOrderDetProcOrderTotalVol": {"name": "采购订单明细表总体积"},  # 字段映射
        
        "procOrderDetProcOrderTotalWithTax": {"name": "采购订单明细表总费用"},  # 字段映射
        
        "procOrderDetProcOrderTotalWt": {"name": "采购订单明细表总重量"},  # 字段映射
        
        "procOrderDetProductionProcessesTypeId": {"name": "采购订单明细表工序类型ID"},  # 字段映射
        
        "procOrderDetProductionShiftId": {"name": "采购订单明细表生产班次ID"},  # 字段映射
        
        "procOrderDetProp": {"name": "采购订单明细表比例"},  # 字段映射
        
        "procOrderDetQuantity": {"name": "采购订单明细表任务数量"},  # 字段映射
        
        "procOrderDetQuoteQty": {"name": "采购订单明细表报价数量"},  # 字段映射
        
        "procOrderDetSerialNumber": {"name": "采购订单明细表顺序号"},  # 字段映射
        
        "procOrderDetSettleAmount": {"name": "采购订单明细表结算金额"},  # 字段映射
        
        "procOrderDetSettlePrice": {"name": "采购订单明细表结算单价"},  # 字段映射
        
        "procOrderDetSettleTotalAmount": {"name": "采购订单明细表结算金额"},  # 字段映射
        
        "procOrderDetSpareQty": {"name": "采购订单明细表备用数量"},  # 字段映射
        
        "procOrderDetState": {"name": "采购订单明细表通用状态"},  # 字段映射
        
        "procOrderDetStockQty": {"name": "采购订单明细表备库存数量"},  # 字段映射
        
        "procOrderDetSumQty": {"name": "采购订单明细表总数量"},  # 字段映射
        
        "procOrderDetTaxExclTotal": {"name": "采购订单明细表不含税总金额"},  # 字段映射
        
        "procOrderDetTaxExclUnitPrice": {"name": "采购订单明细表不含税单价"},  # 字段映射
        
        "procOrderDetTaxInclPrice": {"name": "采购订单明细表含税报价单价"},  # 字段映射
        
        "procOrderDetTaxInclTotal": {"name": "采购订单明细表含税总金额"},  # 字段映射
        
        "procOrderDetUnitPriceTax": {"name": "采购订单明细表含税单价"},  # 字段映射
        
        "procOrderDetUsedQty": {"name": "采购订单明细表使用库存数量"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "采购订单明细表实际需时": "采购订单明细表实际需时(小时)",  # 字段含义
        
        "采购订单明细表调整需时": "采购订单明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "采购订单明细表行政区域id": "采购订单明细表行政区域id",  # 字段含义
        
        "采购订单明细表已开销售订单数量": "采购订单明细表已开销售订单数量",  # 字段含义
        
        "采购订单明细表已开销售订单状态": "采购订单明细表已开销售订单状态",  # 字段含义
        
        "采购订单明细表业务自定义版本号": "采购订单明细表业务自定义版本号",  # 字段含义
        
        "采购订单明细表完成数量": "采购订单明细表完成数量",  # 字段含义
        
        "采购订单明细表完成状态": "采购订单明细表完成状态",  # 字段含义
        
        "采购订单明细表赠品数量": "采购订单明细表赠品数量",  # 字段含义
        
        "采购订单明细表主键ID": "采购订单明细表主键ID",  # 字段含义
        
        "采购订单明细表已开IQC的数量": "采购订单明细表已开IQC的数量",  # 字段含义
        
        "采购订单明细表已开IQC的状态": "采购订单明细表已开IQC的状态",  # 字段含义
        
        "采购订单明细表是否手动修改计划生产时间": "采购订单明细表是否手动修改计划生产时间",  # 字段含义
        
        "采购订单明细表本币单价": "采购订单明细表本币单价(根据币种，外币才显示)，外币不含税",  # 字段含义
        
        "采购订单明细表本币金额": "采购订单明细表本币金额(根据币种，外币才显示)，外币不含税",  # 字段含义
        
        "采购订单明细表损耗": "采购订单明细表损耗",  # 字段含义
        
        "采购订单明细表计划产出数量": "采购订单明细表计划产出数量",  # 字段含义
        
        "采购订单明细表计划需时": "采购订单明细表计划需时(小时)",  # 字段含义
        
        "采购订单明细表完成数量": "采购订单明细表完成数量",  # 字段含义
        
        "采购订单明细表完成状态": "采购订单明细表完成状态",  # 字段含义
        
        "采购订单明细表联系人姓名": "采购订单明细表联系人姓名",  # 字段含义
        
        "采购订单明细表送货供应商": "采购订单明细表送货供应商",  # 字段含义
        
        "采购订单明细表计划产出数量": "采购订单明细表计划产出数量",  # 字段含义
        
        "采购订单明细表计划需时": "采购订单明细表计划需时(小时)",  # 字段含义
        
        "采购订单明细表任务数量": "采购订单明细表任务数量",  # 字段含义
        
        "采购订单明细表结算费用": "采购订单明细表结算费用（默认与含税总金额相等)",  # 字段含义
        
        "采购订单明细表结算单价保留小数位": "采购订单明细表结算单价保留小数位(默认9位，可手动变更)",  # 字段含义
        
        "采购订单明细表总费用": "采购订单明细表总费用(不含税)",  # 字段含义
        
        "采购订单明细表总体积": "采购订单明细表总体积",  # 字段含义
        
        "采购订单明细表总费用": "采购订单明细表总费用(含税)",  # 字段含义
        
        "采购订单明细表总重量": "采购订单明细表总重量",  # 字段含义
        
        "采购订单明细表工序类型ID": "采购订单明细表工序类型ID",  # 字段含义
        
        "采购订单明细表生产班次ID": "采购订单明细表生产班次ID",  # 字段含义
        
        "采购订单明细表比例": "采购订单明细表比例",  # 字段含义
        
        "采购订单明细表任务数量": "采购订单明细表任务数量",  # 字段含义
        
        "采购订单明细表报价数量": "采购订单明细表报价数量",  # 字段含义
        
        "采购订单明细表顺序号": "采购订单明细表顺序号",  # 字段含义
        
        "采购订单明细表结算金额": "采购订单明细表结算金额（默认与含税总金额相等），写入库存价格字段",  # 字段含义
        
        "采购订单明细表结算单价": "采购订单明细表结算单价（默认与含税单价相等），写入库存价格字段",  # 字段含义
        
        "采购订单明细表结算金额": "采购订单明细表结算金额（默认与含税总金额相等），写入库存价格字段",  # 字段含义
        
        "采购订单明细表备用数量": "采购订单明细表备用数量",  # 字段含义
        
        "采购订单明细表通用状态": "采购订单明细表通用状态",  # 字段含义
        
        "采购订单明细表备库存数量": "采购订单明细表备库存数量",  # 字段含义
        
        "采购订单明细表总数量": "采购订单明细表总数量",  # 字段含义
        
        "采购订单明细表不含税总金额": "采购订单明细表不含税总金额",  # 字段含义
        
        "采购订单明细表不含税单价": "采购订单明细表不含税单价(默认隐藏，根据计费方案转换计算得出)",  # 字段含义
        
        "采购订单明细表含税报价单价": "采购订单明细表含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "采购订单明细表含税总金额": "采购订单明细表含税总金额",  # 字段含义
        
        "采购订单明细表含税单价": "采购订单明细表含税单价(默认隐藏，根据计费方案转换计算得出)",  # 字段含义
        
        "采购订单明细表使用库存数量": "采购订单明细表使用库存数量"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("采购订单明细表", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@purchase_mcp.tool()  # 注册工具
def MAT_INSTORAGE_DET(access_token: str,matInstorageDetFromCreateTime:str=None,matInstorageDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    物料入库明细表，物料入库
    
    Args:
        access_token: 访问令牌
        
        matInstorageDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        matInstorageDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "MAT_INSTORAGE_DET"
    # 构建请求URL
    url = "/mat-instorage-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "matInstorageDetMatInstorageClazz": "MAT_INSTORAGE",  # 固定参数
        
        "matInstorageDetClazz": "MAT_INSTORAGE_DET",  # 固定参数
        
        
        "matInstorageDetFromCreateTime": matInstorageDetFromCreateTime,  # 动态参数
        
        "matInstorageDetToCreateTime": matInstorageDetToCreateTime,  # 动态参数
        
        "key": "MAT_INSTORAGE_DET",
        "from": matInstorageDetFromCreateTime,
        "to": matInstorageDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "matInstorageDetAdditionalWeight": {"name": "物料入库明细表附加重量"},  # 字段映射
        
        "matInstorageDetAdjustmentTimeRequired": {"name": "物料入库明细表调整需时"},  # 字段映射
        
        "matInstorageDetBriefName": {"name": "物料入库明细表简称"},  # 字段映射
        
        "matInstorageDetCompleteQuantity": {"name": "物料入库明细表完成数量"},  # 字段映射
        
        "matInstorageDetCompleteStatus": {"name": "物料入库明细表完成状态"},  # 字段映射
        
        "matInstorageDetDeliveryDate": {"name": "物料入库明细表交货日期"},  # 字段映射
        
        "matInstorageDetId": {"name": "物料入库明细表PK"},  # 字段映射
        
        "matInstorageDetInventoryQuantity": {"name": "物料入库明细表库存数量"},  # 字段映射
        
        "matInstorageDetLocalCurrencyTotalAmount": {"name": "物料入库明细表本币总金额"},  # 字段映射
        
        "matInstorageDetLocalCurrencyUnitPrice": {"name": "物料入库明细表本币单价"},  # 字段映射
        
        "matInstorageDetMatInstorageActualTimeRequired": {"name": "物料入库明细表实际需时"},  # 字段映射
        
        "matInstorageDetMatInstorageAdjustmentTimeRequired": {"name": "物料入库明细表调整需时"},  # 字段映射
        
        "matInstorageDetMatInstorageCompleteQuantity": {"name": "物料入库明细表完成数量"},  # 字段映射
        
        "matInstorageDetMatInstorageCompleteStatus": {"name": "物料入库明细表完成状态"},  # 字段映射
        
        "matInstorageDetMatInstorageDeliveryDate": {"name": "物料入库明细表交货日期"},  # 字段映射
        
        "matInstorageDetMatInstorageEndTime": {"name": "物料入库明细表结束时间"},  # 字段映射
        
        "matInstorageDetMatInstorageEndTimeRequired": {"name": "物料入库明细表最后需时"},  # 字段映射
        
        "matInstorageDetMatInstorageEquipmentId": {"name": "物料入库明细表设备id"},  # 字段映射
        
        "matInstorageDetMatInstorageExchangeRateId": {"name": "物料入库明细表币种汇率id"},  # 字段映射
        
        "matInstorageDetMatInstorageOrgId": {"name": "物料入库明细表机构id"},  # 字段映射
        
        "matInstorageDetMatInstoragePlannedOutputQuantity": {"name": "物料入库明细表计划产出数量"},  # 字段映射
        
        "matInstorageDetMatInstoragePlannedTimeRequired": {"name": "物料入库明细表计划需时"},  # 字段映射
        
        "matInstorageDetMatInstorageQuantity": {"name": "物料入库明细表任务数量"},  # 字段映射
        
        "matInstorageDetMatInstorageReceiptDate": {"name": "物料入库明细表单据日期"},  # 字段映射
        
        "matInstorageDetMatInstorageReceiptType": {"name": "物料入库明细表单据类型"},  # 字段映射
        
        "matInstorageDetMaterialId": {"name": "物料入库明细表物料id"},  # 字段映射
        
        "matInstorageDetOrgId": {"name": "物料入库明细表机构id"},  # 字段映射
        
        "matInstorageDetPackageMatId": {"name": "物料入库明细表包装物料id"},  # 字段映射
        
        "matInstorageDetPlannedOutputQuantity": {"name": "物料入库明细表计划产出数量"},  # 字段映射
        
        "matInstorageDetPlannedTimeRequired": {"name": "物料入库明细表计划需时"},  # 字段映射
        
        "matInstorageDetPrintTimes": {"name": "物料入库明细表打印次数"},  # 字段映射
        
        "matInstorageDetQuantity": {"name": "物料入库明细表任务数量"},  # 字段映射
        
        "matInstorageDetQuotationUnitPriceIncludingTax": {"name": "物料入库明细表报价单价"},  # 字段映射
        
        "matInstorageDetQuotationUnitPriceWithoutTax": {"name": "物料入库明细表报价单价"},  # 字段映射
        
        "matInstorageDetReceiptDate": {"name": "物料入库明细表单据日期"},  # 字段映射
        
        "matInstorageDetSettMethod": {"name": "物料入库明细表结算方式"},  # 字段映射
        
        "matInstorageDetSettlementTotalAmount": {"name": "物料入库明细表结算总金额"},  # 字段映射
        
        "matInstorageDetSingleWeight": {"name": "物料入库明细表单重kg"},  # 字段映射
        
        "matInstorageDetTotalAmount": {"name": "物料入库明细表总金额"},  # 字段映射
        
        "matInstorageDetTotalAmountIncludingTax": {"name": "物料入库明细表总金额"},  # 字段映射
        
        "matInstorageDetTotalAmountWithoutTax": {"name": "物料入库明细表总金额"},  # 字段映射
        
        "matInstorageDetTotalWeightLot": {"name": "物料入库明细表合计总重kg"},  # 字段映射
        
        "matInstorageDetUnitPriceIncludingTax": {"name": "物料入库明细表单价"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "物料入库明细表附加重量": "物料入库明细表附加重量",  # 字段含义
        
        "物料入库明细表调整需时": "物料入库明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "物料入库明细表简称": "物料入库明细表简称",  # 字段含义
        
        "物料入库明细表完成数量": "物料入库明细表完成数量",  # 字段含义
        
        "物料入库明细表完成状态": "物料入库明细表完成状态",  # 字段含义
        
        "物料入库明细表交货日期": "物料入库明细表交货日期",  # 字段含义
        
        "物料入库明细表PK": "物料入库明细表PK",  # 字段含义
        
        "物料入库明细表库存数量": "物料入库明细表库存数量(当单据触发时，记录当前库存数量，库存数量流水)",  # 字段含义
        
        "物料入库明细表本币总金额": "物料入库明细表本币总金额",  # 字段含义
        
        "物料入库明细表本币单价": "物料入库明细表本币单价",  # 字段含义
        
        "物料入库明细表实际需时": "物料入库明细表实际需时(小时)",  # 字段含义
        
        "物料入库明细表调整需时": "物料入库明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "物料入库明细表完成数量": "物料入库明细表完成数量",  # 字段含义
        
        "物料入库明细表完成状态": "物料入库明细表完成状态",  # 字段含义
        
        "物料入库明细表交货日期": "物料入库明细表交货日期",  # 字段含义
        
        "物料入库明细表结束时间": "物料入库明细表结束时间",  # 字段含义
        
        "物料入库明细表最后需时": "物料入库明细表最后需时(小时)",  # 字段含义
        
        "物料入库明细表设备id": "物料入库明细表设备id",  # 字段含义
        
        "物料入库明细表币种汇率id": "物料入库明细表币种汇率id",  # 字段含义
        
        "物料入库明细表机构id": "物料入库明细表机构id(客户/供应商)",  # 字段含义
        
        "物料入库明细表计划产出数量": "物料入库明细表计划产出数量",  # 字段含义
        
        "物料入库明细表计划需时": "物料入库明细表计划需时(小时)",  # 字段含义
        
        "物料入库明细表任务数量": "物料入库明细表任务数量",  # 字段含义
        
        "物料入库明细表单据日期": "物料入库明细表单据日期",  # 字段含义
        
        "物料入库明细表单据类型": "物料入库明细表单据类型（一个常量值，与node里的defaultTypeId不一样，推荐使用字典）",  # 字段含义
        
        "物料入库明细表物料id": "物料入库明细表物料id",  # 字段含义
        
        "物料入库明细表机构id": "物料入库明细表机构id(客户/供应商)",  # 字段含义
        
        "物料入库明细表包装物料id": "物料入库明细表包装物料id",  # 字段含义
        
        "物料入库明细表计划产出数量": "物料入库明细表计划产出数量",  # 字段含义
        
        "物料入库明细表计划需时": "物料入库明细表计划需时(小时)",  # 字段含义
        
        "物料入库明细表打印次数": "物料入库明细表打印次数",  # 字段含义
        
        "物料入库明细表任务数量": "物料入库明细表任务数量",  # 字段含义
        
        "物料入库明细表报价单价": "物料入库明细表报价单价（含税）",  # 字段含义
        
        "物料入库明细表报价单价": "物料入库明细表报价单价（不含税）",  # 字段含义
        
        "物料入库明细表单据日期": "物料入库明细表单据日期",  # 字段含义
        
        "物料入库明细表结算方式": "物料入库明细表结算方式",  # 字段含义
        
        "物料入库明细表结算总金额": "物料入库明细表结算总金额",  # 字段含义
        
        "物料入库明细表单重kg": "物料入库明细表单重kg",  # 字段含义
        
        "物料入库明细表总金额": "物料入库明细表总金额(不含税)，汇总批次的总价值，不用理会单价。原则：总价值不会变化",  # 字段含义
        
        "物料入库明细表总金额": "物料入库明细表总金额（含税）",  # 字段含义
        
        "物料入库明细表总金额": "物料入库明细表总金额（不含税）",  # 字段含义
        
        "物料入库明细表合计总重kg": "物料入库明细表合计总重kg",  # 字段含义
        
        "物料入库明细表单价": "物料入库明细表单价（含税）"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("物料入库明细表", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@purchase_mcp.tool()  # 注册工具
def SUPP_STATEMENT_DET(access_token: str,suppStatementDetFromCreateTime:str=None,suppStatementDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    供应商对账单明细，供应商对账
    
    Args:
        access_token: 访问令牌
        
        suppStatementDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        suppStatementDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "SUPP_STATEMENT_DET"
    # 构建请求URL
    url = "/supp-statement-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "suppStatementDetSuppStatementClazz": "SUPP_STATEMENT",  # 固定参数
        
        "suppStatementDetClazz": "SUPP_STATEMENT_DET",  # 固定参数
        
        
        "suppStatementDetFromCreateTime": suppStatementDetFromCreateTime,  # 动态参数
        
        "suppStatementDetToCreateTime": suppStatementDetToCreateTime,  # 动态参数
        
        "key": "SUPP_STATEMENT_DET",
        "from": suppStatementDetFromCreateTime,
        "to": suppStatementDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "suppStatementDetActualTimeRequired": {"name": "供应商对账单明细实际需时"},  # 字段映射
        
        "suppStatementDetAmount": {"name": "供应商对账单明细金额"},  # 字段映射
        
        "suppStatementDetBeginTime": {"name": "供应商对账单明细开始时间"},  # 字段映射
        
        "suppStatementDetBriefName": {"name": "供应商对账单明细简称"},  # 字段映射
        
        "suppStatementDetCompleteQuantity": {"name": "供应商对账单明细完成数量"},  # 字段映射
        
        "suppStatementDetCompleteStatus": {"name": "供应商对账单明细完成状态"},  # 字段映射
        
        "suppStatementDetDeliveryDate": {"name": "供应商对账单明细交货日期"},  # 字段映射
        
        "suppStatementDetEndTime": {"name": "供应商对账单明细结束时间"},  # 字段映射
        
        "suppStatementDetId": {"name": "供应商对账单明细PK"},  # 字段映射
        
        "suppStatementDetLocAmount": {"name": "供应商对账单明细本币金额"},  # 字段映射
        
        "suppStatementDetLocCompleteQuantity": {"name": "供应商对账单明细本币完成数量"},  # 字段映射
        
        "suppStatementDetLocInvoicedAmount": {"name": "供应商对账单明细本币已开票金额"},  # 字段映射
        
        "suppStatementDetLocOtherExpense": {"name": "供应商对账单明细本币其他费用"},  # 字段映射
        
        "suppStatementDetLocSettleAmount": {"name": "供应商对账单明细本币结算金额"},  # 字段映射
        
        "suppStatementDetLocSettledAmount": {"name": "供应商对账单明细本币已结算金额"},  # 字段映射
        
        "suppStatementDetSettleAmount": {"name": "供应商对账单明细结算金额"},  # 字段映射
        
        "suppStatementDetSettledAmount": {"name": "供应商对账单明细已结算金额"},  # 字段映射
        
        "suppStatementDetSettledState": {"name": "供应商对账单明细结算状态"},  # 字段映射
        
        "suppStatementDetSuppStatementCompleteQuantity": {"name": "供应商对账单明细完成数量"},  # 字段映射
        
        "suppStatementDetSuppStatementCompleteStatus": {"name": "供应商对账单明细完成状态"},  # 字段映射
        
        "suppStatementDetSuppStatementCurrency": {"name": "供应商对账单明细币种"},  # 字段映射
        
        "suppStatementDetSuppStatementDeliveryDate": {"name": "供应商对账单明细交货日期"},  # 字段映射
        
        "suppStatementDetSuppStatementDescription": {"name": "供应商对账单明细描述"},  # 字段映射
        
        "suppStatementDetSuppStatementProductionProcessesTypeId": {"name": "供应商对账单明细工序类型ID"},  # 字段映射
        
        "suppStatementDetSuppStatementProductionShiftId": {"name": "供应商对账单明细生产班次ID"},  # 字段映射
        
        "suppStatementDetSuppStatementQuantity": {"name": "供应商对账单明细任务数量"},  # 字段映射
        
        "suppStatementDetSuppStatementReceiptDate": {"name": "供应商对账单明细单据日期"},  # 字段映射
        
        "suppStatementDetSuppStatementTotalAmount": {"name": "供应商对账单明细总金额"},  # 字段映射
        
        "suppStatementDetSuppStatementTotalInvoicedAmount": {"name": "供应商对账单明细总已开票金额"},  # 字段映射
        
        "suppStatementDetSuppStatementTotalOtherExpense": {"name": "供应商对账单明细总其他费用"},  # 字段映射
        
        "suppStatementDetSuppStatementTotalSettleAmount": {"name": "供应商对账单明细总结算金额"},  # 字段映射
        
        "suppStatementDetSuppStatementTotalSettledAmount": {"name": "供应商对账单明细总已结算金额"},  # 字段映射
        
        "suppStatementDetUnitPrice": {"name": "供应商对账单明细单价"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "供应商对账单明细实际需时": "供应商对账单明细实际需时(小时)",  # 字段含义
        
        "供应商对账单明细金额": "供应商对账单明细金额",  # 字段含义
        
        "供应商对账单明细开始时间": "供应商对账单明细开始时间",  # 字段含义
        
        "供应商对账单明细简称": "供应商对账单明细简称",  # 字段含义
        
        "供应商对账单明细完成数量": "供应商对账单明细完成数量",  # 字段含义
        
        "供应商对账单明细完成状态": "供应商对账单明细完成状态",  # 字段含义
        
        "供应商对账单明细交货日期": "供应商对账单明细交货日期",  # 字段含义
        
        "供应商对账单明细结束时间": "供应商对账单明细结束时间",  # 字段含义
        
        "供应商对账单明细PK": "供应商对账单明细PK",  # 字段含义
        
        "供应商对账单明细本币金额": "供应商对账单明细本币金额",  # 字段含义
        
        "供应商对账单明细本币完成数量": "供应商对账单明细本币完成数量",  # 字段含义
        
        "供应商对账单明细本币已开票金额": "供应商对账单明细本币已开票金额",  # 字段含义
        
        "供应商对账单明细本币其他费用": "供应商对账单明细本币其他费用",  # 字段含义
        
        "供应商对账单明细本币结算金额": "供应商对账单明细本币结算金额（本币金额+本币其他费用）",  # 字段含义
        
        "供应商对账单明细本币已结算金额": "供应商对账单明细本币已结算金额",  # 字段含义
        
        "供应商对账单明细结算金额": "供应商对账单明细结算金额（金额+其他费用）",  # 字段含义
        
        "供应商对账单明细已结算金额": "供应商对账单明细已结算金额",  # 字段含义
        
        "供应商对账单明细结算状态": "供应商对账单明细结算状态（0未结算；1部分结算；2全部结算；3终止结算）",  # 字段含义
        
        "供应商对账单明细完成数量": "供应商对账单明细完成数量",  # 字段含义
        
        "供应商对账单明细完成状态": "供应商对账单明细完成状态",  # 字段含义
        
        "供应商对账单明细币种": "供应商对账单明细币种",  # 字段含义
        
        "供应商对账单明细交货日期": "供应商对账单明细交货日期",  # 字段含义
        
        "供应商对账单明细描述": "供应商对账单明细描述",  # 字段含义
        
        "供应商对账单明细工序类型ID": "供应商对账单明细工序类型ID",  # 字段含义
        
        "供应商对账单明细生产班次ID": "供应商对账单明细生产班次ID",  # 字段含义
        
        "供应商对账单明细任务数量": "供应商对账单明细任务数量",  # 字段含义
        
        "供应商对账单明细单据日期": "供应商对账单明细单据日期",  # 字段含义
        
        "供应商对账单明细总金额": "供应商对账单明细总金额",  # 字段含义
        
        "供应商对账单明细总已开票金额": "供应商对账单明细总已开票金额",  # 字段含义
        
        "供应商对账单明细总其他费用": "供应商对账单明细总其他费用",  # 字段含义
        
        "供应商对账单明细总结算金额": "供应商对账单明细总结算金额（总金额+总其他费用）",  # 字段含义
        
        "供应商对账单明细总已结算金额": "供应商对账单明细总已结算金额",  # 字段含义
        
        "供应商对账单明细单价": "供应商对账单明细单价"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("供应商对账单明细", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@purchase_mcp.tool()  # 注册工具
def INVO_ISS_DET(access_token: str,invoIssDetFromCreateTime:str=None,invoIssDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    开票登记明细表，开票登记
    
    Args:
        access_token: 访问令牌
        
        invoIssDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        invoIssDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "INVO_ISS_DET"
    # 构建请求URL
    url = "/invo-iss-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "invoIssDetInvoIssClazz": "INVO_ISS",  # 固定参数
        
        "invoIssDetClazz": "INVO_ISS_DET",  # 固定参数
        
        
        "invoIssDetFromCreateTime": invoIssDetFromCreateTime,  # 动态参数
        
        "invoIssDetToCreateTime": invoIssDetToCreateTime,  # 动态参数
        
        "key": "INVO_ISS_DET",
        "from": invoIssDetFromCreateTime,
        "to": invoIssDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "invoIssDetActualTimeRequired": {"name": "开票登记明细表实际需时"},  # 字段映射
        
        "invoIssDetAuditStatus": {"name": "开票登记明细表审核状态"},  # 字段映射
        
        "invoIssDetBeginTime": {"name": "开票登记明细表开始时间"},  # 字段映射
        
        "invoIssDetBriefName": {"name": "开票登记明细表简称"},  # 字段映射
        
        "invoIssDetCompleteQuantity": {"name": "开票登记明细表完成数量"},  # 字段映射
        
        "invoIssDetCompleteStatus": {"name": "开票登记明细表完成状态"},  # 字段映射
        
        "invoIssDetDeliveryDate": {"name": "开票登记明细表交货日期"},  # 字段映射
        
        "invoIssDetEndTime": {"name": "开票登记明细表结束时间"},  # 字段映射
        
        "invoIssDetEndTimeRequired": {"name": "开票登记明细表最后需时"},  # 字段映射
        
        "invoIssDetId": {"name": "开票登记明细表PK"},  # 字段映射
        
        "invoIssDetInvoIssCompleteQuantity": {"name": "开票登记明细表完成数量"},  # 字段映射
        
        "invoIssDetInvoIssCompleteStatus": {"name": "开票登记明细表完成状态"},  # 字段映射
        
        "invoIssDetInvoIssExchangeRateId": {"name": "开票登记明细表币种汇率id"},  # 字段映射
        
        "invoIssDetInvoIssInvoiceBillDate": {"name": "开票登记明细表发票日期"},  # 字段映射
        
        "invoIssDetInvoIssInvoiceNo": {"name": "开票登记明细表发票号码"},  # 字段映射
        
        "invoIssDetInvoIssPaymentDate": {"name": "开票登记明细表付款日期"},  # 字段映射
        
        "invoIssDetInvoIssPlannedOutputQuantity": {"name": "开票登记明细表计划产出数量"},  # 字段映射
        
        "invoIssDetInvoIssPlannedTimeRequired": {"name": "开票登记明细表计划需时"},  # 字段映射
        
        "invoIssDetInvoIssQuantity": {"name": "开票登记明细表任务数量"},  # 字段映射
        
        "invoIssDetInvoIssSerialNumber": {"name": "开票登记明细表顺序号"},  # 字段映射
        
        "invoIssDetInvoIssSource": {"name": "开票登记明细表源"},  # 字段映射
        
        "invoIssDetInvoIssState": {"name": "开票登记明细表通用状态"},  # 字段映射
        
        "invoIssDetInvoIssTaxRate": {"name": "开票登记明细表税率"},  # 字段映射
        
        "invoIssDetInvoIssUpdater": {"name": "开票登记明细表更新人"},  # 字段映射
        
        "invoIssDetInvoIssUpdaterId": {"name": "开票登记明细表更新人ID"},  # 字段映射
        
        "invoIssDetInvoiceQuantity": {"name": "开票登记明细表开票数量"},  # 字段映射
        
        "invoIssDetLocalAmount": {"name": "开票登记明细表本币金额"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "开票登记明细表实际需时": "开票登记明细表实际需时(小时)",  # 字段含义
        
        "开票登记明细表审核状态": "开票登记明细表审核状态",  # 字段含义
        
        "开票登记明细表开始时间": "开票登记明细表开始时间",  # 字段含义
        
        "开票登记明细表简称": "开票登记明细表简称",  # 字段含义
        
        "开票登记明细表完成数量": "开票登记明细表完成数量",  # 字段含义
        
        "开票登记明细表完成状态": "开票登记明细表完成状态",  # 字段含义
        
        "开票登记明细表交货日期": "开票登记明细表交货日期",  # 字段含义
        
        "开票登记明细表结束时间": "开票登记明细表结束时间",  # 字段含义
        
        "开票登记明细表最后需时": "开票登记明细表最后需时(小时)",  # 字段含义
        
        "开票登记明细表PK": "开票登记明细表PK",  # 字段含义
        
        "开票登记明细表完成数量": "开票登记明细表完成数量",  # 字段含义
        
        "开票登记明细表完成状态": "开票登记明细表完成状态",  # 字段含义
        
        "开票登记明细表币种汇率id": "开票登记明细表币种汇率id",  # 字段含义
        
        "开票登记明细表发票日期": "开票登记明细表发票日期",  # 字段含义
        
        "开票登记明细表发票号码": "开票登记明细表发票号码(手填)",  # 字段含义
        
        "开票登记明细表付款日期": "开票登记明细表付款日期(交易日期)",  # 字段含义
        
        "开票登记明细表计划产出数量": "开票登记明细表计划产出数量",  # 字段含义
        
        "开票登记明细表计划需时": "开票登记明细表计划需时(小时)",  # 字段含义
        
        "开票登记明细表任务数量": "开票登记明细表任务数量",  # 字段含义
        
        "开票登记明细表顺序号": "开票登记明细表顺序号",  # 字段含义
        
        "开票登记明细表源": "开票登记明细表源",  # 字段含义
        
        "开票登记明细表通用状态": "开票登记明细表通用状态",  # 字段含义
        
        "开票登记明细表税率": "开票登记明细表税率",  # 字段含义
        
        "开票登记明细表更新人": "开票登记明细表更新人",  # 字段含义
        
        "开票登记明细表更新人ID": "开票登记明细表更新人ID",  # 字段含义
        
        "开票登记明细表开票数量": "开票登记明细表开票数量",  # 字段含义
        
        "开票登记明细表本币金额": "开票登记明细表本币金额"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("开票登记明细表", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@purchase_mcp.tool()  # 注册工具
def XY_USERCENTER_ORGANIZATION(access_token: str) -> str:  # 定义工具函数
    """
    供应商表，供应商
    
    Args:
        access_token: 访问令牌
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "XY_USERCENTER_ORGANIZATION"
    # 构建请求URL
    url = "/supplier/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "supplierClazz": "XY_USERCENTER_ORGANIZATION",  # 固定参数
        
        
        "key": "XY_USERCENTER_ORGANIZATION",
        "from": None,
        "to": None,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "supplierAccountPeriod": {"name": "供应商表账期"},  # 字段映射
        
        "supplierAuditDate": {"name": "供应商表审核时间"},  # 字段映射
        
        "supplierAuditStatus": {"name": "供应商表审核状态"},  # 字段映射
        
        "supplierBriefName": {"name": "供应商表简称"},  # 字段映射
        
        "supplierClassification": {"name": "供应商表供应商分类"},  # 字段映射
        
        "supplierId": {"name": "供应商表Pk"},  # 字段映射
        
        "supplierLegalName": {"name": "供应商表法人名称"},  # 字段映射
        
        "supplierLevel": {"name": "供应商表供应商级别"},  # 字段映射
        
        "supplierLocationAddress": {"name": "供应商表所在地址"},  # 字段映射
        
        "supplierLocationCity": {"name": "供应商表所在市"},  # 字段映射
        
        "supplierLocationDistrict": {"name": "供应商表所在区域"},  # 字段映射
        
        "supplierLocationProvince": {"name": "供应商表所在省"},  # 字段映射
        
        "supplierNationality": {"name": "供应商表国家"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "供应商表账期": "供应商表账期",  # 字段含义
        
        "供应商表审核时间": "供应商表审核时间",  # 字段含义
        
        "供应商表审核状态": "供应商表审核状态",  # 字段含义
        
        "供应商表简称": "供应商表简称",  # 字段含义
        
        "供应商表供应商分类": "供应商表供应商分类",  # 字段含义
        
        "供应商表Pk": "供应商表Pk",  # 字段含义
        
        "供应商表法人名称": "供应商表法人名称",  # 字段含义
        
        "供应商表供应商级别": "供应商表供应商级别",  # 字段含义
        
        "供应商表所在地址": "供应商表所在地址",  # 字段含义
        
        "供应商表所在市": "供应商表所在市",  # 字段含义
        
        "供应商表所在区域": "供应商表所在区域",  # 字段含义
        
        "供应商表所在省": "供应商表所在省",  # 字段含义
        
        "供应商表国家": "供应商表国家"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("供应商表", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@purchase_mcp.tool()  # 注册工具
def MATERIAL(access_token: str) -> str:  # 定义工具函数
    """
    物料表，物料
    
    Args:
        access_token: 访问令牌
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "MATERIAL"
    # 构建请求URL
    url = "/material/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "matClazz": "MATERIAL",  # 固定参数
        
        
        "key": "MATERIAL",
        "from": None,
        "to": None,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "matApplicationId": {"name": "物料表应用ID"},  # 字段映射
        
        "matAuditDate": {"name": "物料表审核时间"},  # 字段映射
        
        "matAuditStatus": {"name": "物料表审核状态"},  # 字段映射
        
        "matBriefName": {"name": "物料表简称"},  # 字段映射
        
        "matId": {"name": "物料表主键ID"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "物料表应用ID": "物料表应用ID",  # 字段含义
        
        "物料表审核时间": "物料表审核时间",  # 字段含义
        
        "物料表审核状态": "物料表审核状态",  # 字段含义
        
        "物料表简称": "物料表简称",  # 字段含义
        
        "物料表主键ID": "物料表主键ID"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("物料表", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  
