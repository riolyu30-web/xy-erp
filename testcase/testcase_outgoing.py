
import sys # 导入sys模块
import os # 导入os模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将上上级目录添加到系统路径
from datetime import datetime, timedelta # 导入日期时间模块
from services.auth_service import auth_login # 导入登录认证模块
from services.tool import fetch_data  # 导入工具函数
import json # 导入json模块


def OUTGOING_ORDER_DETAIL_test(access_token: str):  # 定义测试函数
    """
    测试 /outgoing-order-detail/findList
    """
    # 构建请求URL
    url = "/outgoing-order-detail/findList"  # API地址
    outgoingOrderDetailFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    outgoingOrderDetailToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "outgoingOrderDetailOutgoingOrderClazz": "OUTGOING_ORDER",  # 固定参数
        
        "outgoingOrderDetailClazz": "OUTGOING_ORDER_DETAIL",  # 固定参数
        
        
        "outgoingOrderDetailFromCreateTime": outgoingOrderDetailFromCreateTime,  # 动态参数
        
        "outgoingOrderDetailToCreateTime": outgoingOrderDetailToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "outgoingOrderDetailActualTimeRequired": {"name": "外发订单明细表实际需时"},  # 字段映射
        
        "outgoingOrderDetailAdjustmentTimeRequired": {"name": "外发订单明细表调整需时"},  # 字段映射
        
        "outgoingOrderDetailAuditStatus": {"name": "外发订单明细表审核状态"},  # 字段映射
        
        "outgoingOrderDetailBeginTime": {"name": "外发订单明细表开始时间"},  # 字段映射
        
        "outgoingOrderDetailBriefName": {"name": "外发订单明细表简称"},  # 字段映射
        
        "outgoingOrderDetailClosedStatus": {"name": "外发订单明细表结案状态"},  # 字段映射
        
        "outgoingOrderDetailCompleteQuantity": {"name": "外发订单明细表完成数量"},  # 字段映射
        
        "outgoingOrderDetailCompleteStatus": {"name": "外发订单明细表完成状态"},  # 字段映射
        
        "outgoingOrderDetailDeliveryDate": {"name": "外发订单明细表交货日期"},  # 字段映射
        
        "outgoingOrderDetailDeliveryTypeId": {"name": "外发订单明细表送货类型"},  # 字段映射
        
        "outgoingOrderDetailExternalNo": {"name": "外发订单明细表外部单号"},  # 字段映射
        
        "outgoingOrderDetailExternalState": {"name": "外发订单明细表上流程状态位"},  # 字段映射
        
        "outgoingOrderDetailId": {"name": "外发订单明细表主键ID"},  # 字段映射
        
        "outgoingOrderDetailLocUnitPrice": {"name": "外发订单明细表本币单价"},  # 字段映射
        
        "outgoingOrderDetailLocalAmount": {"name": "外发订单明细表本币金额"},  # 字段映射
        
        "outgoingOrderDetailLossQty": {"name": "外发订单明细表损耗"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderActualTimeRequired": {"name": "外发订单明细表实际需时"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderAdjustmentTimeRequired": {"name": "外发订单明细表调整需时"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderAuditDate": {"name": "外发订单明细表审核时间"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderBeginTime": {"name": "外发订单明细表开始时间"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderClosedReason": {"name": "外发订单明细表结案原因"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderClosedStatus": {"name": "外发订单明细表结案状态"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderCompleteQuantity": {"name": "外发订单明细表完成数量"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderCompleteStatus": {"name": "外发订单明细表完成状态"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderContName": {"name": "外发订单明细表联系人姓名"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderCreateTime": {"name": "外发订单明细表创建时间"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderDelMethod": {"name": "外发订单明细表配送方式"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderDeliveryDate": {"name": "外发订单明细表交货日期"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderDelvSup": {"name": "外发订单明细表送货供应商"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderPlannedOutputQuantity": {"name": "外发订单明细表计划产出数量"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderQuantity": {"name": "外发订单明细表任务数量"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderReceiptDate": {"name": "外发订单明细表单据日期"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderReceiptType": {"name": "外发订单明细表单据类型"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderSettleSupId": {"name": "外发订单明细表结算供应商ID"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderStlAmtFmt": {"name": "外发订单明细表结算金额保留小数位"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderStlPriceFmt": {"name": "外发订单明细表结算单价保留小数位"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderTotalVol": {"name": "外发订单明细表总体积"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderTotalWithTax": {"name": "外发订单明细表总费用"},  # 字段映射
        
        "outgoingOrderDetailOutgoingOrderTotalWt": {"name": "外发订单明细表总重量"},  # 字段映射
        
        "outgoingOrderDetailPlannedOutputQuantity": {"name": "外发订单明细表计划产出数量"},  # 字段映射
        
        "outgoingOrderDetailPlannedTimeRequired": {"name": "外发订单明细表计划需时"},  # 字段映射
        
        "outgoingOrderDetailQuantity": {"name": "外发订单明细表任务数量"},  # 字段映射
        
        "outgoingOrderDetailQuoteQty": {"name": "外发订单明细表报价数量"},  # 字段映射
        
        "outgoingOrderDetailSemOutstorageQuantity": {"name": "外发订单明细表半成品出库数量"},  # 字段映射
        
        "outgoingOrderDetailSemOutstorageStatus": {"name": "外发订单明细表半成品出库状态"},  # 字段映射
        
        "outgoingOrderDetailSettleAmount": {"name": "外发订单明细表结算金额"},  # 字段映射
        
        "outgoingOrderDetailSettlePrice": {"name": "外发订单明细表结算单价"},  # 字段映射
        
        "outgoingOrderDetailSourceType": {"name": "外发订单明细表来源类型"},  # 字段映射
        
        "outgoingOrderDetailSpareQty": {"name": "外发订单明细表备用数量"},  # 字段映射
        
        "outgoingOrderDetailState": {"name": "外发订单明细表通用状态"},  # 字段映射
        
        "outgoingOrderDetailStockQty": {"name": "外发订单明细表备库存数量"},  # 字段映射
        
        "outgoingOrderDetailSumQty": {"name": "外发订单明细表总数量"},  # 字段映射
        
        "outgoingOrderDetailTaxExclPrice": {"name": "外发订单明细表不含税报价单价"},  # 字段映射
        
        "outgoingOrderDetailTaxExclTotal": {"name": "外发订单明细表不含税总金额"},  # 字段映射
        
        "outgoingOrderDetailTaxExclUnitPrice": {"name": "外发订单明细表不含税单价"},  # 字段映射
        
        "outgoingOrderDetailTaxInclPrice": {"name": "外发订单明细表含税报价单价"},  # 字段映射
        
        "outgoingOrderDetailTaxInclTotal": {"name": "外发订单明细表含税总金额"},  # 字段映射
        
        "outgoingOrderDetailUnitPriceTax": {"name": "外发订单明细表含税单价"},  # 字段映射
        
        "outgoingOrderDetailUpdateTime": {"name": "外发订单明细表更新时间"},  # 字段映射
        
        "outgoingOrderDetailUsedQty": {"name": "外发订单明细表使用库存数量"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "外发订单明细表实际需时": "外发订单明细表实际需时(小时)",  # 字段含义
        
        "外发订单明细表调整需时": "外发订单明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "外发订单明细表审核状态": "外发订单明细表审核状态",  # 字段含义
        
        "外发订单明细表开始时间": "外发订单明细表开始时间",  # 字段含义
        
        "外发订单明细表简称": "外发订单明细表简称",  # 字段含义
        
        "外发订单明细表结案状态": "外发订单明细表结案状态",  # 字段含义
        
        "外发订单明细表完成数量": "外发订单明细表完成数量",  # 字段含义
        
        "外发订单明细表完成状态": "外发订单明细表完成状态",  # 字段含义
        
        "外发订单明细表交货日期": "外发订单明细表交货日期",  # 字段含义
        
        "外发订单明细表送货类型": "外发订单明细表送货类型",  # 字段含义
        
        "外发订单明细表外部单号": "外发订单明细表外部单号(例客户PO，采购送货单号)",  # 字段含义
        
        "外发订单明细表上流程状态位": "外发订单明细表上流程状态位。0-未开始；1-进行中；2-异常；3-结束；4-中止；5-关闭",  # 字段含义
        
        "外发订单明细表主键ID": "外发订单明细表主键ID",  # 字段含义
        
        "外发订单明细表本币单价": "外发订单明细表本币单价(根据币种，外币才显示)，外币不含税",  # 字段含义
        
        "外发订单明细表本币金额": "外发订单明细表本币金额(根据币种，外币才显示)，外币不含税",  # 字段含义
        
        "外发订单明细表损耗": "外发订单明细表损耗",  # 字段含义
        
        "外发订单明细表实际需时": "外发订单明细表实际需时(小时)",  # 字段含义
        
        "外发订单明细表调整需时": "外发订单明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "外发订单明细表审核时间": "外发订单明细表审核时间",  # 字段含义
        
        "外发订单明细表开始时间": "外发订单明细表开始时间",  # 字段含义
        
        "外发订单明细表结案原因": "外发订单明细表结案原因",  # 字段含义
        
        "外发订单明细表结案状态": "外发订单明细表结案状态",  # 字段含义
        
        "外发订单明细表完成数量": "外发订单明细表完成数量",  # 字段含义
        
        "外发订单明细表完成状态": "外发订单明细表完成状态",  # 字段含义
        
        "外发订单明细表联系人姓名": "外发订单明细表联系人姓名",  # 字段含义
        
        "外发订单明细表创建时间": "外发订单明细表创建时间",  # 字段含义
        
        "外发订单明细表配送方式": "外发订单明细表配送方式",  # 字段含义
        
        "外发订单明细表交货日期": "外发订单明细表交货日期",  # 字段含义
        
        "外发订单明细表送货供应商": "外发订单明细表送货供应商",  # 字段含义
        
        "外发订单明细表计划产出数量": "外发订单明细表计划产出数量",  # 字段含义
        
        "外发订单明细表任务数量": "外发订单明细表任务数量",  # 字段含义
        
        "外发订单明细表单据日期": "外发订单明细表单据日期",  # 字段含义
        
        "外发订单明细表单据类型": "外发订单明细表单据类型（一个常量值，与node里的defaultTypeId不一样，推荐使用字典）",  # 字段含义
        
        "外发订单明细表结算供应商ID": "外发订单明细表结算供应商ID",  # 字段含义
        
        "外发订单明细表结算金额保留小数位": "外发订单明细表结算金额保留小数位(默认2位，可手动变更)",  # 字段含义
        
        "外发订单明细表结算单价保留小数位": "外发订单明细表结算单价保留小数位(默认9位，可手动变更)",  # 字段含义
        
        "外发订单明细表总体积": "外发订单明细表总体积",  # 字段含义
        
        "外发订单明细表总费用": "外发订单明细表总费用(含税)",  # 字段含义
        
        "外发订单明细表总重量": "外发订单明细表总重量",  # 字段含义
        
        "外发订单明细表计划产出数量": "外发订单明细表计划产出数量",  # 字段含义
        
        "外发订单明细表计划需时": "外发订单明细表计划需时(小时)",  # 字段含义
        
        "外发订单明细表任务数量": "外发订单明细表任务数量",  # 字段含义
        
        "外发订单明细表报价数量": "外发订单明细表报价数量",  # 字段含义
        
        "外发订单明细表半成品出库数量": "外发订单明细表半成品出库数量",  # 字段含义
        
        "外发订单明细表半成品出库状态": "外发订单明细表半成品出库状态",  # 字段含义
        
        "外发订单明细表结算金额": "外发订单明细表结算金额（默认与含税总金额相等），写入库存价格字段",  # 字段含义
        
        "外发订单明细表结算单价": "外发订单明细表结算单价（默认与含税单价相等），写入库存价格字段",  # 字段含义
        
        "外发订单明细表来源类型": "外发订单明细表来源类型",  # 字段含义
        
        "外发订单明细表备用数量": "外发订单明细表备用数量",  # 字段含义
        
        "外发订单明细表通用状态": "外发订单明细表通用状态",  # 字段含义
        
        "外发订单明细表备库存数量": "外发订单明细表备库存数量",  # 字段含义
        
        "外发订单明细表总数量": "外发订单明细表总数量",  # 字段含义
        
        "外发订单明细表不含税报价单价": "外发订单明细表不含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "外发订单明细表不含税总金额": "外发订单明细表不含税总金额",  # 字段含义
        
        "外发订单明细表不含税单价": "外发订单明细表不含税单价(默认隐藏，根据计费方案转换计算得出)",  # 字段含义
        
        "外发订单明细表含税报价单价": "外发订单明细表含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "外发订单明细表含税总金额": "外发订单明细表含税总金额",  # 字段含义
        
        "外发订单明细表含税单价": "外发订单明细表含税单价(默认隐藏，根据计费方案转换计算得出)",  # 字段含义
        
        "外发订单明细表更新时间": "外发订单明细表更新时间",  # 字段含义
        
        "外发订单明细表使用库存数量": "外发订单明细表使用库存数量"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("外发订单明细表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def MAT_ARR_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /mat-arr-det/mainAndDetail/findList
    """
    # 构建请求URL
    url = "/mat-arr-det/mainAndDetail/findList"  # API地址
    matArrDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    matArrDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "matArrDetMatArrClazz": "MAT_ARR",  # 固定参数
        
        "matArrDetClazz": "MAT_ARR_DET",  # 固定参数
        
        
        "matArrDetFromCreateTime": matArrDetFromCreateTime,  # 动态参数
        
        "matArrDetToCreateTime": matArrDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "matArrDetActMaterialId": {"name": "物料到货明细表实际到货物料"},  # 字段映射
        
        "matArrDetActQuantity": {"name": "物料到货明细表实际到货数量"},  # 字段映射
        
        "matArrDetAuditDate": {"name": "物料到货明细表审核时间"},  # 字段映射
        
        "matArrDetAuditStatus": {"name": "物料到货明细表审核状态"},  # 字段映射
        
        "matArrDetBriefName": {"name": "物料到货明细表简称"},  # 字段映射
        
        "matArrDetDeliveryDate": {"name": "物料到货明细表交货日期"},  # 字段映射
        
        "matArrDetId": {"name": "物料到货明细表PK"},  # 字段映射
        
        "matArrDetLocalCurrencyTotalAmount": {"name": "物料到货明细表本币金额"},  # 字段映射
        
        "matArrDetLocalCurrencyUnitPrice": {"name": "物料到货明细表本币单价"},  # 字段映射
        
        "matArrDetMatArrActualTimeRequired": {"name": "物料到货明细表实际需时"},  # 字段映射
        
        "matArrDetMatArrAdjustmentTimeRequired": {"name": "物料到货明细表调整需时"},  # 字段映射
        
        "matArrDetMatArrAuditStatus": {"name": "物料到货明细表审核状态"},  # 字段映射
        
        "matArrDetMatArrCneeDate": {"name": "物料到货明细表收货日期"},  # 字段映射
        
        "matArrDetMatArrCneeName": {"name": "物料到货明细表收货人"},  # 字段映射
        
        "matArrDetMatArrDelOrdNum": {"name": "物料到货明细表送货单号"},  # 字段映射
        
        "matArrDetMatArrDeliveryDate": {"name": "物料到货明细表交货日期"},  # 字段映射
        
        "matArrDetMatArrInvoiceTypeTaxRate": {"name": "物料到货明细表税率"},  # 字段映射
        
        "matArrDetMatArrPlannedOutputQuantity": {"name": "物料到货明细表计划产出数量"},  # 字段映射
        
        "matArrDetMatArrPlannedTimeRequired": {"name": "物料到货明细表计划需时"},  # 字段映射
        
        "matArrDetMatArrQuantity": {"name": "物料到货明细表任务数量"},  # 字段映射
        
        "matArrDetMatArrReceiptDate": {"name": "物料到货明细表单据日期"},  # 字段映射
        
        "matArrDetMatArrReceiptSupplierId": {"name": "物料到货明细表收货供应商id"},  # 字段映射
        
        "matArrDetMatArrSetInvTyp": {"name": "物料到货明细表结算发票类型"},  # 字段映射
        
        "matArrDetMatArrSetMethod": {"name": "物料到货明细表结算方式"},  # 字段映射
        
        "matArrDetMatArrSettlementTotalAmountKeepDecimalPlace": {"name": "物料到货明细表结算金额保留小数位"},  # 字段映射
        
        "matArrDetMatArrSettlementUnitPriceKeepDecimalPlace": {"name": "物料到货明细表结算单价保留小数位"},  # 字段映射
        
        "matArrDetMatArrState": {"name": "物料到货明细表通用状态"},  # 字段映射
        
        "matArrDetPlannedOutputQuantity": {"name": "物料到货明细表计划产出数量"},  # 字段映射
        
        "matArrDetPlannedTimeRequired": {"name": "物料到货明细表计划需时"},  # 字段映射
        
        "matArrDetQuantity": {"name": "物料到货明细表任务数量"},  # 字段映射
        
        "matArrDetQuotationUnitPriceIncludingTax": {"name": "物料到货明细表含税报价单价"},  # 字段映射
        
        "matArrDetQuotationUnitPriceWithoutTax": {"name": "物料到货明细表不含税报价单价"},  # 字段映射
        
        "matArrDetRetCmpQuantity": {"name": "物料到货明细表退货完成数量"},  # 字段映射
        
        "matArrDetRetCmpStatus": {"name": "物料到货明细表退货完成状态"},  # 字段映射
        
        "matArrDetRetQuantity": {"name": "物料到货明细表退货数量"},  # 字段映射
        
        "matArrDetSerialNumber": {"name": "物料到货明细表顺序号"},  # 字段映射
        
        "matArrDetSettlementTotalAmount": {"name": "物料到货明细表结算金额"},  # 字段映射
        
        "matArrDetSettlementUnitPrice": {"name": "物料到货明细表结算单价"},  # 字段映射
        
        "matArrDetSparePartsCount": {"name": "物料到货明细表备品数"},  # 字段映射
        
        "matArrDetStatedQuantity": {"name": "物料到货明细表已对账数量"},  # 字段映射
        
        "matArrDetStatedStatus": {"name": "物料到货明细表已对账状态"},  # 字段映射
        
        "matArrDetTotTaxAmt": {"name": "物料到货明细表总含税金额"},  # 字段映射
        
        "matArrDetTotalAmountIncludingTax": {"name": "物料到货明细表含税总金额"},  # 字段映射
        
        "matArrDetTotalAmountWithoutTax": {"name": "物料到货明细表不含税总金额"},  # 字段映射
        
        "matArrDetUnitPriceIncludingTax": {"name": "物料到货明细表含税单价"},  # 字段映射
        
        "matArrDetUnitPriceWithoutTax": {"name": "物料到货明细表不含税单价"},  # 字段映射
        
        "matArrDetVersion": {"name": "物料到货明细表版本号"},  # 字段映射
        
        "matArrDetWt_diff": {"name": "物料到货明细表重量差额"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "物料到货明细表实际到货物料": "物料到货明细表实际到货物料",  # 字段含义
        
        "物料到货明细表实际到货数量": "物料到货明细表实际到货数量",  # 字段含义
        
        "物料到货明细表审核时间": "物料到货明细表审核时间",  # 字段含义
        
        "物料到货明细表审核状态": "物料到货明细表审核状态",  # 字段含义
        
        "物料到货明细表简称": "物料到货明细表简称",  # 字段含义
        
        "物料到货明细表交货日期": "物料到货明细表交货日期",  # 字段含义
        
        "物料到货明细表PK": "物料到货明细表PK",  # 字段含义
        
        "物料到货明细表本币金额": "物料到货明细表本币金额",  # 字段含义
        
        "物料到货明细表本币单价": "物料到货明细表本币单价(根据币种，外币才显示)，外币不含税",  # 字段含义
        
        "物料到货明细表实际需时": "物料到货明细表实际需时(小时)",  # 字段含义
        
        "物料到货明细表调整需时": "物料到货明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "物料到货明细表审核状态": "物料到货明细表审核状态",  # 字段含义
        
        "物料到货明细表收货日期": "物料到货明细表收货日期",  # 字段含义
        
        "物料到货明细表收货人": "物料到货明细表收货人",  # 字段含义
        
        "物料到货明细表送货单号": "物料到货明细表送货单号",  # 字段含义
        
        "物料到货明细表交货日期": "物料到货明细表交货日期",  # 字段含义
        
        "物料到货明细表税率": "物料到货明细表税率",  # 字段含义
        
        "物料到货明细表计划产出数量": "物料到货明细表计划产出数量",  # 字段含义
        
        "物料到货明细表计划需时": "物料到货明细表计划需时(小时)",  # 字段含义
        
        "物料到货明细表任务数量": "物料到货明细表任务数量",  # 字段含义
        
        "物料到货明细表单据日期": "物料到货明细表单据日期",  # 字段含义
        
        "物料到货明细表收货供应商id": "物料到货明细表收货供应商id",  # 字段含义
        
        "物料到货明细表结算发票类型": "物料到货明细表结算发票类型",  # 字段含义
        
        "物料到货明细表结算方式": "物料到货明细表结算方式",  # 字段含义
        
        "物料到货明细表结算金额保留小数位": "物料到货明细表结算金额保留小数位(默认2位，可手动变更)",  # 字段含义
        
        "物料到货明细表结算单价保留小数位": "物料到货明细表结算单价保留小数位(默认9位，可手动变更)",  # 字段含义
        
        "物料到货明细表通用状态": "物料到货明细表通用状态",  # 字段含义
        
        "物料到货明细表计划产出数量": "物料到货明细表计划产出数量",  # 字段含义
        
        "物料到货明细表计划需时": "物料到货明细表计划需时(小时)",  # 字段含义
        
        "物料到货明细表任务数量": "物料到货明细表任务数量",  # 字段含义
        
        "物料到货明细表含税报价单价": "物料到货明细表含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "物料到货明细表不含税报价单价": "物料到货明细表不含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "物料到货明细表退货完成数量": "物料到货明细表退货完成数量",  # 字段含义
        
        "物料到货明细表退货完成状态": "物料到货明细表退货完成状态",  # 字段含义
        
        "物料到货明细表退货数量": "物料到货明细表退货数量",  # 字段含义
        
        "物料到货明细表顺序号": "物料到货明细表顺序号",  # 字段含义
        
        "物料到货明细表结算金额": "物料到货明细表结算金额（默认与含税总金额相等），写入库存价格字段",  # 字段含义
        
        "物料到货明细表结算单价": "物料到货明细表结算单价（默认与含税单价相等），写入库存价格字段",  # 字段含义
        
        "物料到货明细表备品数": "物料到货明细表备品数",  # 字段含义
        
        "物料到货明细表已对账数量": "物料到货明细表已对账数量",  # 字段含义
        
        "物料到货明细表已对账状态": "物料到货明细表已对账状态",  # 字段含义
        
        "物料到货明细表总含税金额": "物料到货明细表总含税金额",  # 字段含义
        
        "物料到货明细表含税总金额": "物料到货明细表含税总金额",  # 字段含义
        
        "物料到货明细表不含税总金额": "物料到货明细表不含税总金额",  # 字段含义
        
        "物料到货明细表含税单价": "物料到货明细表含税单价(默认隐藏，根据计费方案转换计算得出)",  # 字段含义
        
        "物料到货明细表不含税单价": "物料到货明细表不含税单价(默认隐藏，根据计费方案转换计算得出)",  # 字段含义
        
        "物料到货明细表版本号": "物料到货明细表版本号",  # 字段含义
        
        "物料到货明细表重量差额": "物料到货明细表重量差额"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("物料到货明细表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def MANU_STATEMENT_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /manu-statement-det/findList
    """
    # 构建请求URL
    url = "/manu-statement-det/findList"  # API地址
    manuStatementDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    manuStatementDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "manuStatementDetManuStatementClazz": "MANU_STATEMENT ",  # 固定参数
        
        "manuStatementDetClazz": "MANU_STATEMENT_DET ",  # 固定参数
        
        
        "manuStatementDetFromCreateTime": manuStatementDetFromCreateTime,  # 动态参数
        
        "manuStatementDetToCreateTime": manuStatementDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "manuStatementDetAdjustmentTimeRequired": {"name": "加工商对账单明细调整需时"},  # 字段映射
        
        "manuStatementDetAmount": {"name": "加工商对账单明细金额"},  # 字段映射
        
        "manuStatementDetAvailableScheduleId": {"name": "加工商对账单明细可用日程id"},  # 字段映射
        
        "manuStatementDetBeginTime": {"name": "加工商对账单明细开始时间"},  # 字段映射
        
        "manuStatementDetBriefName": {"name": "加工商对账单明细简称"},  # 字段映射
        
        "manuStatementDetComment": {"name": "加工商对账单明细评论"},  # 字段映射
        
        "manuStatementDetCompleteQuantity": {"name": "加工商对账单明细完成数量"},  # 字段映射
        
        "manuStatementDetCompleteStatus": {"name": "加工商对账单明细完成状态"},  # 字段映射
        
        "manuStatementDetDeliveryDate": {"name": "加工商对账单明细交货日期"},  # 字段映射
        
        "manuStatementDetDescription": {"name": "加工商对账单明细描述"},  # 字段映射
        
        "manuStatementDetEndTimeRequired": {"name": "加工商对账单明细最后需时"},  # 字段映射
        
        "manuStatementDetEquipmentId": {"name": "加工商对账单明细设备id"},  # 字段映射
        
        "manuStatementDetExchangeRateId": {"name": "加工商对账单明细币种汇率id"},  # 字段映射
        
        "manuStatementDetId": {"name": "加工商对账单明细PK"},  # 字段映射
        
        "manuStatementDetManuStatementBeginTime": {"name": "加工商对账单明细开始时间"},  # 字段映射
        
        "manuStatementDetManuStatementBriefName": {"name": "加工商对账单明细简称"},  # 字段映射
        
        "manuStatementDetManuStatementCompleteQuantity": {"name": "加工商对账单明细完成数量"},  # 字段映射
        
        "manuStatementDetManuStatementCompleteStatus": {"name": "加工商对账单明细完成状态"},  # 字段映射
        
        "manuStatementDetManuStatementCreateTime": {"name": "加工商对账单明细创建时间"},  # 字段映射
        
        "manuStatementDetManuStatementDeliveryDate": {"name": "加工商对账单明细交货日期"},  # 字段映射
        
        "manuStatementDetManuStatementLocCompleteQuantity": {"name": "加工商对账单明细本币完成数量"},  # 字段映射
        
        "manuStatementDetManuStatementLocTotalAmount": {"name": "加工商对账单明细本币总金额"},  # 字段映射
        
        "manuStatementDetManuStatementLocTotalInvoicedAmount": {"name": "加工商对账单明细本币总已开票金额"},  # 字段映射
        
        "manuStatementDetManuStatementLocTotalOtherExpense": {"name": "加工商对账单明细本币总其他费用"},  # 字段映射
        
        "manuStatementDetManuStatementPlannedOutputQuantity": {"name": "加工商对账单明细计划产出数量"},  # 字段映射
        
        "manuStatementDetManuStatementPlannedTimeRequired": {"name": "加工商对账单明细计划需时"},  # 字段映射
        
        "manuStatementDetManuStatementProductionProcessesTypeId": {"name": "加工商对账单明细工序类型ID"},  # 字段映射
        
        "manuStatementDetManuStatementProductionShiftId": {"name": "加工商对账单明细生产班次ID"},  # 字段映射
        
        "manuStatementDetManuStatementQuantity": {"name": "加工商对账单明细任务数量"},  # 字段映射
        
        "manuStatementDetManuStatementReceiptDate": {"name": "加工商对账单明细单据日期"},  # 字段映射
        
        "manuStatementDetManuStatementTotalInvoicedAmount": {"name": "加工商对账单明细总已开票金额"},  # 字段映射
        
        "manuStatementDetManuStatementTotalOtherExpense": {"name": "加工商对账单明细总其他费用"},  # 字段映射
        
        "manuStatementDetManuStatementTotalSettleAmount": {"name": "加工商对账单明细总结算金额"},  # 字段映射
        
        "manuStatementDetManuStatementTotalSettledAmount": {"name": "加工商对账单明细总已结算金额"},  # 字段映射
        
        "manuStatementDetOtherExpense": {"name": "加工商对账单明细其他费用"},  # 字段映射
        
        "manuStatementDetPlannedOutputQuantity": {"name": "加工商对账单明细计划产出数量"},  # 字段映射
        
        "manuStatementDetQuantity": {"name": "加工商对账单明细任务数量"},  # 字段映射
        
        "manuStatementDetSettleAmount": {"name": "加工商对账单明细结算金额"},  # 字段映射
        
        "manuStatementDetSettledAmount": {"name": "加工商对账单明细已结算金额"},  # 字段映射
        
        "manuStatementDetSettledState": {"name": "加工商对账单明细结算状态"},  # 字段映射
        
        "manuStatementDetUnitPrice": {"name": "加工商对账单明细单价"},  # 字段映射
        
        "manuStatementDetUpdateTime": {"name": "加工商对账单明细更新时间"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "加工商对账单明细调整需时": "加工商对账单明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "加工商对账单明细金额": "加工商对账单明细金额",  # 字段含义
        
        "加工商对账单明细可用日程id": "加工商对账单明细可用日程id",  # 字段含义
        
        "加工商对账单明细开始时间": "加工商对账单明细开始时间",  # 字段含义
        
        "加工商对账单明细简称": "加工商对账单明细简称",  # 字段含义
        
        "加工商对账单明细评论": "加工商对账单明细评论",  # 字段含义
        
        "加工商对账单明细完成数量": "加工商对账单明细完成数量",  # 字段含义
        
        "加工商对账单明细完成状态": "加工商对账单明细完成状态",  # 字段含义
        
        "加工商对账单明细交货日期": "加工商对账单明细交货日期",  # 字段含义
        
        "加工商对账单明细描述": "加工商对账单明细描述",  # 字段含义
        
        "加工商对账单明细最后需时": "加工商对账单明细最后需时(小时)",  # 字段含义
        
        "加工商对账单明细设备id": "加工商对账单明细设备id",  # 字段含义
        
        "加工商对账单明细币种汇率id": "加工商对账单明细币种汇率id",  # 字段含义
        
        "加工商对账单明细PK": "加工商对账单明细PK",  # 字段含义
        
        "加工商对账单明细开始时间": "加工商对账单明细开始时间",  # 字段含义
        
        "加工商对账单明细简称": "加工商对账单明细简称",  # 字段含义
        
        "加工商对账单明细完成数量": "加工商对账单明细完成数量",  # 字段含义
        
        "加工商对账单明细完成状态": "加工商对账单明细完成状态",  # 字段含义
        
        "加工商对账单明细创建时间": "加工商对账单明细创建时间",  # 字段含义
        
        "加工商对账单明细交货日期": "加工商对账单明细交货日期",  # 字段含义
        
        "加工商对账单明细本币完成数量": "加工商对账单明细本币完成数量",  # 字段含义
        
        "加工商对账单明细本币总金额": "加工商对账单明细本币总金额",  # 字段含义
        
        "加工商对账单明细本币总已开票金额": "加工商对账单明细本币总已开票金额",  # 字段含义
        
        "加工商对账单明细本币总其他费用": "加工商对账单明细本币总其他费用",  # 字段含义
        
        "加工商对账单明细计划产出数量": "加工商对账单明细计划产出数量",  # 字段含义
        
        "加工商对账单明细计划需时": "加工商对账单明细计划需时(小时)",  # 字段含义
        
        "加工商对账单明细工序类型ID": "加工商对账单明细工序类型ID",  # 字段含义
        
        "加工商对账单明细生产班次ID": "加工商对账单明细生产班次ID",  # 字段含义
        
        "加工商对账单明细任务数量": "加工商对账单明细任务数量",  # 字段含义
        
        "加工商对账单明细单据日期": "加工商对账单明细单据日期",  # 字段含义
        
        "加工商对账单明细总已开票金额": "加工商对账单明细总已开票金额",  # 字段含义
        
        "加工商对账单明细总其他费用": "加工商对账单明细总其他费用",  # 字段含义
        
        "加工商对账单明细总结算金额": "加工商对账单明细总结算金额（总金额+总其他费用）",  # 字段含义
        
        "加工商对账单明细总已结算金额": "加工商对账单明细总已结算金额",  # 字段含义
        
        "加工商对账单明细其他费用": "加工商对账单明细其他费用",  # 字段含义
        
        "加工商对账单明细计划产出数量": "加工商对账单明细计划产出数量",  # 字段含义
        
        "加工商对账单明细任务数量": "加工商对账单明细任务数量",  # 字段含义
        
        "加工商对账单明细结算金额": "加工商对账单明细结算金额（金额+其他费用）",  # 字段含义
        
        "加工商对账单明细已结算金额": "加工商对账单明细已结算金额",  # 字段含义
        
        "加工商对账单明细结算状态": "加工商对账单明细结算状态（0未结算；1部分结算；2全部结算；3终止结算）",  # 字段含义
        
        "加工商对账单明细单价": "加工商对账单明细单价",  # 字段含义
        
        "加工商对账单明细更新时间": "加工商对账单明细更新时间"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("加工商对账单明细", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def XY_USERCENTER_ORGANIZATION_test(access_token: str):  # 定义测试函数
    """
    测试 /supplier/findList
    """
    # 构建请求URL
    url = "/supplier/findList"  # API地址

    # 构建请求体数据
    data = {
        
        "supplierClazz": "XY_USERCENTER_ORGANIZATION",  # 固定参数
        
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "supplierAccountPeriod": {"name": "供应商表账期"},  # 字段映射
        
        "supplierAreaId": {"name": "供应商表区域id"},  # 字段映射
        
        "supplierAuditDate": {"name": "供应商表审核时间"},  # 字段映射
        
        "supplierBriefName": {"name": "供应商表简称"},  # 字段映射
        
        "supplierBusinessScope": {"name": "供应商表经营范围"},  # 字段映射
        
        "supplierClassification": {"name": "供应商表供应商分类"},  # 字段映射
        
        "supplierCreditLimit": {"name": "供应商表信用限额"},  # 字段映射
        
        "supplierDefaultDeliveryType": {"name": "供应商表默认送货类型"},  # 字段映射
        
        "supplierDefaultInvoiceTypeTaxRate": {"name": "供应商表发票类型税率"},  # 字段映射
        
        "supplierId": {"name": "供应商表Pk"},  # 字段映射
        
        "supplierLegalName": {"name": "供应商表法人名称"},  # 字段映射
        
        "supplierLevel": {"name": "供应商表供应商级别"},  # 字段映射
        
        "supplierLocationCity": {"name": "供应商表所在市"},  # 字段映射
        
        "supplierLocationDistrict": {"name": "供应商表所在区域"},  # 字段映射
        
        "supplierLocationProvince": {"name": "供应商表所在省"},  # 字段映射
        
        "supplierNationality": {"name": "供应商表国家"},  # 字段映射
        
        "supplierReconciliationDate": {"name": "供应商表结账日"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "供应商表账期": "供应商表账期",  # 字段含义
        
        "供应商表区域id": "供应商表区域id",  # 字段含义
        
        "供应商表审核时间": "供应商表审核时间",  # 字段含义
        
        "供应商表简称": "供应商表简称",  # 字段含义
        
        "供应商表经营范围": "供应商表经营范围",  # 字段含义
        
        "供应商表供应商分类": "供应商表供应商分类",  # 字段含义
        
        "供应商表信用限额": "供应商表信用限额",  # 字段含义
        
        "供应商表默认送货类型": "供应商表默认送货类型",  # 字段含义
        
        "供应商表发票类型税率": "供应商表发票类型税率",  # 字段含义
        
        "供应商表Pk": "供应商表Pk",  # 字段含义
        
        "供应商表法人名称": "供应商表法人名称",  # 字段含义
        
        "供应商表供应商级别": "供应商表供应商级别",  # 字段含义
        
        "供应商表所在市": "供应商表所在市",  # 字段含义
        
        "供应商表所在区域": "供应商表所在区域",  # 字段含义
        
        "供应商表所在省": "供应商表所在省",  # 字段含义
        
        "供应商表国家": "供应商表国家",  # 字段含义
        
        "供应商表结账日": "供应商表结账日"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("供应商表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)


if __name__ == "__main__":
    access_token = auth_login()  # 获取访问令牌
    
    OUTGOING_ORDER_DETAIL_test(access_token)  # 调用测试函数
    
    MAT_ARR_DET_test(access_token)  # 调用测试函数
    
    MANU_STATEMENT_DET_test(access_token)  # 调用测试函数
    
    XY_USERCENTER_ORGANIZATION_test(access_token)  # 调用测试函数
    