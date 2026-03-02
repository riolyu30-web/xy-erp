
import sys # 导入sys模块
import os # 导入os模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将上上级目录添加到系统路径
from datetime import datetime, timedelta # 导入日期时间模块
from services.auth_service import auth_login # 导入登录认证模块
from services.tool import fetch_data  # 导入工具函数
import json # 导入json模块


def PROD_PRCES_APPLY_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /prod-prces-apply-det/findList
    """
    # 当前方法名
    function_name = "PROD_PRCES_APPLY_DET"
    # 构建请求URL
    url = "/prod-prces-apply-det/findList"  # API地址
    prodPrcesApplyDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    prodPrcesApplyDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "prodPrcesApplyDetProdPrcesApplyClazz": "PROD_PRCES_APPLY",  # 固定参数
        
        "prodPrcesApplyDetClazz": "PROD_PRCES_APPLY_DET",  # 固定参数
        
        
        "prodPrcesApplyDetFromCreateTime": prodPrcesApplyDetFromCreateTime,  # 动态参数
        
        "prodPrcesApplyDetToCreateTime": prodPrcesApplyDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "prodPrcesApplyDetActualTimeRequired": {"name": "生产加工申请明细实际需时"},  # 字段映射
        
        "prodPrcesApplyDetApplicationId": {"name": "生产加工申请明细应用ID"},  # 字段映射
        
        "prodPrcesApplyDetAuditDate": {"name": "生产加工申请明细审核时间"},  # 字段映射
        
        "prodPrcesApplyDetAuditStatus": {"name": "生产加工申请明细审核状态"},  # 字段映射
        
        "prodPrcesApplyDetBeginTime": {"name": "生产加工申请明细开始时间"},  # 字段映射
        
        "prodPrcesApplyDetBriefName": {"name": "生产加工申请明细简称"},  # 字段映射
        
        "prodPrcesApplyDetDeliveryDate": {"name": "生产加工申请明细交货日期"},  # 字段映射
        
        "prodPrcesApplyDetEndTime": {"name": "生产加工申请明细结束时间"},  # 字段映射
        
        "prodPrcesApplyDetExchangeRateId": {"name": "生产加工申请明细币种汇率id"},  # 字段映射
        
        "prodPrcesApplyDetId": {"name": "生产加工申请明细PK"},  # 字段映射
        
        "prodPrcesApplyDetPlannedOutputQuantity": {"name": "生产加工申请明细计划产出数量"},  # 字段映射
        
        "prodPrcesApplyDetPlannedTimeRequired": {"name": "生产加工申请明细计划需时"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyActualTimeRequired": {"name": "生产加工申请明细实际需时"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyAdjustmentTimeRequired": {"name": "生产加工申请明细调整需时"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyAvailableScheduleId": {"name": "生产加工申请明细可用日程id"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyCompleteQuantity": {"name": "生产加工申请明细完成数量"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyExchangeRateId": {"name": "生产加工申请明细币种汇率id"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyProductionProcessesTypeId": {"name": "生产加工申请明细工序类型ID"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyProductionShiftId": {"name": "生产加工申请明细生产班次ID"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyQuantity": {"name": "生产加工申请明细任务数量"},  # 字段映射
        
        "prodPrcesApplyDetProdPrcesApplyState": {"name": "生产加工申请明细通用状态"},  # 字段映射
        
        "prodPrcesApplyDetQuantity": {"name": "生产加工申请明细任务数量"},  # 字段映射
        
        "prodPrcesApplyDetReceiptDate": {"name": "生产加工申请明细单据日期"},  # 字段映射
        
        "prodPrcesApplyDetReceiptType": {"name": "生产加工申请明细单据类型"},  # 字段映射
        
        "prodPrcesApplyDetRelatedTasksId": {"name": "生产加工申请明细关联任务id"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "生产加工申请明细实际需时": "生产加工申请明细实际需时(小时)",  # 字段含义
        
        "生产加工申请明细应用ID": "生产加工申请明细应用ID",  # 字段含义
        
        "生产加工申请明细审核时间": "生产加工申请明细审核时间",  # 字段含义
        
        "生产加工申请明细审核状态": "生产加工申请明细审核状态",  # 字段含义
        
        "生产加工申请明细开始时间": "生产加工申请明细开始时间",  # 字段含义
        
        "生产加工申请明细简称": "生产加工申请明细简称",  # 字段含义
        
        "生产加工申请明细交货日期": "生产加工申请明细交货日期",  # 字段含义
        
        "生产加工申请明细结束时间": "生产加工申请明细结束时间",  # 字段含义
        
        "生产加工申请明细币种汇率id": "生产加工申请明细币种汇率id",  # 字段含义
        
        "生产加工申请明细PK": "生产加工申请明细PK",  # 字段含义
        
        "生产加工申请明细计划产出数量": "生产加工申请明细计划产出数量",  # 字段含义
        
        "生产加工申请明细计划需时": "生产加工申请明细计划需时(小时)",  # 字段含义
        
        "生产加工申请明细实际需时": "生产加工申请明细实际需时(小时)",  # 字段含义
        
        "生产加工申请明细调整需时": "生产加工申请明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "生产加工申请明细可用日程id": "生产加工申请明细可用日程id",  # 字段含义
        
        "生产加工申请明细完成数量": "生产加工申请明细完成数量",  # 字段含义
        
        "生产加工申请明细币种汇率id": "生产加工申请明细币种汇率id",  # 字段含义
        
        "生产加工申请明细工序类型ID": "生产加工申请明细工序类型ID",  # 字段含义
        
        "生产加工申请明细生产班次ID": "生产加工申请明细生产班次ID",  # 字段含义
        
        "生产加工申请明细任务数量": "生产加工申请明细任务数量",  # 字段含义
        
        "生产加工申请明细通用状态": "生产加工申请明细通用状态",  # 字段含义
        
        "生产加工申请明细任务数量": "生产加工申请明细任务数量",  # 字段含义
        
        "生产加工申请明细单据日期": "生产加工申请明细单据日期",  # 字段含义
        
        "生产加工申请明细单据类型": "生产加工申请明细单据类型（一个常量值，与node里的defaultTypeId不一样，推荐使用字典）",  # 字段含义
        
        "生产加工申请明细关联任务id": "生产加工申请明细关联任务id"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("生产加工申请明细", function_name, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def MAT_OUT_APY_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /mat-out-apy-det/findList
    """
    # 当前方法名
    function_name = "MAT_OUT_APY_DET"
    # 构建请求URL
    url = "/mat-out-apy-det/findList"  # API地址
    matOutApyDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    matOutApyDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "matOutApyDetMatOutApyClazz": "MAT_OUT_APY",  # 固定参数
        
        "matOutApyDetClazz": "MAT_OUT_APY_DET",  # 固定参数
        
        
        "matOutApyDetFromCreateTime": matOutApyDetFromCreateTime,  # 动态参数
        
        "matOutApyDetToCreateTime": matOutApyDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "matOutApyDetActualTimeRequired": {"name": "物料出库申请明细实际需时"},  # 字段映射
        
        "matOutApyDetAdjustmentTimeRequired": {"name": "物料出库申请明细调整需时"},  # 字段映射
        
        "matOutApyDetApplicationId": {"name": "物料出库申请明细应用ID"},  # 字段映射
        
        "matOutApyDetAuditDate": {"name": "物料出库申请明细审核时间"},  # 字段映射
        
        "matOutApyDetAuditStatus": {"name": "物料出库申请明细审核状态"},  # 字段映射
        
        "matOutApyDetBriefName": {"name": "物料出库申请明细简称"},  # 字段映射
        
        "matOutApyDetDeliveryDate": {"name": "物料出库申请明细交货日期"},  # 字段映射
        
        "matOutApyDetEndTime": {"name": "物料出库申请明细结束时间"},  # 字段映射
        
        "matOutApyDetExchangeRateId": {"name": "物料出库申请明细币种汇率id"},  # 字段映射
        
        "matOutApyDetId": {"name": "物料出库申请明细主键id"},  # 字段映射
        
        "matOutApyDetMatOutApyActualTimeRequired": {"name": "物料出库申请明细实际需时"},  # 字段映射
        
        "matOutApyDetMatOutApyAdjustmentTimeRequired": {"name": "物料出库申请明细调整需时"},  # 字段映射
        
        "matOutApyDetMatOutApyApplyReason": {"name": "物料出库申请明细申请原因"},  # 字段映射
        
        "matOutApyDetMatOutApyAuditDate": {"name": "物料出库申请明细审核时间"},  # 字段映射
        
        "matOutApyDetMatOutApyBriefName": {"name": "物料出库申请明细简称"},  # 字段映射
        
        "matOutApyDetPlannedOutputQuantity": {"name": "物料出库申请明细计划产出数量"},  # 字段映射
        
        "matOutApyDetPlannedTimeRequired": {"name": "物料出库申请明细计划需时"},  # 字段映射
        
        "matOutApyDetProductionShiftId": {"name": "物料出库申请明细生产班次ID"},  # 字段映射
        
        "matOutApyDetQuantity": {"name": "物料出库申请明细任务数量"},  # 字段映射
        
        "matOutApyDetState": {"name": "物料出库申请明细通用状态"},  # 字段映射
        
        "matOutApyDetUpdateTime": {"name": "物料出库申请明细更新时间"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "物料出库申请明细实际需时": "物料出库申请明细实际需时(小时)",  # 字段含义
        
        "物料出库申请明细调整需时": "物料出库申请明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "物料出库申请明细应用ID": "物料出库申请明细应用ID",  # 字段含义
        
        "物料出库申请明细审核时间": "物料出库申请明细审核时间",  # 字段含义
        
        "物料出库申请明细审核状态": "物料出库申请明细审核状态",  # 字段含义
        
        "物料出库申请明细简称": "物料出库申请明细简称",  # 字段含义
        
        "物料出库申请明细交货日期": "物料出库申请明细交货日期",  # 字段含义
        
        "物料出库申请明细结束时间": "物料出库申请明细结束时间",  # 字段含义
        
        "物料出库申请明细币种汇率id": "物料出库申请明细币种汇率id",  # 字段含义
        
        "物料出库申请明细主键id": "物料出库申请明细主键id",  # 字段含义
        
        "物料出库申请明细实际需时": "物料出库申请明细实际需时(小时)",  # 字段含义
        
        "物料出库申请明细调整需时": "物料出库申请明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "物料出库申请明细申请原因": "物料出库申请明细申请原因",  # 字段含义
        
        "物料出库申请明细审核时间": "物料出库申请明细审核时间",  # 字段含义
        
        "物料出库申请明细简称": "物料出库申请明细简称",  # 字段含义
        
        "物料出库申请明细计划产出数量": "物料出库申请明细计划产出数量",  # 字段含义
        
        "物料出库申请明细计划需时": "物料出库申请明细计划需时(小时)",  # 字段含义
        
        "物料出库申请明细生产班次ID": "物料出库申请明细生产班次ID",  # 字段含义
        
        "物料出库申请明细任务数量": "物料出库申请明细任务数量",  # 字段含义
        
        "物料出库申请明细通用状态": "物料出库申请明细通用状态",  # 字段含义
        
        "物料出库申请明细更新时间": "物料出库申请明细更新时间"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("物料出库申请明细", function_name, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def SAM_ORDER_NOTICE_DET_test(access_token: str):  # 定义测试函数
    """
    测试 /sam-order-notice-det/findList
    """
    # 当前方法名
    function_name = "SAM_ORDER_NOTICE_DET"
    # 构建请求URL
    url = "/sam-order-notice-det/findList"  # API地址
    samOrderNoticeDetFromCreateTime = (datetime.now() - timedelta(days=30)).strftime("YYYY-%m-DD %H:%M:%S")
    samOrderNoticeDetToCreateTime = datetime.now().strftime("YYYY-%m-DD %H:%M:%S")

    # 构建请求体数据
    data = {
        
        "samOrderNoticeDetSamOrderNoticeClazz": "SAM_ORDER_NOTICE",  # 固定参数
        
        "samOrderNoticeDetClazz": "SAM_ORDER_NOTICE_DET",  # 固定参数
        
        
        "samOrderNoticeDetFromCreateTime": samOrderNoticeDetFromCreateTime,  # 动态参数
        
        "samOrderNoticeDetToCreateTime": samOrderNoticeDetToCreateTime,  # 动态参数
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "samOrderNoticeDetActualTimeRequired": {"name": "打样通知单明细实际需时"},  # 字段映射
        
        "samOrderNoticeDetAdjustmentTimeRequired": {"name": "打样通知单明细调整需时"},  # 字段映射
        
        "samOrderNoticeDetAuditDate": {"name": "打样通知单明细审核时间"},  # 字段映射
        
        "samOrderNoticeDetAuditStatus": {"name": "打样通知单明细审核状态"},  # 字段映射
        
        "samOrderNoticeDetBeginTime": {"name": "打样通知单明细开始时间"},  # 字段映射
        
        "samOrderNoticeDetBizOrderDetQuantity": {"name": "打样通知单明细已开业务订单数量"},  # 字段映射
        
        "samOrderNoticeDetBizOrderDetSpareQuantity": {"name": "打样通知单明细已开业务订单备品数量"},  # 字段映射
        
        "samOrderNoticeDetBizOrderDetSpareStatus": {"name": "打样通知单明细已开业务订单备品状态"},  # 字段映射
        
        "samOrderNoticeDetBizOrderDetStatus": {"name": "打样通知单明细已开业务订单状态"},  # 字段映射
        
        "samOrderNoticeDetCompleteQuantity": {"name": "打样通知单明细完成数量"},  # 字段映射
        
        "samOrderNoticeDetCompleteStatus": {"name": "打样通知单明细完成状态"},  # 字段映射
        
        "samOrderNoticeDetCreateTime": {"name": "打样通知单明细创建时间"},  # 字段映射
        
        "samOrderNoticeDetDeliveryDate": {"name": "打样通知单明细交货日期"},  # 字段映射
        
        "samOrderNoticeDetEndTime": {"name": "打样通知单明细结束时间"},  # 字段映射
        
        "samOrderNoticeDetId": {"name": "打样通知单明细pk"},  # 字段映射
        
        "samOrderNoticeDetPlannedOutputQuantity": {"name": "打样通知单明细计划产出数量"},  # 字段映射
        
        "samOrderNoticeDetPlannedTimeRequired": {"name": "打样通知单明细计划需时"},  # 字段映射
        
        "samOrderNoticeDetQuantity": {"name": "打样通知单明细任务数量"},  # 字段映射
        
        "samOrderNoticeDetSamOrderNoticeCompleteQuantity": {"name": "打样通知单明细完成数量"},  # 字段映射
        
        "samOrderNoticeDetSamOrderNoticeCompleteStatus": {"name": "打样通知单明细完成状态"},  # 字段映射
        
        "samOrderNoticeDetSamOrderNoticePlannedOutputQuantity": {"name": "打样通知单明细计划产出数量"},  # 字段映射
        
        "samOrderNoticeDetSamOrderNoticePlannedTimeRequired": {"name": "打样通知单明细计划需时"},  # 字段映射
        
        "samOrderNoticeDetSamOrderNoticeQuantity": {"name": "打样通知单明细任务数量"},  # 字段映射
        
        "samOrderNoticeDetSamOrderNoticeReasonDesc": {"name": "打样通知单明细研发原因描述"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "打样通知单明细实际需时": "打样通知单明细实际需时(小时)",  # 字段含义
        
        "打样通知单明细调整需时": "打样通知单明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "打样通知单明细审核时间": "打样通知单明细审核时间",  # 字段含义
        
        "打样通知单明细审核状态": "打样通知单明细审核状态",  # 字段含义
        
        "打样通知单明细开始时间": "打样通知单明细开始时间",  # 字段含义
        
        "打样通知单明细已开业务订单数量": "打样通知单明细已开业务订单数量（业务订单反写）",  # 字段含义
        
        "打样通知单明细已开业务订单备品数量": "打样通知单明细已开业务订单备品数量（业务订单反写）",  # 字段含义
        
        "打样通知单明细已开业务订单备品状态": "打样通知单明细已开业务订单备品状态（业务订单反写）",  # 字段含义
        
        "打样通知单明细已开业务订单状态": "打样通知单明细已开业务订单状态（业务订单反写）",  # 字段含义
        
        "打样通知单明细完成数量": "打样通知单明细完成数量",  # 字段含义
        
        "打样通知单明细完成状态": "打样通知单明细完成状态",  # 字段含义
        
        "打样通知单明细创建时间": "打样通知单明细创建时间",  # 字段含义
        
        "打样通知单明细交货日期": "打样通知单明细交货日期",  # 字段含义
        
        "打样通知单明细结束时间": "打样通知单明细结束时间",  # 字段含义
        
        "打样通知单明细pk": "打样通知单明细pk",  # 字段含义
        
        "打样通知单明细计划产出数量": "打样通知单明细计划产出数量",  # 字段含义
        
        "打样通知单明细计划需时": "打样通知单明细计划需时(小时)",  # 字段含义
        
        "打样通知单明细任务数量": "打样通知单明细任务数量",  # 字段含义
        
        "打样通知单明细完成数量": "打样通知单明细完成数量",  # 字段含义
        
        "打样通知单明细完成状态": "打样通知单明细完成状态",  # 字段含义
        
        "打样通知单明细计划产出数量": "打样通知单明细计划产出数量",  # 字段含义
        
        "打样通知单明细计划需时": "打样通知单明细计划需时(小时)",  # 字段含义
        
        "打样通知单明细任务数量": "打样通知单明细任务数量",  # 字段含义
        
        "打样通知单明细研发原因描述": "打样通知单明细研发原因描述"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("打样通知单明细", function_name, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def PROCESSES_TYPE_test(access_token: str):  # 定义测试函数
    """
    测试 /processes-type/findList
    """
    # 当前方法名
    function_name = "PROCESSES_TYPE"
    # 构建请求URL
    url = "/processes-type/findList"  # API地址

    # 构建请求体数据
    data = {
        
        "prcesTypeClazz": "PROCESSES_TYPE",  # 固定参数
        
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "prcesTypeAuditStatus": {"name": "工序类型审核状态"},  # 字段映射
        
        "prcesTypeBriefName": {"name": "工序类型简称"},  # 字段映射
        
        "prcesTypeExternalState": {"name": "工序类型上流程状态位"},  # 字段映射
        
        "prcesTypeId": {"name": "工序类型主键ID"},  # 字段映射
        
        "prcesTypeState": {"name": "工序类型通用状态"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "工序类型审核状态": "工序类型审核状态",  # 字段含义
        
        "工序类型简称": "工序类型简称",  # 字段含义
        
        "工序类型上流程状态位": "工序类型上流程状态位。0-未开始；1-进行中；2-异常；3-结束；4-中止；5-关闭",  # 字段含义
        
        "工序类型主键ID": "工序类型主键ID",  # 字段含义
        
        "工序类型通用状态": "工序类型通用状态"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("工序类型", function_name, data, access_token, filtered_fields, meaning_list, debug_mode=True)

def EQUIPMENT_test(access_token: str):  # 定义测试函数
    """
    测试 /equ/findList
    """
    # 当前方法名
    function_name = "EQUIPMENT"
    # 构建请求URL
    url = "/equ/findList"  # API地址

    # 构建请求体数据
    data = {
        
        "equClazz": "EQUIPMENT",  # 固定参数
        
        
        
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        
        "equAccDep": {"name": "设备表累计折旧"},  # 字段映射
        
        "equApplicationId": {"name": "设备表应用ID"},  # 字段映射
        
        "equAuditDate": {"name": "设备表审核时间"},  # 字段映射
        
        "equBizVersion": {"name": "设备表业务自定义版本号"},  # 字段映射
        
        "equBrand": {"name": "设备表品牌"},  # 字段映射
        
        "equBriefName": {"name": "设备表简称"},  # 字段映射
        
        "equCheckTime": {"name": "设备表校机时间"},  # 字段映射
        
        "equDailyProductionCapacity": {"name": "设备表每日产能"},  # 字段映射
        
        "equId": {"name": "设备表主键ID"},  # 字段映射
        
        "equIsProductionEquipment": {"name": "设备表是否生产设备"},  # 字段映射
        
        "equMaxProcessLength": {"name": "设备表最大加工长"},  # 字段映射
        
        "equMaxProcessWidth": {"name": "设备表最大加工宽"},  # 字段映射
        
        "equMaxUsageCount": {"name": "设备表最大使用次数"},  # 字段映射
        
        "equMinProcessLength": {"name": "设备表最小加工长"},  # 字段映射
        
        "equMinProcessWidth": {"name": "设备表最小加工宽"},  # 字段映射
        
        "equPurDate": {"name": "设备表采购日期"},  # 字段映射
        
        "equRunStatus": {"name": "设备表运行状态"},  # 字段映射
        
        "equRunTime": {"name": "设备表每日运行时长"},  # 字段映射
        
        "equSerialNumber": {"name": "设备表顺序号"},  # 字段映射
        
        "equUsageCount": {"name": "设备表已使用次数"},  # 字段映射
        
        "equUsageRate": {"name": "设备表使用率"},  # 字段映射
        
        "equWarrantyEndDate": {"name": "设备表保修截止日期"}  # 字段映射
        
    }  # 过滤字段字典结束

    meaning_list = {
        
        "设备表累计折旧": "设备表累计折旧",  # 字段含义
        
        "设备表应用ID": "设备表应用ID",  # 字段含义
        
        "设备表审核时间": "设备表审核时间",  # 字段含义
        
        "设备表业务自定义版本号": "设备表业务自定义版本号",  # 字段含义
        
        "设备表品牌": "设备表品牌",  # 字段含义
        
        "设备表简称": "设备表简称",  # 字段含义
        
        "设备表校机时间": "设备表校机时间",  # 字段含义
        
        "设备表每日产能": "设备表每日产能(小时)",  # 字段含义
        
        "设备表主键ID": "设备表主键ID",  # 字段含义
        
        "设备表是否生产设备": "设备表是否生产设备",  # 字段含义
        
        "设备表最大加工长": "设备表最大加工长",  # 字段含义
        
        "设备表最大加工宽": "设备表最大加工宽",  # 字段含义
        
        "设备表最大使用次数": "设备表最大使用次数",  # 字段含义
        
        "设备表最小加工长": "设备表最小加工长",  # 字段含义
        
        "设备表最小加工宽": "设备表最小加工宽",  # 字段含义
        
        "设备表采购日期": "设备表采购日期",  # 字段含义
        
        "设备表运行状态": "设备表运行状态",  # 字段含义
        
        "设备表每日运行时长": "设备表每日运行时长(小时)",  # 字段含义
        
        "设备表顺序号": "设备表顺序号",  # 字段含义
        
        "设备表已使用次数": "设备表已使用次数",  # 字段含义
        
        "设备表使用率": "设备表使用率",  # 字段含义
        
        "设备表保修截止日期": "设备表保修截止日期"  # 字段含义
        
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("设备表", function_name, data, access_token, filtered_fields, meaning_list, debug_mode=True)


if __name__ == "__main__":
    access_token = auth_login()  # 获取访问令牌
    
    PROD_PRCES_APPLY_DET_test(access_token)  # 调用测试函数
    
    MAT_OUT_APY_DET_test(access_token)  # 调用测试函数
    
    SAM_ORDER_NOTICE_DET_test(access_token)  # 调用测试函数
    
    PROCESSES_TYPE_test(access_token)  # 调用测试函数
    
    EQUIPMENT_test(access_token)  # 调用测试函数
    