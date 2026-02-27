
import sys # 导入sys模块
import os # 导入os模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将上上级目录添加到系统路径
from datetime import datetime, timedelta # 导入日期时间模块
from services.auth_service import auth_login # 导入登录认证模块
from services.tool import fetch_data  # 导入工具函数
import json # 导入json模块


def biz_order_detail_test(access_token: str):  # 定义测试函数
    """
    测试 /biz-order-detail/findList
    """
    # 构建请求URL
    url = "/biz-order-detail/findList"  # API地址
    bizOrderDetailFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    bizOrderDetailToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "bizOrderDetailBizOrderClazz": "BUSINESS_ORDER",  # 固定参数
        
        "bizOrderDetailClazz": "BUSINESS_ORDER_DETAIL",  # 固定参数
        
        
        "bizOrderDetailFromCreateTime": bizOrderDetailFromCreateTime,  # 动态参数
        
        "bizOrderDetailToCreateTime": bizOrderDetailToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "bizOrderDetailActualTimeRequired": {"name": "业务订单明细实际需时"},  # 字段映射
        
        "bizOrderDetailAddress": {"name": "业务订单明细详细地址"},  # 字段映射
        
        "bizOrderDetailAdjustmentTimeRequired": {"name": "业务订单明细调整需时"},  # 字段映射
        
        "bizOrderDetailAssignStatus": {"name": "业务订单明细指派状态"},  # 字段映射
        
        "bizOrderDetailAuditDate": {"name": "业务订单明细审核时间"},  # 字段映射
        
        "bizOrderDetailAuditStatus": {"name": "业务订单明细审核状态"},  # 字段映射
        
        "bizOrderDetailBizOrderBeginTime": {"name": "业务订单明细开始时间"},  # 字段映射
        
        "bizOrderDetailBizOrderBriefName": {"name": "业务订单明细简称"},  # 字段映射
        
        "bizOrderDetailBizOrderClosedReason": {"name": "业务订单明细结案原因"},  # 字段映射
        
        "bizOrderDetailBizOrderClosedStatus": {"name": "业务订单明细结案状态"},  # 字段映射
        
        "bizOrderDetailBizOrderCompleteQuantity": {"name": "业务订单明细完成数量"},  # 字段映射
        
        "bizOrderDetailBizOrderCompleteStatus": {"name": "业务订单明细完成状态"},  # 字段映射
        
        "bizOrderDetailBizOrderContName": {"name": "业务订单明细联系人姓名"},  # 字段映射
        
        "bizOrderDetailBizOrderCur": {"name": "业务订单明细币种"},  # 字段映射
        
        "bizOrderDetailBizOrderCurRate": {"name": "业务订单明细汇率"},  # 字段映射
        
        "bizOrderDetailBizOrderDeliveryDate": {"name": "业务订单明细交货日期"},  # 字段映射
        
        "bizOrderDetailBizOrderDelvCust": {"name": "业务订单明细送货客户"},  # 字段映射
        
        "bizOrderDetailBizOrderIsUrgent": {"name": "业务订单明细是否加急"},  # 字段映射
        
        "bizOrderDetailBizOrderMaterialId": {"name": "业务订单明细物料id"},  # 字段映射
        
        "bizOrderDetailBizOrderPlannedTimeRequired": {"name": "业务订单明细计划需时"},  # 字段映射
        
        "bizOrderDetailBizOrderPrintTimes": {"name": "业务订单明细打印次数"},  # 字段映射
        
        "bizOrderDetailBizOrderPriority": {"name": "业务订单明细优先级"},  # 字段映射
        
        "bizOrderDetailBizOrderStlAmtFmt": {"name": "业务订单明细结算金额保留小数位"},  # 字段映射
        
        "bizOrderDetailBizOrderStlFee": {"name": "业务订单明细结算费用"},  # 字段映射
        
        "bizOrderDetailBizOrderTaxRt": {"name": "业务订单明细税率"},  # 字段映射
        
        "bizOrderDetailBizOrderTotalFeeNt": {"name": "业务订单明细总费用"},  # 字段映射
        
        "bizOrderDetailBizOrderTotalVol": {"name": "业务订单明细总体积"},  # 字段映射
        
        "bizOrderDetailBizOrderTotalWithTax": {"name": "业务订单明细总费用"},  # 字段映射
        
        "bizOrderDetailBizOrderTotalWt": {"name": "业务订单明细总重量"},  # 字段映射
        
        "bizOrderDetailCompleteStatus": {"name": "业务订单明细完成状态"},  # 字段映射
        
        "bizOrderDetailDeliveryDate": {"name": "业务订单明细交货日期"},  # 字段映射
        
        "bizOrderDetailDeliveryTypeId": {"name": "业务订单明细送货类型"},  # 字段映射
        
        "bizOrderDetailEndTimeRequired": {"name": "业务订单明细最后需时"},  # 字段映射
        
        "bizOrderDetailEngName": {"name": "业务订单明细英文名称"},  # 字段映射
        
        "bizOrderDetailExpectedDate": {"name": "业务订单明细预计交期"},  # 字段映射
        
        "bizOrderDetailExtMatBarcode": {"name": "业务订单明细外部物料条码"},  # 字段映射
        
        "bizOrderDetailExtMatCode": {"name": "业务订单明细外部物料编码"},  # 字段映射
        
        "bizOrderDetailExtMatName": {"name": "业务订单明细外部物料名称"},  # 字段映射
        
        "bizOrderDetailId": {"name": "业务订单明细主键ID"},  # 字段映射
        
        "bizOrderDetailInvoRecIssQuantity": {"name": "业务订单明细开/收票数量"},  # 字段映射
        
        "bizOrderDetailLocUnitPrice": {"name": "业务订单明细本币单价"},  # 字段映射
        
        "bizOrderDetailLocalAmount": {"name": "业务订单明细本币金额"},  # 字段映射
        
        "bizOrderDetailLossQty": {"name": "业务订单明细损耗"},  # 字段映射
        
        "bizOrderDetailMatCat": {"name": "业务订单明细物料分类ID"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "业务订单明细实际需时": "业务订单明细实际需时(小时)",  # 字段含义
        
        "业务订单明细详细地址": "业务订单明细详细地址",  # 字段含义
        
        "业务订单明细调整需时": "业务订单明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "业务订单明细指派状态": "业务订单明细指派状态",  # 字段含义
        
        "业务订单明细审核时间": "业务订单明细审核时间",  # 字段含义
        
        "业务订单明细审核状态": "业务订单明细审核状态",  # 字段含义
        
        "业务订单明细开始时间": "业务订单明细开始时间",  # 字段含义
        
        "业务订单明细简称": "业务订单明细简称",  # 字段含义
        
        "业务订单明细结案原因": "业务订单明细结案原因",  # 字段含义
        
        "业务订单明细结案状态": "业务订单明细结案状态",  # 字段含义
        
        "业务订单明细完成数量": "业务订单明细完成数量",  # 字段含义
        
        "业务订单明细完成状态": "业务订单明细完成状态",  # 字段含义
        
        "业务订单明细联系人姓名": "业务订单明细联系人姓名",  # 字段含义
        
        "业务订单明细币种": "业务订单明细币种",  # 字段含义
        
        "业务订单明细汇率": "业务订单明细汇率",  # 字段含义
        
        "业务订单明细交货日期": "业务订单明细交货日期",  # 字段含义
        
        "业务订单明细送货客户": "业务订单明细送货客户",  # 字段含义
        
        "业务订单明细是否加急": "业务订单明细是否加急",  # 字段含义
        
        "业务订单明细物料id": "业务订单明细物料id",  # 字段含义
        
        "业务订单明细计划需时": "业务订单明细计划需时(小时)",  # 字段含义
        
        "业务订单明细打印次数": "业务订单明细打印次数",  # 字段含义
        
        "业务订单明细优先级": "业务订单明细优先级",  # 字段含义
        
        "业务订单明细结算金额保留小数位": "业务订单明细结算金额保留小数位(默认2位，可手动变更)",  # 字段含义
        
        "业务订单明细结算费用": "业务订单明细结算费用（默认与含税总金额相等)",  # 字段含义
        
        "业务订单明细税率": "业务订单明细税率",  # 字段含义
        
        "业务订单明细总费用": "业务订单明细总费用(不含税)",  # 字段含义
        
        "业务订单明细总体积": "业务订单明细总体积",  # 字段含义
        
        "业务订单明细总费用": "业务订单明细总费用(含税)",  # 字段含义
        
        "业务订单明细总重量": "业务订单明细总重量",  # 字段含义
        
        "业务订单明细完成状态": "业务订单明细完成状态",  # 字段含义
        
        "业务订单明细交货日期": "业务订单明细交货日期",  # 字段含义
        
        "业务订单明细送货类型": "业务订单明细送货类型",  # 字段含义
        
        "业务订单明细最后需时": "业务订单明细最后需时(小时)",  # 字段含义
        
        "业务订单明细英文名称": "业务订单明细英文名称",  # 字段含义
        
        "业务订单明细预计交期": "业务订单明细预计交期",  # 字段含义
        
        "业务订单明细外部物料条码": "业务订单明细外部物料条码(BarCode)",  # 字段含义
        
        "业务订单明细外部物料编码": "业务订单明细外部物料编码(例客户产品编码)",  # 字段含义
        
        "业务订单明细外部物料名称": "业务订单明细外部物料名称(例客户产品名称)",  # 字段含义
        
        "业务订单明细主键ID": "业务订单明细主键ID",  # 字段含义
        
        "业务订单明细开/收票数量": "业务订单明细开/收票数量",  # 字段含义
        
        "业务订单明细本币单价": "业务订单明细本币单价(根据币种，外币才显示)，外币不含税",  # 字段含义
        
        "业务订单明细本币金额": "业务订单明细本币金额(根据币种，外币才显示)，外币不含税",  # 字段含义
        
        "业务订单明细损耗": "业务订单明细损耗",  # 字段含义
        
        "业务订单明细物料分类ID": "业务订单明细物料分类ID"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("业务订单明细", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def prd_oapy_det_test(access_token: str):  # 定义测试函数
    """
    测试 /prd-oapy-det/findList
    """
    # 构建请求URL
    url = "/prd-oapy-det/findList"  # API地址
    prdOApyDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    prdOApyDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "prdOApyDetPrdOApyClazz": "PRD_O_APY",  # 固定参数
        
        "prdOApyDetClazz": "PRD_O_APY_DET",  # 固定参数
        
        
        "prdOApyDetFromCreateTime": prdOApyDetFromCreateTime,  # 动态参数
        
        "prdOApyDetToCreateTime": prdOApyDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "prdOApyDetActualTimeRequired": {"name": "成品出库申请明细实际需时"},  # 字段映射
        
        "prdOApyDetAdjustmentTimeRequired": {"name": "成品出库申请明细调整需时"},  # 字段映射
        
        "prdOApyDetAuditDate": {"name": "成品出库申请明细审核时间"},  # 字段映射
        
        "prdOApyDetAuditStatus": {"name": "成品出库申请明细审核状态"},  # 字段映射
        
        "prdOApyDetBeginTime": {"name": "成品出库申请明细开始时间"},  # 字段映射
        
        "prdOApyDetBriefName": {"name": "成品出库申请明细简称"},  # 字段映射
        
        "prdOApyDetCompleteQuantity": {"name": "成品出库申请明细完成数量"},  # 字段映射
        
        "prdOApyDetCompleteStatus": {"name": "成品出库申请明细完成状态"},  # 字段映射
        
        "prdOApyDetConsigneeName": {"name": "成品出库申请明细收货单位名称"},  # 字段映射
        
        "prdOApyDetCreateTime": {"name": "成品出库申请明细创建时间"},  # 字段映射
        
        "prdOApyDetCustContact": {"name": "成品出库申请明细收货人"},  # 字段映射
        
        "prdOApyDetCustContactCellPhone": {"name": "成品出库申请明细手机号"},  # 字段映射
        
        "prdOApyDetCustContactPhone": {"name": "成品出库申请明细电话"},  # 字段映射
        
        "prdOApyDetCustDeliverAddress": {"name": "成品出库申请明细送货地址"},  # 字段映射
        
        "prdOApyDetDeliveryDate": {"name": "成品出库申请明细交货日期"},  # 字段映射
        
        "prdOApyDetDescription": {"name": "成品出库申请明细描述"},  # 字段映射
        
        "prdOApyDetEndTime": {"name": "成品出库申请明细结束时间"},  # 字段映射
        
        "prdOApyDetEndTimeRequired": {"name": "成品出库申请明细最后需时"},  # 字段映射
        
        "prdOApyDetEngName": {"name": "成品出库申请明细英文名称"},  # 字段映射
        
        "prdOApyDetExchangeRateId": {"name": "成品出库申请明细币种汇率id"},  # 字段映射
        
        "prdOApyDetGiftQuantity": {"name": "成品出库申请明细赠品数量"},  # 字段映射
        
        "prdOApyDetId": {"name": "成品出库申请明细PK"},  # 字段映射
        
        "prdOApyDetInvTypeTaxRateId": {"name": "成品出库申请明细发票税率id"},  # 字段映射
        
        "prdOApyDetPlannedTimeRequired": {"name": "成品出库申请明细计划需时"},  # 字段映射
        
        "prdOApyDetPrdOApyActualTimeRequired": {"name": "成品出库申请明细实际需时"},  # 字段映射
        
        "prdOApyDetPrdOApyAdjustmentTimeRequired": {"name": "成品出库申请明细调整需时"},  # 字段映射
        
        "prdOApyDetPrdOApyBeginTime": {"name": "成品出库申请明细开始时间"},  # 字段映射
        
        "prdOApyDetPrdOApyBriefName": {"name": "成品出库申请明细简称"},  # 字段映射
        
        "prdOApyDetPrdOApyClosedReason": {"name": "成品出库申请明细结案原因"},  # 字段映射
        
        "prdOApyDetPrdOApyClosedStatus": {"name": "成品出库申请明细结案状态"},  # 字段映射
        
        "prdOApyDetPrdOApyComment": {"name": "成品出库申请明细评论"},  # 字段映射
        
        "prdOApyDetPrdOApyCompleteQuantity": {"name": "成品出库申请明细完成数量"},  # 字段映射
        
        "prdOApyDetPrdOApyCompleteStatus": {"name": "成品出库申请明细完成状态"},  # 字段映射
        
        "prdOApyDetPrdOApyCreateTime": {"name": "成品出库申请明细创建时间"},  # 字段映射
        
        "prdOApyDetPrdOApyDeliveryDate": {"name": "成品出库申请明细交货日期"},  # 字段映射
        
        "prdOApyDetPrdOApyEngName": {"name": "成品出库申请明细英文名称"},  # 字段映射
        
        "prdOApyDetPrdOApyGropeCode": {"name": "成品出库申请明细搜索码"},  # 字段映射
        
        "prdOApyDetPrdOApyPlannedTimeRequired": {"name": "成品出库申请明细计划需时"},  # 字段映射
        
        "prdOApyDetPrdOApyProductionShiftId": {"name": "成品出库申请明细生产班次ID"},  # 字段映射
        
        "prdOApyDetPrdOApyQuantity": {"name": "成品出库申请明细任务数量"},  # 字段映射
        
        "prdOApyDetPrdSalGiftQuantity": {"name": "成品出库申请明细成品销货赠品完成数量"},  # 字段映射
        
        "prdOApyDetPrdSalGiftStatus": {"name": "成品出库申请明细成品销货赠品完成状态"},  # 字段映射
        
        "prdOApyDetPrdSalQuantity": {"name": "成品出库申请明细成品销货完成数量"},  # 字段映射
        
        "prdOApyDetPrdSalSpareQuantity": {"name": "成品出库申请明细成品销货备品完成数量"},  # 字段映射
        
        "prdOApyDetPrdSalSpareStatus": {"name": "成品出库申请明细成品销货备品完成状态"},  # 字段映射
        
        "prdOApyDetPrdSalStatus": {"name": "成品出库申请明细成品销货完成状态"},  # 字段映射
        
        "prdOApyDetTotalAmountInTax": {"name": "成品出库申请明细含税金额"},  # 字段映射
        
        "prdOApyDetTotalAmountWitTax": {"name": "成品出库申请明细不含税金额"},  # 字段映射
        
        "prdOApyDetTransPlanQuantity": {"name": "成品出库申请明细运输计划完成数量"},  # 字段映射
        
        "prdOApyDetTransPlanStatus": {"name": "成品出库申请明细运输计划完成状态"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "成品出库申请明细实际需时": "成品出库申请明细实际需时(小时)",  # 字段含义
        
        "成品出库申请明细调整需时": "成品出库申请明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "成品出库申请明细审核时间": "成品出库申请明细审核时间",  # 字段含义
        
        "成品出库申请明细审核状态": "成品出库申请明细审核状态",  # 字段含义
        
        "成品出库申请明细开始时间": "成品出库申请明细开始时间",  # 字段含义
        
        "成品出库申请明细简称": "成品出库申请明细简称",  # 字段含义
        
        "成品出库申请明细完成数量": "成品出库申请明细完成数量",  # 字段含义
        
        "成品出库申请明细完成状态": "成品出库申请明细完成状态",  # 字段含义
        
        "成品出库申请明细收货单位名称": "成品出库申请明细收货单位名称",  # 字段含义
        
        "成品出库申请明细创建时间": "成品出库申请明细创建时间",  # 字段含义
        
        "成品出库申请明细收货人": "成品出库申请明细收货人(客户联系人)",  # 字段含义
        
        "成品出库申请明细手机号": "成品出库申请明细手机号(客户联系人手机号)",  # 字段含义
        
        "成品出库申请明细电话": "成品出库申请明细电话(客户联系人电话)",  # 字段含义
        
        "成品出库申请明细送货地址": "成品出库申请明细送货地址(客户送货地址)",  # 字段含义
        
        "成品出库申请明细交货日期": "成品出库申请明细交货日期",  # 字段含义
        
        "成品出库申请明细描述": "成品出库申请明细描述",  # 字段含义
        
        "成品出库申请明细结束时间": "成品出库申请明细结束时间",  # 字段含义
        
        "成品出库申请明细最后需时": "成品出库申请明细最后需时(小时)",  # 字段含义
        
        "成品出库申请明细英文名称": "成品出库申请明细英文名称",  # 字段含义
        
        "成品出库申请明细币种汇率id": "成品出库申请明细币种汇率id",  # 字段含义
        
        "成品出库申请明细赠品数量": "成品出库申请明细赠品数量",  # 字段含义
        
        "成品出库申请明细PK": "成品出库申请明细PK",  # 字段含义
        
        "成品出库申请明细发票税率id": "成品出库申请明细发票税率id",  # 字段含义
        
        "成品出库申请明细计划需时": "成品出库申请明细计划需时(小时)",  # 字段含义
        
        "成品出库申请明细实际需时": "成品出库申请明细实际需时(小时)",  # 字段含义
        
        "成品出库申请明细调整需时": "成品出库申请明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "成品出库申请明细开始时间": "成品出库申请明细开始时间",  # 字段含义
        
        "成品出库申请明细简称": "成品出库申请明细简称",  # 字段含义
        
        "成品出库申请明细结案原因": "成品出库申请明细结案原因",  # 字段含义
        
        "成品出库申请明细结案状态": "成品出库申请明细结案状态",  # 字段含义
        
        "成品出库申请明细评论": "成品出库申请明细评论",  # 字段含义
        
        "成品出库申请明细完成数量": "成品出库申请明细完成数量",  # 字段含义
        
        "成品出库申请明细完成状态": "成品出库申请明细完成状态",  # 字段含义
        
        "成品出库申请明细创建时间": "成品出库申请明细创建时间",  # 字段含义
        
        "成品出库申请明细交货日期": "成品出库申请明细交货日期",  # 字段含义
        
        "成品出库申请明细英文名称": "成品出库申请明细英文名称",  # 字段含义
        
        "成品出库申请明细搜索码": "成品出库申请明细搜索码",  # 字段含义
        
        "成品出库申请明细计划需时": "成品出库申请明细计划需时(小时)",  # 字段含义
        
        "成品出库申请明细生产班次ID": "成品出库申请明细生产班次ID",  # 字段含义
        
        "成品出库申请明细任务数量": "成品出库申请明细任务数量",  # 字段含义
        
        "成品出库申请明细成品销货赠品完成数量": "成品出库申请明细成品销货赠品完成数量",  # 字段含义
        
        "成品出库申请明细成品销货赠品完成状态": "成品出库申请明细成品销货赠品完成状态",  # 字段含义
        
        "成品出库申请明细成品销货完成数量": "成品出库申请明细成品销货完成数量",  # 字段含义
        
        "成品出库申请明细成品销货备品完成数量": "成品出库申请明细成品销货备品完成数量",  # 字段含义
        
        "成品出库申请明细成品销货备品完成状态": "成品出库申请明细成品销货备品完成状态",  # 字段含义
        
        "成品出库申请明细成品销货完成状态": "成品出库申请明细成品销货完成状态",  # 字段含义
        
        "成品出库申请明细含税金额": "成品出库申请明细含税金额",  # 字段含义
        
        "成品出库申请明细不含税金额": "成品出库申请明细不含税金额",  # 字段含义
        
        "成品出库申请明细运输计划完成数量": "成品出库申请明细运输计划完成数量",  # 字段含义
        
        "成品出库申请明细运输计划完成状态": "成品出库申请明细运输计划完成状态"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("成品出库申请明细", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)


if __name__ == "__main__":
    access_token = auth_login()  # 获取访问令牌
    
    biz_order_detail_test(access_token)  # 调用测试函数
    
    prd_oapy_det_test(access_token)  # 调用测试函数
    