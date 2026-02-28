
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

def prd_sal_det_test(access_token: str):  # 定义测试函数
    """
    测试 /prd-sal-det/findList
    """
    # 构建请求URL
    url = "/prd-sal-det/findList"  # API地址
    prdSalDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    prdSalDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "prdSalDetPrdSalClazz": "PRD_SAL",  # 固定参数
        
        "prdSalDetClazz": "PRD_SAL_DET",  # 固定参数
        
        
        "prdSalDetFromCreateTime": prdSalDetFromCreateTime,  # 动态参数
        
        "prdSalDetToCreateTime": prdSalDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "prdSalDetActualTimeRequired": {"name": "成品销货明细表实际需时"},  # 字段映射
        
        "prdSalDetArea": {"name": "成品销货明细表面积"},  # 字段映射
        
        "prdSalDetAuditStatus": {"name": "成品销货明细表审核状态"},  # 字段映射
        
        "prdSalDetBeginTime": {"name": "成品销货明细表开始时间"},  # 字段映射
        
        "prdSalDetBriefName": {"name": "成品销货明细表简称"},  # 字段映射
        
        "prdSalDetClosedStatus": {"name": "成品销货明细表结案状态"},  # 字段映射
        
        "prdSalDetCompleteQuantity": {"name": "成品销货明细表完成数量"},  # 字段映射
        
        "prdSalDetCompleteStatus": {"name": "成品销货明细表完成状态"},  # 字段映射
        
        "prdSalDetCousigQuantity": {"name": "成品销货明细表回签数量"},  # 字段映射
        
        "prdSalDetCurrency": {"name": "成品销货明细表币种"},  # 字段映射
        
        "prdSalDetDeliverTotality": {"name": "成品销货明细表送货总数"},  # 字段映射
        
        "prdSalDetDeliveryDate": {"name": "成品销货明细表交货日期"},  # 字段映射
        
        "prdSalDetEngName": {"name": "成品销货明细表英文名称"},  # 字段映射
        
        "prdSalDetGrossWeightTotal": {"name": "成品销货明细表总毛重kg"},  # 字段映射
        
        "prdSalDetId": {"name": "成品销货明细表PK"},  # 字段映射
        
        "prdSalDetPlannedOutputQuantity": {"name": "成品销货明细表计划产出数量"},  # 字段映射
        
        "prdSalDetPlannedTimeRequired": {"name": "成品销货明细表计划需时"},  # 字段映射
        
        "prdSalDetPrdRetQuantity": {"name": "成品销货明细表成品退货数量"},  # 字段映射
        
        "prdSalDetPrdRetSpareQuantity": {"name": "成品销货明细表成品备品退货数量"},  # 字段映射
        
        "prdSalDetPrdRetSpareStatus": {"name": "成品销货明细表成品退货备品完成状态"},  # 字段映射
        
        "prdSalDetPrdRetStatus": {"name": "成品销货明细表成品退货完成状态"},  # 字段映射
        
        "prdSalDetPrdSalActualTimeRequired": {"name": "成品销货明细表实际需时"},  # 字段映射
        
        "prdSalDetPrdSalAdjustmentTimeRequired": {"name": "成品销货明细表调整需时"},  # 字段映射
        
        "prdSalDetPrdSalCompleteQuantity": {"name": "成品销货明细表完成数量"},  # 字段映射
        
        "prdSalDetPrdSalCompleteStatus": {"name": "成品销货明细表完成状态"},  # 字段映射
        
        "prdSalDetPrdSalConsigneeName": {"name": "成品销货明细表收货单位名称"},  # 字段映射
        
        "prdSalDetPrdSalCustContact": {"name": "成品销货明细表收货人"},  # 字段映射
        
        "prdSalDetPrdSalCustContactCellPhone": {"name": "成品销货明细表手机号"},  # 字段映射
        
        "prdSalDetPrdSalCustContactPhone": {"name": "成品销货明细表电话"},  # 字段映射
        
        "prdSalDetPrdSalCustDeclarationNumber": {"name": "成品销货明细表报关号"},  # 字段映射
        
        "prdSalDetPrdSalCustDeliverAddress": {"name": "成品销货明细表送货地址"},  # 字段映射
        
        "prdSalDetPrdSalDeliveryDate": {"name": "成品销货明细表交货日期"},  # 字段映射
        
        "prdSalDetPrdSalDriverName": {"name": "成品销货明细表司机"},  # 字段映射
        
        "prdSalDetPrdSalLicensePlate": {"name": "成品销货明细表车牌"},  # 字段映射
        
        "prdSalDetPrdSalLoadCompletionTime": {"name": "成品销货明细表装车完成时间"},  # 字段映射
        
        "prdSalDetPrdSalLoadStartTime": {"name": "成品销货明细表装车开始时间"},  # 字段映射
        
        "prdSalDetPrdSalLoadSupervisor": {"name": "成品销货明细表装车负责人_id"},  # 字段映射
        
        "prdSalDetPrdSalMainlandFinanceSignTime": {"name": "成品销货明细表大陆财务签收时间"},  # 字段映射
        
        "prdSalDetPrdSalPlannedOutputQuantity": {"name": "成品销货明细表计划产出数量"},  # 字段映射
        
        "prdSalDetPrdSalPlannedTimeRequired": {"name": "成品销货明细表计划需时"},  # 字段映射
        
        "prdSalDetPrdSalSettleAccountMode": {"name": "成品销货明细表结算方式"},  # 字段映射
        
        "prdSalDetPrdSalSettlementCustomerOrSupplierId": {"name": "成品销货明细表结算供应商/客户"},  # 字段映射
        
        "prdSalDetQuantity": {"name": "成品销货明细表任务数量"},  # 字段映射
        
        "prdSalDetQuotationUnitPriceIncludingTax": {"name": "成品销货明细表含税报价单价"},  # 字段映射
        
        "prdSalDetQuotationUnitPriceWithoutTax": {"name": "成品销货明细表不含税报价单价"},  # 字段映射
        
        "prdSalDetReceiptDate": {"name": "成品销货明细表单据日期"},  # 字段映射
        
        "prdSalDetReceiptType": {"name": "成品销货明细表单据类型"},  # 字段映射
        
        "prdSalDetSourceType": {"name": "成品销货明细表来源类型"},  # 字段映射
        
        "prdSalDetSpareQty": {"name": "成品销货明细表备品数量"},  # 字段映射
        
        "prdSalDetState": {"name": "成品销货明细表通用状态"},  # 字段映射
        
        "prdSalDetStatedQuantity": {"name": "成品销货明细表已对账数量"},  # 字段映射
        
        "prdSalDetStatedStatus": {"name": "成品销货明细表已对账状态"},  # 字段映射
        
        "prdSalDetSystemCode": {"name": "成品销货明细表系统编码"},  # 字段映射
        
        "prdSalDetTarget": {"name": "成品销货明细表目标"},  # 字段映射
        
        "prdSalDetTotalAmountIncludingTax": {"name": "成品销货明细表含税总金额"},  # 字段映射
        
        "prdSalDetTotalAmountWithoutTax": {"name": "成品销货明细表不含税总金额"},  # 字段映射
        
        "prdSalDetTransManageQuantity": {"name": "成品销货明细表运输管理完成数量"},  # 字段映射
        
        "prdSalDetTransManageStatus": {"name": "成品销货明细表运输管理完成状态"},  # 字段映射
        
        "prdSalDetUpdater": {"name": "成品销货明细表更新人"},  # 字段映射
        
        "prdSalDetVolumeTotal": {"name": "成品销货明细表总体积CMB"},  # 字段映射
        
        "prdSalDetWeightNetTotal": {"name": "成品销货明细表总净重kg"},  # 字段映射
        
        "prdSalDetWeightTotal": {"name": "成品销货明细表合计重量"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "成品销货明细表实际需时": "成品销货明细表实际需时(小时)",  # 字段含义
        
        "成品销货明细表面积": "成品销货明细表面积",  # 字段含义
        
        "成品销货明细表审核状态": "成品销货明细表审核状态",  # 字段含义
        
        "成品销货明细表开始时间": "成品销货明细表开始时间",  # 字段含义
        
        "成品销货明细表简称": "成品销货明细表简称",  # 字段含义
        
        "成品销货明细表结案状态": "成品销货明细表结案状态",  # 字段含义
        
        "成品销货明细表完成数量": "成品销货明细表完成数量",  # 字段含义
        
        "成品销货明细表完成状态": "成品销货明细表完成状态",  # 字段含义
        
        "成品销货明细表回签数量": "成品销货明细表回签数量",  # 字段含义
        
        "成品销货明细表币种": "成品销货明细表币种",  # 字段含义
        
        "成品销货明细表送货总数": "成品销货明细表送货总数",  # 字段含义
        
        "成品销货明细表交货日期": "成品销货明细表交货日期",  # 字段含义
        
        "成品销货明细表英文名称": "成品销货明细表英文名称",  # 字段含义
        
        "成品销货明细表总毛重kg": "成品销货明细表总毛重kg",  # 字段含义
        
        "成品销货明细表PK": "成品销货明细表PK",  # 字段含义
        
        "成品销货明细表计划产出数量": "成品销货明细表计划产出数量",  # 字段含义
        
        "成品销货明细表计划需时": "成品销货明细表计划需时(小时)",  # 字段含义
        
        "成品销货明细表成品退货数量": "成品销货明细表成品退货数量",  # 字段含义
        
        "成品销货明细表成品备品退货数量": "成品销货明细表成品备品退货数量",  # 字段含义
        
        "成品销货明细表成品退货备品完成状态": "成品销货明细表成品退货备品完成状态",  # 字段含义
        
        "成品销货明细表成品退货完成状态": "成品销货明细表成品退货完成状态",  # 字段含义
        
        "成品销货明细表实际需时": "成品销货明细表实际需时(小时)",  # 字段含义
        
        "成品销货明细表调整需时": "成品销货明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "成品销货明细表完成数量": "成品销货明细表完成数量",  # 字段含义
        
        "成品销货明细表完成状态": "成品销货明细表完成状态",  # 字段含义
        
        "成品销货明细表收货单位名称": "成品销货明细表收货单位名称",  # 字段含义
        
        "成品销货明细表收货人": "成品销货明细表收货人(客户联系人)",  # 字段含义
        
        "成品销货明细表手机号": "成品销货明细表手机号(客户联系人手机号)",  # 字段含义
        
        "成品销货明细表电话": "成品销货明细表电话(客户联系人电话)",  # 字段含义
        
        "成品销货明细表报关号": "成品销货明细表报关号",  # 字段含义
        
        "成品销货明细表送货地址": "成品销货明细表送货地址(客户送货地址)",  # 字段含义
        
        "成品销货明细表交货日期": "成品销货明细表交货日期",  # 字段含义
        
        "成品销货明细表司机": "成品销货明细表司机",  # 字段含义
        
        "成品销货明细表车牌": "成品销货明细表车牌",  # 字段含义
        
        "成品销货明细表装车完成时间": "成品销货明细表装车完成时间",  # 字段含义
        
        "成品销货明细表装车开始时间": "成品销货明细表装车开始时间",  # 字段含义
        
        "成品销货明细表装车负责人_id": "成品销货明细表装车负责人_id",  # 字段含义
        
        "成品销货明细表大陆财务签收时间": "成品销货明细表大陆财务签收时间",  # 字段含义
        
        "成品销货明细表计划产出数量": "成品销货明细表计划产出数量",  # 字段含义
        
        "成品销货明细表计划需时": "成品销货明细表计划需时(小时)",  # 字段含义
        
        "成品销货明细表结算方式": "成品销货明细表结算方式",  # 字段含义
        
        "成品销货明细表结算供应商/客户": "成品销货明细表结算供应商/客户",  # 字段含义
        
        "成品销货明细表任务数量": "成品销货明细表任务数量",  # 字段含义
        
        "成品销货明细表含税报价单价": "成品销货明细表含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "成品销货明细表不含税报价单价": "成品销货明细表不含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "成品销货明细表单据日期": "成品销货明细表单据日期",  # 字段含义
        
        "成品销货明细表单据类型": "成品销货明细表单据类型（一个常量值，与node里的defaultTypeId不一样，推荐使用字典）",  # 字段含义
        
        "成品销货明细表来源类型": "成品销货明细表来源类型",  # 字段含义
        
        "成品销货明细表备品数量": "成品销货明细表备品数量",  # 字段含义
        
        "成品销货明细表通用状态": "成品销货明细表通用状态",  # 字段含义
        
        "成品销货明细表已对账数量": "成品销货明细表已对账数量",  # 字段含义
        
        "成品销货明细表已对账状态": "成品销货明细表已对账状态",  # 字段含义
        
        "成品销货明细表系统编码": "成品销货明细表系统编码",  # 字段含义
        
        "成品销货明细表目标": "成品销货明细表目标",  # 字段含义
        
        "成品销货明细表含税总金额": "成品销货明细表含税总金额",  # 字段含义
        
        "成品销货明细表不含税总金额": "成品销货明细表不含税总金额",  # 字段含义
        
        "成品销货明细表运输管理完成数量": "成品销货明细表运输管理完成数量",  # 字段含义
        
        "成品销货明细表运输管理完成状态": "成品销货明细表运输管理完成状态",  # 字段含义
        
        "成品销货明细表更新人": "成品销货明细表更新人",  # 字段含义
        
        "成品销货明细表总体积CMB": "成品销货明细表总体积CMB",  # 字段含义
        
        "成品销货明细表总净重kg": "成品销货明细表总净重kg(送货数量+备品)*单重",  # 字段含义
        
        "成品销货明细表合计重量": "成品销货明细表合计重量(总毛重+托盘总重量)"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("成品销货明细表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def PRD_RET_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /prd-ret-det/findList
    """
    # 构建请求URL
    url = "/prd-ret-det/findList"  # API地址
    prdRetDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    prdRetDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "prdRetDetPrdRetClazz": "PRD_RET",  # 固定参数
        
        "prdRetDetClazz": "PRD_RET_DET",  # 固定参数
        
        
        "prdRetDetFromCreateTime": prdRetDetFromCreateTime,  # 动态参数
        
        "prdRetDetToCreateTime": prdRetDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "prdRetDetArea": {"name": "成品退货明细表面积"},  # 字段映射
        
        "prdRetDetBeginTime": {"name": "成品退货明细表开始时间"},  # 字段映射
        
        "prdRetDetClosedStatus": {"name": "成品退货明细表结案状态"},  # 字段映射
        
        "prdRetDetCompleteQuantity": {"name": "成品退货明细表完成数量"},  # 字段映射
        
        "prdRetDetCompleteStatus": {"name": "成品退货明细表完成状态"},  # 字段映射
        
        "prdRetDetCurrencyExchangeRate": {"name": "成品退货明细表汇率"},  # 字段映射
        
        "prdRetDetDeliveryDate": {"name": "成品退货明细表交货日期"},  # 字段映射
        
        "prdRetDetEndTime": {"name": "成品退货明细表结束时间"},  # 字段映射
        
        "prdRetDetEquipmentId": {"name": "成品退货明细表设备id"},  # 字段映射
        
        "prdRetDetId": {"name": "成品退货明细表PK"},  # 字段映射
        
        "prdRetDetLocalCurrencyTotalAmount": {"name": "成品退货明细表本币金额"},  # 字段映射
        
        "prdRetDetLocalCurrencyUnitPrice": {"name": "成品退货明细表本币单价"},  # 字段映射
        
        "prdRetDetPlannedOutputQuantity": {"name": "成品退货明细表计划产出数量"},  # 字段映射
        
        "prdRetDetPlannedTimeRequired": {"name": "成品退货明细表计划需时"},  # 字段映射
        
        "prdRetDetPrdRetActualTimeRequired": {"name": "成品退货明细表实际需时"},  # 字段映射
        
        "prdRetDetPrdRetCompleteQuantity": {"name": "成品退货明细表完成数量"},  # 字段映射
        
        "prdRetDetPrdRetCompleteStatus": {"name": "成品退货明细表完成状态"},  # 字段映射
        
        "prdRetDetPrdRetConsignee": {"name": "成品退货明细表收货人"},  # 字段映射
        
        "prdRetDetPrdRetConsigneeCellPhone": {"name": "成品退货明细表收货人手机"},  # 字段映射
        
        "prdRetDetPrdRetConsigneePhone": {"name": "成品退货明细表收货人电话"},  # 字段映射
        
        "prdRetDetPrdRetDecimalMethod": {"name": "成品退货明细表保留小数位方法"},  # 字段映射
        
        "prdRetDetPrdRetDeliveryAddress": {"name": "成品退货明细表送货地址"},  # 字段映射
        
        "prdRetDetPrdRetDeliveryDate": {"name": "成品退货明细表交货日期"},  # 字段映射
        
        "prdRetDetPrdRetEndTime": {"name": "成品退货明细表结束时间"},  # 字段映射
        
        "prdRetDetPrdRetEndTimeRequired": {"name": "成品退货明细表最后需时"},  # 字段映射
        
        "prdRetDetPrdRetPlannedOutputQuantity": {"name": "成品退货明细表计划产出数量"},  # 字段映射
        
        "prdRetDetPrdRetPlannedTimeRequired": {"name": "成品退货明细表计划需时"},  # 字段映射
        
        "prdRetDetPrdRetQuantity": {"name": "成品退货明细表任务数量"},  # 字段映射
        
        "prdRetDetPrdRetReason": {"name": "成品退货明细表原因"},  # 字段映射
        
        "prdRetDetPrdRetReceiptDate": {"name": "成品退货明细表单据日期"},  # 字段映射
        
        "prdRetDetPrdRetTransCompany": {"name": "成品退货明细表运输公司"},  # 字段映射
        
        "prdRetDetQuantity": {"name": "成品退货明细表任务数量"},  # 字段映射
        
        "prdRetDetQuotationUnitPriceIncludingTax": {"name": "成品退货明细表含税报价单价"},  # 字段映射
        
        "prdRetDetQuotationUnitPriceWithoutTax": {"name": "成品退货明细表不含税报价单价"},  # 字段映射
        
        "prdRetDetSettlementTotalAmount": {"name": "成品退货明细表结算金额"},  # 字段映射
        
        "prdRetDetSettlementUnitPrice": {"name": "成品退货明细表结算单价"},  # 字段映射
        
        "prdRetDetStatedQuantity": {"name": "成品退货明细表已对账数量"},  # 字段映射
        
        "prdRetDetStatedStatus": {"name": "成品退货明细表已对账状态"},  # 字段映射
        
        "prdRetDetTotalAmountIncludingTax": {"name": "成品退货明细表含税总金额"},  # 字段映射
        
        "prdRetDetTotalAmountWithoutTax": {"name": "成品退货明细表不含税总金额"},  # 字段映射
        
        "prdRetDetTotalQuantity": {"name": "成品退货明细表退货总数"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "成品退货明细表面积": "成品退货明细表面积",  # 字段含义
        
        "成品退货明细表开始时间": "成品退货明细表开始时间",  # 字段含义
        
        "成品退货明细表结案状态": "成品退货明细表结案状态",  # 字段含义
        
        "成品退货明细表完成数量": "成品退货明细表完成数量",  # 字段含义
        
        "成品退货明细表完成状态": "成品退货明细表完成状态",  # 字段含义
        
        "成品退货明细表汇率": "成品退货明细表汇率",  # 字段含义
        
        "成品退货明细表交货日期": "成品退货明细表交货日期",  # 字段含义
        
        "成品退货明细表结束时间": "成品退货明细表结束时间",  # 字段含义
        
        "成品退货明细表设备id": "成品退货明细表设备id",  # 字段含义
        
        "成品退货明细表PK": "成品退货明细表PK",  # 字段含义
        
        "成品退货明细表本币金额": "成品退货明细表本币金额",  # 字段含义
        
        "成品退货明细表本币单价": "成品退货明细表本币单价(根据币种，外币才显示)，外币不含税",  # 字段含义
        
        "成品退货明细表计划产出数量": "成品退货明细表计划产出数量",  # 字段含义
        
        "成品退货明细表计划需时": "成品退货明细表计划需时(小时)",  # 字段含义
        
        "成品退货明细表实际需时": "成品退货明细表实际需时(小时)",  # 字段含义
        
        "成品退货明细表完成数量": "成品退货明细表完成数量",  # 字段含义
        
        "成品退货明细表完成状态": "成品退货明细表完成状态",  # 字段含义
        
        "成品退货明细表收货人": "成品退货明细表收货人",  # 字段含义
        
        "成品退货明细表收货人手机": "成品退货明细表收货人手机",  # 字段含义
        
        "成品退货明细表收货人电话": "成品退货明细表收货人电话",  # 字段含义
        
        "成品退货明细表保留小数位方法": "成品退货明细表保留小数位方法(1四舍五入，2有小数进位，默认四舍五入)",  # 字段含义
        
        "成品退货明细表送货地址": "成品退货明细表送货地址",  # 字段含义
        
        "成品退货明细表交货日期": "成品退货明细表交货日期",  # 字段含义
        
        "成品退货明细表结束时间": "成品退货明细表结束时间",  # 字段含义
        
        "成品退货明细表最后需时": "成品退货明细表最后需时(小时)",  # 字段含义
        
        "成品退货明细表计划产出数量": "成品退货明细表计划产出数量",  # 字段含义
        
        "成品退货明细表计划需时": "成品退货明细表计划需时(小时)",  # 字段含义
        
        "成品退货明细表任务数量": "成品退货明细表任务数量",  # 字段含义
        
        "成品退货明细表原因": "成品退货明细表原因",  # 字段含义
        
        "成品退货明细表单据日期": "成品退货明细表单据日期",  # 字段含义
        
        "成品退货明细表运输公司": "成品退货明细表运输公司",  # 字段含义
        
        "成品退货明细表任务数量": "成品退货明细表任务数量",  # 字段含义
        
        "成品退货明细表含税报价单价": "成品退货明细表含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "成品退货明细表不含税报价单价": "成品退货明细表不含税报价单价(吨价，平方价，千平方英寸)",  # 字段含义
        
        "成品退货明细表结算金额": "成品退货明细表结算金额（默认与含税总金额相等），写入库存价格字段",  # 字段含义
        
        "成品退货明细表结算单价": "成品退货明细表结算单价（默认与含税单价相等），写入库存价格字段",  # 字段含义
        
        "成品退货明细表已对账数量": "成品退货明细表已对账数量",  # 字段含义
        
        "成品退货明细表已对账状态": "成品退货明细表已对账状态",  # 字段含义
        
        "成品退货明细表含税总金额": "成品退货明细表含税总金额",  # 字段含义
        
        "成品退货明细表不含税总金额": "成品退货明细表不含税总金额",  # 字段含义
        
        "成品退货明细表退货总数": "成品退货明细表退货总数"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("成品退货明细表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def CUST_STATEMENT_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /cust-statement-det/findList
    """
    # 构建请求URL
    url = "/cust-statement-det/findList"  # API地址
    custStatementDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    custStatementDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "custStatementDetCustStatementClazz": "CUST_STATEMENT",  # 固定参数
        
        "custStatementDetClazz": "CUST_STATEMENT_DET",  # 固定参数
        
        
        "custStatementDetFromCreateTime": custStatementDetFromCreateTime,  # 动态参数
        
        "custStatementDetToCreateTime": custStatementDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "custStatementDetActualTimeRequired": {"name": "客户对账单明细实际需时"},  # 字段映射
        
        "custStatementDetAdjustmentTimeRequired": {"name": "客户对账单明细调整需时"},  # 字段映射
        
        "custStatementDetAmount": {"name": "客户对账单明细金额"},  # 字段映射
        
        "custStatementDetAuditDate": {"name": "客户对账单明细审核时间"},  # 字段映射
        
        "custStatementDetAuditStatus": {"name": "客户对账单明细审核状态"},  # 字段映射
        
        "custStatementDetBriefName": {"name": "客户对账单明细简称"},  # 字段映射
        
        "custStatementDetCompleteQuantity": {"name": "客户对账单明细完成数量"},  # 字段映射
        
        "custStatementDetCustStatementActualTimeRequired": {"name": "客户对账单明细实际需时"},  # 字段映射
        
        "custStatementDetCustStatementAdjustmentTimeRequired": {"name": "客户对账单明细调整需时"},  # 字段映射
        
        "custStatementDetCustStatementBriefName": {"name": "客户对账单明细简称"},  # 字段映射
        
        "custStatementDetCustStatementCompleteQuantity": {"name": "客户对账单明细完成数量"},  # 字段映射
        
        "custStatementDetCustStatementCompleteStatus": {"name": "客户对账单明细完成状态"},  # 字段映射
        
        "custStatementDetCustStatementDeliveryDate": {"name": "客户对账单明细交货日期"},  # 字段映射
        
        "custStatementDetCustStatementEndTime": {"name": "客户对账单明细结束时间"},  # 字段映射
        
        "custStatementDetCustStatementEndTimeRequired": {"name": "客户对账单明细最后需时"},  # 字段映射
        
        "custStatementDetCustStatementEquipmentId": {"name": "客户对账单明细设备id"},  # 字段映射
        
        "custStatementDetCustStatementLocCompleteQuantity": {"name": "客户对账单明细本币完成数量"},  # 字段映射
        
        "custStatementDetCustStatementLocTotalAmount": {"name": "客户对账单明细本币总金额"},  # 字段映射
        
        "custStatementDetCustStatementLocTotalInvoicedAmount": {"name": "客户对账单明细本币总已开票金额"},  # 字段映射
        
        "custStatementDetCustStatementLocTotalOtherExpense": {"name": "客户对账单明细本币总其他费用"},  # 字段映射
        
        "custStatementDetCustStatementLocTotalSettleAmount": {"name": "客户对账单明细本币总结算金额"},  # 字段映射
        
        "custStatementDetCustStatementLocTotalSettledAmount": {"name": "客户对账单明细本币总已结算金额"},  # 字段映射
        
        "custStatementDetCustStatementTotalAmount": {"name": "客户对账单明细总金额"},  # 字段映射
        
        "custStatementDetCustStatementTotalInvoicedAmount": {"name": "客户对账单明细总已开票金额"},  # 字段映射
        
        "custStatementDetCustStatementTotalOtherExpense": {"name": "客户对账单明细总其他费用"},  # 字段映射
        
        "custStatementDetCustStatementTotalSettleAmount": {"name": "客户对账单明细总结算金额"},  # 字段映射
        
        "custStatementDetCustStatementTotalSettledAmount": {"name": "客户对账单明细总已结算金额"},  # 字段映射
        
        "custStatementDetDeliveryDate": {"name": "客户对账单明细交货日期"},  # 字段映射
        
        "custStatementDetEndTime": {"name": "客户对账单明细结束时间"},  # 字段映射
        
        "custStatementDetEndTimeRequired": {"name": "客户对账单明细最后需时"},  # 字段映射
        
        "custStatementDetId": {"name": "客户对账单明细PK"},  # 字段映射
        
        "custStatementDetUnitCode": {"name": "客户对账单明细单位id"},  # 字段映射
        
        "custStatementDetUnitPrice": {"name": "客户对账单明细单价"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "客户对账单明细实际需时": "客户对账单明细实际需时(小时)",  # 字段含义
        
        "客户对账单明细调整需时": "客户对账单明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "客户对账单明细金额": "客户对账单明细金额",  # 字段含义
        
        "客户对账单明细审核时间": "客户对账单明细审核时间",  # 字段含义
        
        "客户对账单明细审核状态": "客户对账单明细审核状态",  # 字段含义
        
        "客户对账单明细简称": "客户对账单明细简称",  # 字段含义
        
        "客户对账单明细完成数量": "客户对账单明细完成数量",  # 字段含义
        
        "客户对账单明细实际需时": "客户对账单明细实际需时(小时)",  # 字段含义
        
        "客户对账单明细调整需时": "客户对账单明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "客户对账单明细简称": "客户对账单明细简称",  # 字段含义
        
        "客户对账单明细完成数量": "客户对账单明细完成数量",  # 字段含义
        
        "客户对账单明细完成状态": "客户对账单明细完成状态",  # 字段含义
        
        "客户对账单明细交货日期": "客户对账单明细交货日期",  # 字段含义
        
        "客户对账单明细结束时间": "客户对账单明细结束时间",  # 字段含义
        
        "客户对账单明细最后需时": "客户对账单明细最后需时(小时)",  # 字段含义
        
        "客户对账单明细设备id": "客户对账单明细设备id",  # 字段含义
        
        "客户对账单明细本币完成数量": "客户对账单明细本币完成数量",  # 字段含义
        
        "客户对账单明细本币总金额": "客户对账单明细本币总金额",  # 字段含义
        
        "客户对账单明细本币总已开票金额": "客户对账单明细本币总已开票金额",  # 字段含义
        
        "客户对账单明细本币总其他费用": "客户对账单明细本币总其他费用",  # 字段含义
        
        "客户对账单明细本币总结算金额": "客户对账单明细本币总结算金额（本币总金额+本币总其他费用）",  # 字段含义
        
        "客户对账单明细本币总已结算金额": "客户对账单明细本币总已结算金额",  # 字段含义
        
        "客户对账单明细总金额": "客户对账单明细总金额",  # 字段含义
        
        "客户对账单明细总已开票金额": "客户对账单明细总已开票金额",  # 字段含义
        
        "客户对账单明细总其他费用": "客户对账单明细总其他费用",  # 字段含义
        
        "客户对账单明细总结算金额": "客户对账单明细总结算金额（总金额+总其他费用）",  # 字段含义
        
        "客户对账单明细总已结算金额": "客户对账单明细总已结算金额",  # 字段含义
        
        "客户对账单明细交货日期": "客户对账单明细交货日期",  # 字段含义
        
        "客户对账单明细结束时间": "客户对账单明细结束时间",  # 字段含义
        
        "客户对账单明细最后需时": "客户对账单明细最后需时(小时)",  # 字段含义
        
        "客户对账单明细PK": "客户对账单明细PK",  # 字段含义
        
        "客户对账单明细单位id": "客户对账单明细单位id",  # 字段含义
        
        "客户对账单明细单价": "客户对账单明细单价"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("客户对账单明细", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def INVO_ISS_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /invo-iss-det/findList
    """
    # 构建请求URL
    url = "/invo-iss-det/findList"  # API地址
    invoIssDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    invoIssDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "invoIssDetInvoIssClazz": "INVO_ISS",  # 固定参数
        
        "invoIssDetClazz": "INVO_ISS_DET",  # 固定参数
        
        
        "invoIssDetFromCreateTime": invoIssDetFromCreateTime,  # 动态参数
        
        "invoIssDetToCreateTime": invoIssDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "invoIssDetActualTimeRequired": {"name": "开票登记明细表实际需时"},  # 字段映射
        
        "invoIssDetAdjustmentTimeRequired": {"name": "开票登记明细表调整需时"},  # 字段映射
        
        "invoIssDetAmount": {"name": "开票登记明细表自动调整金额"},  # 字段映射
        
        "invoIssDetAuditDate": {"name": "开票登记明细表审核时间"},  # 字段映射
        
        "invoIssDetAuditStatus": {"name": "开票登记明细表审核状态"},  # 字段映射
        
        "invoIssDetBeginTime": {"name": "开票登记明细表开始时间"},  # 字段映射
        
        "invoIssDetBriefName": {"name": "开票登记明细表简称"},  # 字段映射
        
        "invoIssDetCompleteQuantity": {"name": "开票登记明细表完成数量"},  # 字段映射
        
        "invoIssDetCompleteStatus": {"name": "开票登记明细表完成状态"},  # 字段映射
        
        "invoIssDetDeliveryDate": {"name": "开票登记明细表交货日期"},  # 字段映射
        
        "invoIssDetEndTime": {"name": "开票登记明细表结束时间"},  # 字段映射
        
        "invoIssDetEndTimeRequired": {"name": "开票登记明细表最后需时"},  # 字段映射
        
        "invoIssDetId": {"name": "开票登记明细表PK"},  # 字段映射
        
        "invoIssDetInvoIssActualTimeRequired": {"name": "开票登记明细表实际需时"},  # 字段映射
        
        "invoIssDetInvoIssAmountIncludingTax": {"name": "开票登记明细表收款/付款金额"},  # 字段映射
        
        "invoIssDetInvoIssBriefName": {"name": "开票登记明细表简称"},  # 字段映射
        
        "invoIssDetInvoIssCompleteQuantity": {"name": "开票登记明细表完成数量"},  # 字段映射
        
        "invoIssDetInvoIssCompleteStatus": {"name": "开票登记明细表完成状态"},  # 字段映射
        
        "invoIssDetInvoIssDeliveryDate": {"name": "开票登记明细表交货日期"},  # 字段映射
        
        "invoIssDetInvoIssEndTime": {"name": "开票登记明细表结束时间"},  # 字段映射
        
        "invoIssDetInvoIssEndTimeRequired": {"name": "开票登记明细表最后需时"},  # 字段映射
        
        "invoIssDetInvoIssPlannedOutputQuantity": {"name": "开票登记明细表计划产出数量"},  # 字段映射
        
        "invoIssDetInvoIssQuantity": {"name": "开票登记明细表任务数量"},  # 字段映射
        
        "invoIssDetLocalAmount": {"name": "开票登记明细表本币金额"},  # 字段映射
        
        "invoIssDetPlannedOutputQuantity": {"name": "开票登记明细表计划产出数量"},  # 字段映射
        
        "invoIssDetPlannedTimeRequired": {"name": "开票登记明细表计划需时"},  # 字段映射
        
        "invoIssDetQuantity": {"name": "开票登记明细表任务数量"},  # 字段映射
        
        "invoIssDetReceiptDate": {"name": "开票登记明细表单据日期"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "开票登记明细表实际需时": "开票登记明细表实际需时(小时)",  # 字段含义
        
        "开票登记明细表调整需时": "开票登记明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "开票登记明细表自动调整金额": "开票登记明细表自动调整金额",  # 字段含义
        
        "开票登记明细表审核时间": "开票登记明细表审核时间",  # 字段含义
        
        "开票登记明细表审核状态": "开票登记明细表审核状态",  # 字段含义
        
        "开票登记明细表开始时间": "开票登记明细表开始时间",  # 字段含义
        
        "开票登记明细表简称": "开票登记明细表简称",  # 字段含义
        
        "开票登记明细表完成数量": "开票登记明细表完成数量",  # 字段含义
        
        "开票登记明细表完成状态": "开票登记明细表完成状态",  # 字段含义
        
        "开票登记明细表交货日期": "开票登记明细表交货日期",  # 字段含义
        
        "开票登记明细表结束时间": "开票登记明细表结束时间",  # 字段含义
        
        "开票登记明细表最后需时": "开票登记明细表最后需时(小时)",  # 字段含义
        
        "开票登记明细表PK": "开票登记明细表PK",  # 字段含义
        
        "开票登记明细表实际需时": "开票登记明细表实际需时(小时)",  # 字段含义
        
        "开票登记明细表收款/付款金额": "开票登记明细表收款/付款金额(含税)",  # 字段含义
        
        "开票登记明细表简称": "开票登记明细表简称",  # 字段含义
        
        "开票登记明细表完成数量": "开票登记明细表完成数量",  # 字段含义
        
        "开票登记明细表完成状态": "开票登记明细表完成状态",  # 字段含义
        
        "开票登记明细表交货日期": "开票登记明细表交货日期",  # 字段含义
        
        "开票登记明细表结束时间": "开票登记明细表结束时间",  # 字段含义
        
        "开票登记明细表最后需时": "开票登记明细表最后需时(小时)",  # 字段含义
        
        "开票登记明细表计划产出数量": "开票登记明细表计划产出数量",  # 字段含义
        
        "开票登记明细表任务数量": "开票登记明细表任务数量",  # 字段含义
        
        "开票登记明细表本币金额": "开票登记明细表本币金额",  # 字段含义
        
        "开票登记明细表计划产出数量": "开票登记明细表计划产出数量",  # 字段含义
        
        "开票登记明细表计划需时": "开票登记明细表计划需时(小时)",  # 字段含义
        
        "开票登记明细表任务数量": "开票登记明细表任务数量",  # 字段含义
        
        "开票登记明细表单据日期": "开票登记明细表单据日期"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("开票登记明细表", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)


if __name__ == "__main__":
    access_token = auth_login()  # 获取访问令牌
    
    #biz_order_detail_test(access_token)  # 调用测试函数
    
    prd_oapy_det_test(access_token)  # 调用测试函数
    
    #prd_sal_det_test(access_token)  # 调用测试函数
    
    #PRD_RET_DET_test(access_token)  # 调用测试函数
    
    #CUST_STATEMENT_DET_test(access_token)  # 调用测试函数
    
    #INVO_ISS_DET_test(access_token)  # 调用测试函数
    