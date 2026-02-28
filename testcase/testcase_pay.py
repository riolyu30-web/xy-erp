
import sys # 导入sys模块
import os # 导入os模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将上上级目录添加到系统路径
from datetime import datetime, timedelta # 导入日期时间模块
from services.auth_service import auth_login # 导入登录认证模块
from services.tool import fetch_data  # 导入工具函数
import json # 导入json模块


def REC_SETTLE_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /rec-settle-det/findList
    """
    # 构建请求URL
    url = "/rec-settle-det/findList"  # API地址
    recSettleDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    recSettleDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S ")

    # 构建请求体数据
    data = {
        
        "recSettleDetRecSettleClazz": "REC_SETTLE",  # 固定参数
        
        "recSettleDetClazz": "REC_SETTLE_DET",  # 固定参数
        
        
        "recSettleDetFromCreateTime": recSettleDetFromCreateTime,  # 动态参数
        
        "recSettleDetToCreateTime": recSettleDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "recSettleDetActAmount": {"name": "应收结算明细实际结算金额"},  # 字段映射
        
        "recSettleDetActDiffAmount": {"name": "应收结算明细实际结算差额"},  # 字段映射
        
        "recSettleDetActualTimeRequired": {"name": "应收结算明细实际需时"},  # 字段映射
        
        "recSettleDetAdjustmentTimeRequired": {"name": "应收结算明细调整需时"},  # 字段映射
        
        "recSettleDetAmount": {"name": "应收结算明细结算金额"},  # 字段映射
        
        "recSettleDetAuditStatus": {"name": "应收结算明细审核状态"},  # 字段映射
        
        "recSettleDetBeginTime": {"name": "应收结算明细开始时间"},  # 字段映射
        
        "recSettleDetBriefName": {"name": "应收结算明细简称"},  # 字段映射
        
        "recSettleDetClosedReason": {"name": "应收结算明细结案原因"},  # 字段映射
        
        "recSettleDetClosedStatus": {"name": "应收结算明细结案状态"},  # 字段映射
        
        "recSettleDetCompleteQuantity": {"name": "应收结算明细完成数量"},  # 字段映射
        
        "recSettleDetDeliveryDate": {"name": "应收结算明细交货日期"},  # 字段映射
        
        "recSettleDetEndTime": {"name": "应收结算明细结束时间"},  # 字段映射
        
        "recSettleDetId": {"name": "应收结算明细PK"},  # 字段映射
        
        "recSettleDetLocActAmount": {"name": "应收结算明细本币实际结算金额"},  # 字段映射
        
        "recSettleDetLocActDiffAmount": {"name": "应收结算明细本币实际结算"},  # 字段映射
        
        "recSettleDetLocAmount": {"name": "应收结算明细本币结算金额"},  # 字段映射
        
        "recSettleDetLocOtherExpense": {"name": "应收结算明细本币其他费用"},  # 字段映射
        
        "recSettleDetLocTotalInvoicedAmount": {"name": "应收结算明细本币总开票金额"},  # 字段映射
        
        "recSettleDetPlannedOutputQuantity": {"name": "应收结算明细计划产出数量"},  # 字段映射
        
        "recSettleDetRecSettleAcctHolderName": {"name": "应收结算明细账号持有人"},  # 字段映射
        
        "recSettleDetRecSettleActualTimeRequired": {"name": "应收结算明细实际需时"},  # 字段映射
        
        "recSettleDetRecSettleBankName": {"name": "应收结算明细银行名称"},  # 字段映射
        
        "recSettleDetRecSettleBriefName": {"name": "应收结算明细简称"},  # 字段映射
        
        "recSettleDetRecSettleCompleteQuantity": {"name": "应收结算明细完成数量"},  # 字段映射
        
        "recSettleDetRecSettleCompleteStatus": {"name": "应收结算明细完成状态"},  # 字段映射
        
        "recSettleDetRecSettleDeliveryDate": {"name": "应收结算明细交货日期"},  # 字段映射
        
        "recSettleDetRecSettleLocTotalActAmount": {"name": "应收结算明细本币总实际结算金额"},  # 字段映射
        
        "recSettleDetRecSettleLocTotalActDiffAmount": {"name": "应收结算明细本币总实际结算差额"},  # 字段映射
        
        "recSettleDetRecSettleLocTotalAmount": {"name": "应收结算明细本币总结算金额"},  # 字段映射
        
        "recSettleDetRecSettleLocTotalInvoicedAmount": {"name": "应收结算明细本币总开票金额"},  # 字段映射
        
        "recSettleDetRecSettleLocTotalOtherExpense": {"name": "应收结算明细本币总其他费用"},  # 字段映射
        
        "recSettleDetRecSettlePlannedOutputQuantity": {"name": "应收结算明细计划产出数量"},  # 字段映射
        
        "recSettleDetRecSettlePlannedTimeRequired": {"name": "应收结算明细计划需时"},  # 字段映射
        
        "recSettleDetRecSettleQuantity": {"name": "应收结算明细任务数量"},  # 字段映射
        
        "recSettleDetRecSettleReceiptDate": {"name": "应收结算明细单据日期"},  # 字段映射
        
        "recSettleDetRecSettleSettleAmount": {"name": "应收结算明细结算金额"},  # 字段映射
        
        "recSettleDetRecSettleTotalActAmount": {"name": "应收结算明细实际结算金额"},  # 字段映射
        
        "recSettleDetRecSettleTotalActDiffAmount": {"name": "应收结算明细总实际结算差额"},  # 字段映射
        
        "recSettleDetRecSettleTotalAmount": {"name": "应收结算明细总结算金额"},  # 字段映射
        
        "recSettleDetRecSettleTotalInvoicedAmount": {"name": "应收结算明细总开票金额"},  # 字段映射
        
        "recSettleDetTotalInvoicedAmount": {"name": "应收结算明细总开票金额"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "应收结算明细实际结算金额": "应收结算明细实际结算金额",  # 字段含义
        
        "应收结算明细实际结算差额": "应收结算明细实际结算差额",  # 字段含义
        
        "应收结算明细实际需时": "应收结算明细实际需时(小时)",  # 字段含义
        
        "应收结算明细调整需时": "应收结算明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "应收结算明细结算金额": "应收结算明细结算金额",  # 字段含义
        
        "应收结算明细审核状态": "应收结算明细审核状态",  # 字段含义
        
        "应收结算明细开始时间": "应收结算明细开始时间",  # 字段含义
        
        "应收结算明细简称": "应收结算明细简称",  # 字段含义
        
        "应收结算明细结案原因": "应收结算明细结案原因",  # 字段含义
        
        "应收结算明细结案状态": "应收结算明细结案状态",  # 字段含义
        
        "应收结算明细完成数量": "应收结算明细完成数量",  # 字段含义
        
        "应收结算明细交货日期": "应收结算明细交货日期",  # 字段含义
        
        "应收结算明细结束时间": "应收结算明细结束时间",  # 字段含义
        
        "应收结算明细PK": "应收结算明细PK",  # 字段含义
        
        "应收结算明细本币实际结算金额": "应收结算明细本币实际结算金额",  # 字段含义
        
        "应收结算明细本币实际结算": "应收结算明细本币实际结算",  # 字段含义
        
        "应收结算明细本币结算金额": "应收结算明细本币结算金额",  # 字段含义
        
        "应收结算明细本币其他费用": "应收结算明细本币其他费用",  # 字段含义
        
        "应收结算明细本币总开票金额": "应收结算明细本币总开票金额",  # 字段含义
        
        "应收结算明细计划产出数量": "应收结算明细计划产出数量",  # 字段含义
        
        "应收结算明细账号持有人": "应收结算明细账号持有人",  # 字段含义
        
        "应收结算明细实际需时": "应收结算明细实际需时(小时)",  # 字段含义
        
        "应收结算明细银行名称": "应收结算明细银行名称",  # 字段含义
        
        "应收结算明细简称": "应收结算明细简称",  # 字段含义
        
        "应收结算明细完成数量": "应收结算明细完成数量",  # 字段含义
        
        "应收结算明细完成状态": "应收结算明细完成状态",  # 字段含义
        
        "应收结算明细交货日期": "应收结算明细交货日期",  # 字段含义
        
        "应收结算明细本币总实际结算金额": "应收结算明细本币总实际结算金额",  # 字段含义
        
        "应收结算明细本币总实际结算差额": "应收结算明细本币总实际结算差额",  # 字段含义
        
        "应收结算明细本币总结算金额": "应收结算明细本币总结算金额",  # 字段含义
        
        "应收结算明细本币总开票金额": "应收结算明细本币总开票金额",  # 字段含义
        
        "应收结算明细本币总其他费用": "应收结算明细本币总其他费用",  # 字段含义
        
        "应收结算明细计划产出数量": "应收结算明细计划产出数量",  # 字段含义
        
        "应收结算明细计划需时": "应收结算明细计划需时(小时)",  # 字段含义
        
        "应收结算明细任务数量": "应收结算明细任务数量",  # 字段含义
        
        "应收结算明细单据日期": "应收结算明细单据日期",  # 字段含义
        
        "应收结算明细结算金额": "应收结算明细结算金额",  # 字段含义
        
        "应收结算明细实际结算金额": "应收结算明细实际结算金额",  # 字段含义
        
        "应收结算明细总实际结算差额": "应收结算明细总实际结算差额",  # 字段含义
        
        "应收结算明细总结算金额": "应收结算明细总结算金额",  # 字段含义
        
        "应收结算明细总开票金额": "应收结算明细总开票金额",  # 字段含义
        
        "应收结算明细总开票金额": "应收结算明细总开票金额"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("应收结算明细", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def PAY_SETTLE_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /pay-settle-det/findList
    """
    # 构建请求URL
    url = "/pay-settle-det/findList"  # API地址
    paySettleDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    paySettleDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "paySettleDetPaySettleClazz": "PAY_SETTLE",  # 固定参数
        
        "paySettleDetClazz": "PAY_SETTLE_DET",  # 固定参数
        
        
        "paySettleDetFromCreateTime": paySettleDetFromCreateTime,  # 动态参数
        
        "paySettleDetToCreateTime": paySettleDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "paySettleDetActAmount": {"name": "应付结算明细实际结算金额"},  # 字段映射
        
        "paySettleDetActDiffAmount": {"name": "应付结算明细实际结算差额"},  # 字段映射
        
        "paySettleDetActualTimeRequired": {"name": "应付结算明细实际需时"},  # 字段映射
        
        "paySettleDetAmount": {"name": "应付结算明细结算金额"},  # 字段映射
        
        "paySettleDetAuditDate": {"name": "应付结算明细审核时间"},  # 字段映射
        
        "paySettleDetBeginTime": {"name": "应付结算明细开始时间"},  # 字段映射
        
        "paySettleDetBriefName": {"name": "应付结算明细简称"},  # 字段映射
        
        "paySettleDetCompleteQuantity": {"name": "应付结算明细完成数量"},  # 字段映射
        
        "paySettleDetCompleteStatus": {"name": "应付结算明细完成状态"},  # 字段映射
        
        "paySettleDetDeliveryDate": {"name": "应付结算明细交货日期"},  # 字段映射
        
        "paySettleDetEndTime": {"name": "应付结算明细结束时间"},  # 字段映射
        
        "paySettleDetExchangeRate": {"name": "应付结算明细汇率"},  # 字段映射
        
        "paySettleDetId": {"name": "应付结算明细PK"},  # 字段映射
        
        "paySettleDetLocActAmount": {"name": "应付结算明细本币实际结算金额"},  # 字段映射
        
        "paySettleDetLocActDiffAmount": {"name": "应付结算明细本币实际结算"},  # 字段映射
        
        "paySettleDetLocAmount": {"name": "应付结算明细本币结算金额"},  # 字段映射
        
        "paySettleDetLocOtherExpense": {"name": "应付结算明细本币其他费用"},  # 字段映射
        
        "paySettleDetLocTotalInvoicedAmount": {"name": "应付结算明细本币总开票金额"},  # 字段映射
        
        "paySettleDetPaySettleAcctHolderName": {"name": "应付结算明细账号持有人"},  # 字段映射
        
        "paySettleDetPaySettleActualTimeRequired": {"name": "应付结算明细实际需时"},  # 字段映射
        
        "paySettleDetPaySettleAuditStatus": {"name": "应付结算明细审核状态"},  # 字段映射
        
        "paySettleDetPaySettleBankName": {"name": "应付结算明细银行名称"},  # 字段映射
        
        "paySettleDetPaySettleBriefName": {"name": "应付结算明细简称"},  # 字段映射
        
        "paySettleDetPaySettleCompleteQuantity": {"name": "应付结算明细完成数量"},  # 字段映射
        
        "paySettleDetPaySettleCompleteStatus": {"name": "应付结算明细完成状态"},  # 字段映射
        
        "paySettleDetPaySettleCurrency": {"name": "应付结算明细币种"},  # 字段映射
        
        "paySettleDetPaySettleLocTotalActAmount": {"name": "应付结算明细本币总实际结算金额"},  # 字段映射
        
        "paySettleDetPaySettleLocTotalActDiffAmount": {"name": "应付结算明细本币总实际结算差额"},  # 字段映射
        
        "paySettleDetPaySettleLocTotalAmount": {"name": "应付结算明细本币总结算金额"},  # 字段映射
        
        "paySettleDetPaySettleLocTotalInvoicedAmount": {"name": "应付结算明细本币总开票金额"},  # 字段映射
        
        "paySettleDetPaySettleLocTotalOtherExpense": {"name": "应付结算明细本币总其他费用"},  # 字段映射
        
        "paySettleDetPaySettleSettleAmount": {"name": "应付结算明细结算金额"},  # 字段映射
        
        "paySettleDetPaySettleTotalActAmount": {"name": "应付结算明细实际结算金额"},  # 字段映射
        
        "paySettleDetPaySettleTotalActDiffAmount": {"name": "应付结算明细总实际结算差额"},  # 字段映射
        
        "paySettleDetPaySettleTotalAmount": {"name": "应付结算明细总结算金额"},  # 字段映射
        
        "paySettleDetPaySettleTotalInvoicedAmount": {"name": "应付结算明细总开票金额"},  # 字段映射
        
        "paySettleDetPaySettleTotalOtherExpense": {"name": "应付结算明细总其他费用"},  # 字段映射
        
        "paySettleDetTotalInvoicedAmount": {"name": "应付结算明细总开票金额"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "应付结算明细实际结算金额": "应付结算明细实际结算金额",  # 字段含义
        
        "应付结算明细实际结算差额": "应付结算明细实际结算差额",  # 字段含义
        
        "应付结算明细实际需时": "应付结算明细实际需时(小时)",  # 字段含义
        
        "应付结算明细结算金额": "应付结算明细结算金额",  # 字段含义
        
        "应付结算明细审核时间": "应付结算明细审核时间",  # 字段含义
        
        "应付结算明细开始时间": "应付结算明细开始时间",  # 字段含义
        
        "应付结算明细简称": "应付结算明细简称",  # 字段含义
        
        "应付结算明细完成数量": "应付结算明细完成数量",  # 字段含义
        
        "应付结算明细完成状态": "应付结算明细完成状态",  # 字段含义
        
        "应付结算明细交货日期": "应付结算明细交货日期",  # 字段含义
        
        "应付结算明细结束时间": "应付结算明细结束时间",  # 字段含义
        
        "应付结算明细汇率": "应付结算明细汇率",  # 字段含义
        
        "应付结算明细PK": "应付结算明细PK",  # 字段含义
        
        "应付结算明细本币实际结算金额": "应付结算明细本币实际结算金额",  # 字段含义
        
        "应付结算明细本币实际结算": "应付结算明细本币实际结算",  # 字段含义
        
        "应付结算明细本币结算金额": "应付结算明细本币结算金额",  # 字段含义
        
        "应付结算明细本币其他费用": "应付结算明细本币其他费用",  # 字段含义
        
        "应付结算明细本币总开票金额": "应付结算明细本币总开票金额",  # 字段含义
        
        "应付结算明细账号持有人": "应付结算明细账号持有人",  # 字段含义
        
        "应付结算明细实际需时": "应付结算明细实际需时(小时)",  # 字段含义
        
        "应付结算明细审核状态": "应付结算明细审核状态",  # 字段含义
        
        "应付结算明细银行名称": "应付结算明细银行名称",  # 字段含义
        
        "应付结算明细简称": "应付结算明细简称",  # 字段含义
        
        "应付结算明细完成数量": "应付结算明细完成数量",  # 字段含义
        
        "应付结算明细完成状态": "应付结算明细完成状态",  # 字段含义
        
        "应付结算明细币种": "应付结算明细币种",  # 字段含义
        
        "应付结算明细本币总实际结算金额": "应付结算明细本币总实际结算金额",  # 字段含义
        
        "应付结算明细本币总实际结算差额": "应付结算明细本币总实际结算差额",  # 字段含义
        
        "应付结算明细本币总结算金额": "应付结算明细本币总结算金额",  # 字段含义
        
        "应付结算明细本币总开票金额": "应付结算明细本币总开票金额",  # 字段含义
        
        "应付结算明细本币总其他费用": "应付结算明细本币总其他费用",  # 字段含义
        
        "应付结算明细结算金额": "应付结算明细结算金额",  # 字段含义
        
        "应付结算明细实际结算金额": "应付结算明细实际结算金额",  # 字段含义
        
        "应付结算明细总实际结算差额": "应付结算明细总实际结算差额",  # 字段含义
        
        "应付结算明细总结算金额": "应付结算明细总结算金额",  # 字段含义
        
        "应付结算明细总开票金额": "应付结算明细总开票金额",  # 字段含义
        
        "应付结算明细总其他费用": "应付结算明细总其他费用",  # 字段含义
        
        "应付结算明细总开票金额": "应付结算明细总开票金额"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("应付结算明细", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def RECEIVABLE_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /receivable-det/findList
    """
    # 构建请求URL
    url = "/receivable-det/findList"  # API地址
    receivableDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    receivableDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "receivableDetReceivableClazz": "RECEIVABLE",  # 固定参数
        
        "receivableDetClazz": "RECEIVABLE_DET",  # 固定参数
        
        
        "receivableDetFromCreateTime": receivableDetFromCreateTime,  # 动态参数
        
        "receivableDetToCreateTime": receivableDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "receivableDetActAmount": {"name": "应收账单明细实收/付金额"},  # 字段映射
        
        "receivableDetActDiffAmount": {"name": "应收账单明细实收/付差额"},  # 字段映射
        
        "receivableDetAdvOffAmount": {"name": "应收账单明细预收/付冲抵金额"},  # 字段映射
        
        "receivableDetAmount": {"name": "应收账单明细应收金额"},  # 字段映射
        
        "receivableDetBriefName": {"name": "应收账单明细简称"},  # 字段映射
        
        "receivableDetClosedReason": {"name": "应收账单明细结案原因"},  # 字段映射
        
        "receivableDetClosedStatus": {"name": "应收账单明细结案状态"},  # 字段映射
        
        "receivableDetCompleteQuantity": {"name": "应收账单明细完成数量"},  # 字段映射
        
        "receivableDetCompleteStatus": {"name": "应收账单明细完成状态"},  # 字段映射
        
        "receivableDetDeliveryDate": {"name": "应收账单明细交货日期"},  # 字段映射
        
        "receivableDetEndTime": {"name": "应收账单明细结束时间"},  # 字段映射
        
        "receivableDetExtension": {"name": "应收账单明细扩展数据"},  # 字段映射
        
        "receivableDetId": {"name": "应收账单明细PK"},  # 字段映射
        
        "receivableDetInvoicedAmount": {"name": "应收账单明细已开票金额"},  # 字段映射
        
        "receivableDetInvoicedState": {"name": "应收账单明细开票状态"},  # 字段映射
        
        "receivableDetLocActAmount": {"name": "应收账单明细本币实收/付金额"},  # 字段映射
        
        "receivableDetLocActDiffAmount": {"name": "应收账单明细本币实收/付差额"},  # 字段映射
        
        "receivableDetLocAdvOffAmount": {"name": "应收账单明细本币预收/付冲抵金额"},  # 字段映射
        
        "receivableDetLocAmount": {"name": "应收账单明细本币应收/付金额"},  # 字段映射
        
        "receivableDetLocCompleteQuantity": {"name": "应收账单明细本币完成数量"},  # 字段映射
        
        "receivableDetLocInvoicedAmount": {"name": "应收账单明细本币已开票金额"},  # 字段映射
        
        "receivableDetLocOffActAmount": {"name": "应收账单明细本币冲抵后实收/付金额"},  # 字段映射
        
        "receivableDetLocOffActDiffAmount": {"name": "应收账单明细本币冲抵后实收/付差额"},  # 字段映射
        
        "receivableDetOffActAmount": {"name": "应收账单明细冲抵后实收/付金额"},  # 字段映射
        
        "receivableDetOffActDiffAmount": {"name": "应收账单明细冲抵后实收/付差额"},  # 字段映射
        
        "receivableDetOtherExpense": {"name": "应收账单明细其他费用"},  # 字段映射
        
        "receivableDetPlannedOutputQuantity": {"name": "应收账单明细计划产出数量"},  # 字段映射
        
        "receivableDetPlannedTimeRequired": {"name": "应收账单明细计划需时"},  # 字段映射
        
        "receivableDetQuantity": {"name": "应收账单明细任务数量"},  # 字段映射
        
        "receivableDetReceivableActualTimeRequired": {"name": "应收账单明细实际需时"},  # 字段映射
        
        "receivableDetReceivableAuditDate": {"name": "应收账单明细审核时间"},  # 字段映射
        
        "receivableDetReceivableBankAccount": {"name": "应收账单明细银行账号"},  # 字段映射
        
        "receivableDetReceivableClosedStatus": {"name": "应收账单明细结案状态"},  # 字段映射
        
        "receivableDetReceivableCompleteQuantity": {"name": "应收账单明细完成数量"},  # 字段映射
        
        "receivableDetReceivableCompleteStatus": {"name": "应收账单明细完成状态"},  # 字段映射
        
        "receivableDetReceivableCurrency": {"name": "应收账单明细币种"},  # 字段映射
        
        "receivableDetReceivableDeliveryDate": {"name": "应收账单明细交货日期"},  # 字段映射
        
        "receivableDetReceivableLocCompleteQuantity": {"name": "应收账单明细本币完成数量"},  # 字段映射
        
        "receivableDetReceivableLocTotalActAmount": {"name": "应收账单明细本币总实收/付金额"},  # 字段映射
        
        "receivableDetReceivableLocTotalActDiffAmount": {"name": "应收账单明细本币总实收/付差额"},  # 字段映射
        
        "receivableDetReceivableLocTotalAdvOffAmount": {"name": "应收账单明细本币总预收/付冲抵金额"},  # 字段映射
        
        "receivableDetReceivableLocTotalAmount": {"name": "应收账单明细本币总应收/付金额"},  # 字段映射
        
        "receivableDetReceivableLocTotalInvoicedAmount": {"name": "应收账单明细本币总开票金额"},  # 字段映射
        
        "receivableDetReceivableLocTotalOffActAmount": {"name": "应收账单明细本币总冲抵后实收/付金额"},  # 字段映射
        
        "receivableDetReceivableLocTotalOffActDiffAmount": {"name": "应收账单明细本币总冲抵后实收/付差额"},  # 字段映射
        
        "receivableDetReceivableLocTotalOtherExpense": {"name": "应收账单明细本币总其他费用"},  # 字段映射
        
        "receivableDetReceivablePlannedOutputQuantity": {"name": "应收账单明细计划产出数量"},  # 字段映射
        
        "receivableDetReceivablePlannedTimeRequired": {"name": "应收账单明细计划需时"},  # 字段映射
        
        "receivableDetReceivableTotalActAmount": {"name": "应收账单明细总实收/付金额"},  # 字段映射
        
        "receivableDetReceivableTotalActDiffAmount": {"name": "应收账单明细总实收/付差额"},  # 字段映射
        
        "receivableDetReceivableTotalAdvOffAmount": {"name": "应收账单明细总预收/付冲抵金额"},  # 字段映射
        
        "receivableDetReceivableTotalAmount": {"name": "应收账单明细总应收/付金额"},  # 字段映射
        
        "receivableDetReceivableTotalInvoicedAmount": {"name": "应收账单明细总开票金额"},  # 字段映射
        
        "receivableDetReceivableTotalOffActAmount": {"name": "应收账单明细总冲抵后实收/付金额"},  # 字段映射
        
        "receivableDetReceivableTotalOffActDiffAmount": {"name": "应收账单明细总冲抵后实收/付差额"},  # 字段映射
        
        "receivableDetSettleAmount": {"name": "应收账单明细结算金额"},  # 字段映射
        
        "receivableDetSource": {"name": "应收账单明细源"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "应收账单明细实收/付金额": "应收账单明细实收/付金额",  # 字段含义
        
        "应收账单明细实收/付差额": "应收账单明细实收/付差额",  # 字段含义
        
        "应收账单明细预收/付冲抵金额": "应收账单明细预收/付冲抵金额",  # 字段含义
        
        "应收账单明细应收金额": "应收账单明细应收金额",  # 字段含义
        
        "应收账单明细简称": "应收账单明细简称",  # 字段含义
        
        "应收账单明细结案原因": "应收账单明细结案原因",  # 字段含义
        
        "应收账单明细结案状态": "应收账单明细结案状态",  # 字段含义
        
        "应收账单明细完成数量": "应收账单明细完成数量",  # 字段含义
        
        "应收账单明细完成状态": "应收账单明细完成状态",  # 字段含义
        
        "应收账单明细交货日期": "应收账单明细交货日期",  # 字段含义
        
        "应收账单明细结束时间": "应收账单明细结束时间",  # 字段含义
        
        "应收账单明细扩展数据": "应收账单明细扩展数据",  # 字段含义
        
        "应收账单明细PK": "应收账单明细PK",  # 字段含义
        
        "应收账单明细已开票金额": "应收账单明细已开票金额",  # 字段含义
        
        "应收账单明细开票状态": "应收账单明细开票状态",  # 字段含义
        
        "应收账单明细本币实收/付金额": "应收账单明细本币实收/付金额",  # 字段含义
        
        "应收账单明细本币实收/付差额": "应收账单明细本币实收/付差额",  # 字段含义
        
        "应收账单明细本币预收/付冲抵金额": "应收账单明细本币预收/付冲抵金额",  # 字段含义
        
        "应收账单明细本币应收/付金额": "应收账单明细本币应收/付金额",  # 字段含义
        
        "应收账单明细本币完成数量": "应收账单明细本币完成数量（本币已结算金额）",  # 字段含义
        
        "应收账单明细本币已开票金额": "应收账单明细本币已开票金额",  # 字段含义
        
        "应收账单明细本币冲抵后实收/付金额": "应收账单明细本币冲抵后实收/付金额",  # 字段含义
        
        "应收账单明细本币冲抵后实收/付差额": "应收账单明细本币冲抵后实收/付差额",  # 字段含义
        
        "应收账单明细冲抵后实收/付金额": "应收账单明细冲抵后实收/付金额",  # 字段含义
        
        "应收账单明细冲抵后实收/付差额": "应收账单明细冲抵后实收/付差额",  # 字段含义
        
        "应收账单明细其他费用": "应收账单明细其他费用",  # 字段含义
        
        "应收账单明细计划产出数量": "应收账单明细计划产出数量",  # 字段含义
        
        "应收账单明细计划需时": "应收账单明细计划需时(小时)",  # 字段含义
        
        "应收账单明细任务数量": "应收账单明细任务数量",  # 字段含义
        
        "应收账单明细实际需时": "应收账单明细实际需时(小时)",  # 字段含义
        
        "应收账单明细审核时间": "应收账单明细审核时间",  # 字段含义
        
        "应收账单明细银行账号": "应收账单明细银行账号",  # 字段含义
        
        "应收账单明细结案状态": "应收账单明细结案状态",  # 字段含义
        
        "应收账单明细完成数量": "应收账单明细完成数量",  # 字段含义
        
        "应收账单明细完成状态": "应收账单明细完成状态",  # 字段含义
        
        "应收账单明细币种": "应收账单明细币种",  # 字段含义
        
        "应收账单明细交货日期": "应收账单明细交货日期",  # 字段含义
        
        "应收账单明细本币完成数量": "应收账单明细本币完成数量（本币已结算金额）",  # 字段含义
        
        "应收账单明细本币总实收/付金额": "应收账单明细本币总实收/付金额",  # 字段含义
        
        "应收账单明细本币总实收/付差额": "应收账单明细本币总实收/付差额",  # 字段含义
        
        "应收账单明细本币总预收/付冲抵金额": "应收账单明细本币总预收/付冲抵金额",  # 字段含义
        
        "应收账单明细本币总应收/付金额": "应收账单明细本币总应收/付金额",  # 字段含义
        
        "应收账单明细本币总开票金额": "应收账单明细本币总开票金额",  # 字段含义
        
        "应收账单明细本币总冲抵后实收/付金额": "应收账单明细本币总冲抵后实收/付金额",  # 字段含义
        
        "应收账单明细本币总冲抵后实收/付差额": "应收账单明细本币总冲抵后实收/付差额",  # 字段含义
        
        "应收账单明细本币总其他费用": "应收账单明细本币总其他费用",  # 字段含义
        
        "应收账单明细计划产出数量": "应收账单明细计划产出数量",  # 字段含义
        
        "应收账单明细计划需时": "应收账单明细计划需时(小时)",  # 字段含义
        
        "应收账单明细总实收/付金额": "应收账单明细总实收/付金额",  # 字段含义
        
        "应收账单明细总实收/付差额": "应收账单明细总实收/付差额",  # 字段含义
        
        "应收账单明细总预收/付冲抵金额": "应收账单明细总预收/付冲抵金额",  # 字段含义
        
        "应收账单明细总应收/付金额": "应收账单明细总应收/付金额",  # 字段含义
        
        "应收账单明细总开票金额": "应收账单明细总开票金额",  # 字段含义
        
        "应收账单明细总冲抵后实收/付金额": "应收账单明细总冲抵后实收/付金额",  # 字段含义
        
        "应收账单明细总冲抵后实收/付差额": "应收账单明细总冲抵后实收/付差额",  # 字段含义
        
        "应收账单明细结算金额": "应收账单明细结算金额",  # 字段含义
        
        "应收账单明细源": "应收账单明细源"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("应收账单明细", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def PAYABLE_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /payable-det/findList
    """
    # 构建请求URL
    url = "/payable-det/findList"  # API地址
    payableDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    payableDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "payableDetPayableClazz": "PAYABLE",  # 固定参数
        
        "payableDetClazz": "PAYABLE_DET",  # 固定参数
        
        
        "payableDetFromCreateTime": payableDetFromCreateTime,  # 动态参数
        
        "payableDetToCreateTime": payableDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "payableDetActAmount": {"name": "应付账单明细实收/付金额"},  # 字段映射
        
        "payableDetActDiffAmount": {"name": "应付账单明细实收/付差额"},  # 字段映射
        
        "payableDetActualTimeRequired": {"name": "应付账单明细实际需时"},  # 字段映射
        
        "payableDetAdjustmentTimeRequired": {"name": "应付账单明细调整需时"},  # 字段映射
        
        "payableDetAdvOffAmount": {"name": "应付账单明细预收/付冲抵金额"},  # 字段映射
        
        "payableDetAmount": {"name": "应付账单明细应收金额"},  # 字段映射
        
        "payableDetAuditStatus": {"name": "应付账单明细审核状态"},  # 字段映射
        
        "payableDetAvailableScheduleId": {"name": "应付账单明细可用日程id"},  # 字段映射
        
        "payableDetBriefName": {"name": "应付账单明细简称"},  # 字段映射
        
        "payableDetClosedReason": {"name": "应付账单明细结案原因"},  # 字段映射
        
        "payableDetCompleteQuantity": {"name": "应付账单明细完成数量"},  # 字段映射
        
        "payableDetCompleteStatus": {"name": "应付账单明细完成状态"},  # 字段映射
        
        "payableDetDeliveryDate": {"name": "应付账单明细交货日期"},  # 字段映射
        
        "payableDetExternalState": {"name": "应付账单明细上流程状态位"},  # 字段映射
        
        "payableDetId": {"name": "应付账单明细PK"},  # 字段映射
        
        "payableDetLocActAmount": {"name": "应付账单明细本币实收/付金额"},  # 字段映射
        
        "payableDetLocActDiffAmount": {"name": "应付账单明细本币实收/付差额"},  # 字段映射
        
        "payableDetLocAdvOffAmount": {"name": "应付账单明细本币预收/付冲抵金额"},  # 字段映射
        
        "payableDetLocAmount": {"name": "应付账单明细本币应收/付金额"},  # 字段映射
        
        "payableDetLocCompleteQuantity": {"name": "应付账单明细本币完成数量"},  # 字段映射
        
        "payableDetLocInvoicedAmount": {"name": "应付账单明细本币已开票金额"},  # 字段映射
        
        "payableDetLocOffActAmount": {"name": "应付账单明细本币冲抵后实收/付金额"},  # 字段映射
        
        "payableDetLocOffActDiffAmount": {"name": "应付账单明细本币冲抵后实收/付差额"},  # 字段映射
        
        "payableDetLocOtherExpense": {"name": "应付账单明细本币其他费用"},  # 字段映射
        
        "payableDetOffActAmount": {"name": "应付账单明细冲抵后实收/付金额"},  # 字段映射
        
        "payableDetOffActDiffAmount": {"name": "应付账单明细冲抵后实收/付差额"},  # 字段映射
        
        "payableDetPayableCompleteQuantity": {"name": "应付账单明细完成数量"},  # 字段映射
        
        "payableDetPayableCompleteStatus": {"name": "应付账单明细完成状态"},  # 字段映射
        
        "payableDetPayableDeliveryDate": {"name": "应付账单明细交货日期"},  # 字段映射
        
        "payableDetPayableQuantity": {"name": "应付账单明细任务数量"},  # 字段映射
        
        "payableDetPayableReceiptDate": {"name": "应付账单明细单据日期"},  # 字段映射
        
        "payableDetPayableState": {"name": "应付账单明细通用状态"},  # 字段映射
        
        "payableDetPayableTotalActAmount": {"name": "应付账单明细总实收/付金额"},  # 字段映射
        
        "payableDetPayableTotalActDiffAmount": {"name": "应付账单明细总实收/付差额"},  # 字段映射
        
        "payableDetPayableTotalAdvOffAmount": {"name": "应付账单明细总预收/付冲抵金额"},  # 字段映射
        
        "payableDetPayableTotalAmount": {"name": "应付账单明细总应收/付金额"},  # 字段映射
        
        "payableDetPayableTotalInvoicedAmount": {"name": "应付账单明细总开票金额"},  # 字段映射
        
        "payableDetPayableTotalOffActAmount": {"name": "应付账单明细总冲抵后实收/付金额"},  # 字段映射
        
        "payableDetPayableTotalOffActDiffAmount": {"name": "应付账单明细总冲抵后实收/付差额"},  # 字段映射
        
        "payableDetPayableTotalOtherExpense": {"name": "应付账单明细总其他费用"},  # 字段映射
        
        "payableDetWorkOrderId": {"name": "应付账单明细工单ID"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "应付账单明细实收/付金额": "应付账单明细实收/付金额",  # 字段含义
        
        "应付账单明细实收/付差额": "应付账单明细实收/付差额",  # 字段含义
        
        "应付账单明细实际需时": "应付账单明细实际需时(小时)",  # 字段含义
        
        "应付账单明细调整需时": "应付账单明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "应付账单明细预收/付冲抵金额": "应付账单明细预收/付冲抵金额",  # 字段含义
        
        "应付账单明细应收金额": "应付账单明细应收金额",  # 字段含义
        
        "应付账单明细审核状态": "应付账单明细审核状态",  # 字段含义
        
        "应付账单明细可用日程id": "应付账单明细可用日程id",  # 字段含义
        
        "应付账单明细简称": "应付账单明细简称",  # 字段含义
        
        "应付账单明细结案原因": "应付账单明细结案原因",  # 字段含义
        
        "应付账单明细完成数量": "应付账单明细完成数量",  # 字段含义
        
        "应付账单明细完成状态": "应付账单明细完成状态",  # 字段含义
        
        "应付账单明细交货日期": "应付账单明细交货日期",  # 字段含义
        
        "应付账单明细上流程状态位": "应付账单明细上流程状态位。0-未开始；1-进行中；2-异常；3-结束；4-中止；5-关闭",  # 字段含义
        
        "应付账单明细PK": "应付账单明细PK",  # 字段含义
        
        "应付账单明细本币实收/付金额": "应付账单明细本币实收/付金额",  # 字段含义
        
        "应付账单明细本币实收/付差额": "应付账单明细本币实收/付差额",  # 字段含义
        
        "应付账单明细本币预收/付冲抵金额": "应付账单明细本币预收/付冲抵金额",  # 字段含义
        
        "应付账单明细本币应收/付金额": "应付账单明细本币应收/付金额",  # 字段含义
        
        "应付账单明细本币完成数量": "应付账单明细本币完成数量（本币已结算金额）",  # 字段含义
        
        "应付账单明细本币已开票金额": "应付账单明细本币已开票金额",  # 字段含义
        
        "应付账单明细本币冲抵后实收/付金额": "应付账单明细本币冲抵后实收/付金额",  # 字段含义
        
        "应付账单明细本币冲抵后实收/付差额": "应付账单明细本币冲抵后实收/付差额",  # 字段含义
        
        "应付账单明细本币其他费用": "应付账单明细本币其他费用",  # 字段含义
        
        "应付账单明细冲抵后实收/付金额": "应付账单明细冲抵后实收/付金额",  # 字段含义
        
        "应付账单明细冲抵后实收/付差额": "应付账单明细冲抵后实收/付差额",  # 字段含义
        
        "应付账单明细完成数量": "应付账单明细完成数量",  # 字段含义
        
        "应付账单明细完成状态": "应付账单明细完成状态",  # 字段含义
        
        "应付账单明细交货日期": "应付账单明细交货日期",  # 字段含义
        
        "应付账单明细任务数量": "应付账单明细任务数量",  # 字段含义
        
        "应付账单明细单据日期": "应付账单明细单据日期",  # 字段含义
        
        "应付账单明细通用状态": "应付账单明细通用状态",  # 字段含义
        
        "应付账单明细总实收/付金额": "应付账单明细总实收/付金额",  # 字段含义
        
        "应付账单明细总实收/付差额": "应付账单明细总实收/付差额",  # 字段含义
        
        "应付账单明细总预收/付冲抵金额": "应付账单明细总预收/付冲抵金额",  # 字段含义
        
        "应付账单明细总应收/付金额": "应付账单明细总应收/付金额",  # 字段含义
        
        "应付账单明细总开票金额": "应付账单明细总开票金额",  # 字段含义
        
        "应付账单明细总冲抵后实收/付金额": "应付账单明细总冲抵后实收/付金额",  # 字段含义
        
        "应付账单明细总冲抵后实收/付差额": "应付账单明细总冲抵后实收/付差额",  # 字段含义
        
        "应付账单明细总其他费用": "应付账单明细总其他费用",  # 字段含义
        
        "应付账单明细工单ID": "应付账单明细工单ID"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("应付账单明细", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)


if __name__ == "__main__":
    access_token = auth_login()  # 获取访问令牌
    
    REC_SETTLE_DET_test(access_token)  # 调用测试函数
    
    PAY_SETTLE_DET_test(access_token)  # 调用测试函数
    
    RECEIVABLE_DET_test(access_token)  # 调用测试函数
    
    PAYABLE_DET_test(access_token)  # 调用测试函数
    