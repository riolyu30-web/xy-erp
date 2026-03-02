from fastmcp import FastMCP  # 导入FastMCP框架
from services.tool import fetch_data  # 导入工具函数
from datetime import datetime, timedelta # 导入日期时间模块
import json  # 导入JSON库
quality_mcp = FastMCP(name="quality")  # 创建计算服务MCP实例


@quality_mcp.tool()  # 注册工具
def CUST_COMP_DET(access_token: str,custCompDetFromCreateTime:str=None,custCompDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    客户投诉明细表，客户投诉
    
    Args:
        access_token: 访问令牌
        
        custCompDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        custCompDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "CUST_COMP_DET"
    # 构建请求URL
    url = "/cust-comp-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "custCompDetCustCompClazz": "CUST_COMP",  # 固定参数
        
        "custCompDetClazz": "CUST_COMP_DET",  # 固定参数
        
        
        "custCompDetFromCreateTime": custCompDetFromCreateTime,  # 动态参数
        
        "custCompDetToCreateTime": custCompDetToCreateTime,  # 动态参数
        
        "key": "CUST_COMP_DET",
        "from": custCompDetFromCreateTime,
        "to": custCompDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "custCompDetActualTimeRequired": {"name": "客户投诉明细表实际需时"},  # 字段映射
        
        "custCompDetAuditDate": {"name": "客户投诉明细表审核时间"},  # 字段映射
        
        "custCompDetAuditStatus": {"name": "客户投诉明细表审核状态"},  # 字段映射
        
        "custCompDetBriefName": {"name": "客户投诉明细表简称"},  # 字段映射
        
        "custCompDetClosedReason": {"name": "客户投诉明细表结案原因"},  # 字段映射
        
        "custCompDetCustCompAccountability": {"name": "客户投诉明细表责任归属"},  # 字段映射
        
        "custCompDetCustCompActualTimeRequired": {"name": "客户投诉明细表实际需时"},  # 字段映射
        
        "custCompDetCustCompAdjustmentTimeRequired": {"name": "客户投诉明细表调整需时"},  # 字段映射
        
        "custCompDetCustCompChannelId": {"name": "客户投诉明细表投诉渠道"},  # 字段映射
        
        "custCompDetCustCompClosedReason": {"name": "客户投诉明细表结案原因"},  # 字段映射
        
        "custCompDetCustCompClosedStatus": {"name": "客户投诉明细表结案状态"},  # 字段映射
        
        "custCompDetCustCompComplaintsContent": {"name": "客户投诉明细表投诉详细内容"},  # 字段映射
        
        "custCompDetCustCompComplaintsReason": {"name": "客户投诉明细表投诉原因"},  # 字段映射
        
        "custCompDetId": {"name": "客户投诉明细表PK"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "客户投诉明细表实际需时": "客户投诉明细表实际需时(小时)",  # 字段含义
        
        "客户投诉明细表审核时间": "客户投诉明细表审核时间",  # 字段含义
        
        "客户投诉明细表审核状态": "客户投诉明细表审核状态",  # 字段含义
        
        "客户投诉明细表简称": "客户投诉明细表简称",  # 字段含义
        
        "客户投诉明细表结案原因": "客户投诉明细表结案原因",  # 字段含义
        
        "客户投诉明细表责任归属": "客户投诉明细表责任归属(字典：生产责任、客户责任、业助责任、供应商责任、无法判断等)",  # 字段含义
        
        "客户投诉明细表实际需时": "客户投诉明细表实际需时(小时)",  # 字段含义
        
        "客户投诉明细表调整需时": "客户投诉明细表调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "客户投诉明细表投诉渠道": "客户投诉明细表投诉渠道(字典：微信、Email，口头，电话等)，默认微信，渠道guid",  # 字段含义
        
        "客户投诉明细表结案原因": "客户投诉明细表结案原因",  # 字段含义
        
        "客户投诉明细表结案状态": "客户投诉明细表结案状态",  # 字段含义
        
        "客户投诉明细表投诉详细内容": "客户投诉明细表投诉详细内容(手填)",  # 字段含义
        
        "客户投诉明细表投诉原因": "客户投诉明细表投诉原因(字典：产品质量问题，数量不足)默认产品质量问题",  # 字段含义
        
        "客户投诉明细表PK": "客户投诉明细表PK"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("客户投诉明细表", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@quality_mcp.tool()  # 注册工具
def QUALITY_INSPECT_IQC_DET(access_token: str,qualityInspectIqcDetFromCreateTime:str=None,qualityInspectIqcDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    IQC明细，材料检业务查询
    
    Args:
        access_token: 访问令牌
        
        qualityInspectIqcDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        qualityInspectIqcDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "QUALITY_INSPECT_IQC_DET"
    # 构建请求URL
    url = "/quality-inspect-iqc-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "qualityInspectIqcDetQualityInspectIqcClazz": "QUALITY_INSPECT_IQC",  # 固定参数
        
        "qualityInspectIqcDetClazz": "QUALITY_INSPECT_IQC_DET",  # 固定参数
        
        
        "qualityInspectIqcDetFromCreateTime": qualityInspectIqcDetFromCreateTime,  # 动态参数
        
        "qualityInspectIqcDetToCreateTime": qualityInspectIqcDetToCreateTime,  # 动态参数
        
        "key": "QUALITY_INSPECT_IQC_DET",
        "from": qualityInspectIqcDetFromCreateTime,
        "to": qualityInspectIqcDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "alityInspectIqcDetQualityInspectIqcPlannedTimeRequired": {"name": "IQC明细计划需时"},  # 字段映射
        
        "ityInspectIqcDetQualityInspectIqcPlannedOutputQuantity": {"name": "IQC明细计划产出数量"},  # 字段映射
        
        "qualityInspectIqcDetAcceptQty": {"name": "IQC明细接受数量"},  # 字段映射
        
        "qualityInspectIqcDetActualTimeRequired": {"name": "IQC明细实际需时"},  # 字段映射
        
        "qualityInspectIqcDetAdjustmentTimeRequired": {"name": "IQC明细调整需时"},  # 字段映射
        
        "qualityInspectIqcDetBriefName": {"name": "IQC明细简称"},  # 字段映射
        
        "qualityInspectIqcDetCheckQuantity": {"name": "IQC明细检验数量"},  # 字段映射
        
        "qualityInspectIqcDetClosedReason": {"name": "IQC明细结案原因"},  # 字段映射
        
        "qualityInspectIqcDetDefectTotalQty": {"name": "IQC明细缺陷总数"},  # 字段映射
        
        "qualityInspectIqcDetDeliveryDate": {"name": "IQC明细交货日期"},  # 字段映射
        
        "qualityInspectIqcDetEndTime": {"name": "IQC明细结束时间"},  # 字段映射
        
        "qualityInspectIqcDetId": {"name": "IQC明细PK"},  # 字段映射
        
        "qualityInspectIqcDetQualityInspectIqcBriefName": {"name": "IQC明细简称"},  # 字段映射
        
        "qualityInspectIqcDetQualityInspectIqcCompleteQuantity": {"name": "IQC明细完成数量"},  # 字段映射
        
        "qualityInspectIqcDetQualityInspectIqcCompleteStatus": {"name": "IQC明细完成状态"},  # 字段映射
        
        "qualityInspectIqcDetQuantity": {"name": "IQC明细任务数量"},  # 字段映射
        
        "qualityInspectIqcDetResults": {"name": "IQC明细质检检验结果"},  # 字段映射
        
        "qualityInspectIqcDetSupervisorEmployee": {"name": "IQC明细主管员工"},  # 字段映射
        
        "qualityInspectIqcDetUnqualifiedQuantity": {"name": "IQC明细不合格数量"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "IQC明细计划需时": "IQC明细计划需时(小时)",  # 字段含义
        
        "IQC明细计划产出数量": "IQC明细计划产出数量",  # 字段含义
        
        "IQC明细接受数量": "IQC明细接受数量",  # 字段含义
        
        "IQC明细实际需时": "IQC明细实际需时(小时)",  # 字段含义
        
        "IQC明细调整需时": "IQC明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "IQC明细简称": "IQC明细简称",  # 字段含义
        
        "IQC明细检验数量": "IQC明细检验数量",  # 字段含义
        
        "IQC明细结案原因": "IQC明细结案原因",  # 字段含义
        
        "IQC明细缺陷总数": "IQC明细缺陷总数",  # 字段含义
        
        "IQC明细交货日期": "IQC明细交货日期",  # 字段含义
        
        "IQC明细结束时间": "IQC明细结束时间",  # 字段含义
        
        "IQC明细PK": "IQC明细PK",  # 字段含义
        
        "IQC明细简称": "IQC明细简称",  # 字段含义
        
        "IQC明细完成数量": "IQC明细完成数量",  # 字段含义
        
        "IQC明细完成状态": "IQC明细完成状态",  # 字段含义
        
        "IQC明细任务数量": "IQC明细任务数量",  # 字段含义
        
        "IQC明细质检检验结果": "IQC明细质检检验结果(1合格，2不合格)",  # 字段含义
        
        "IQC明细主管员工": "IQC明细主管员工",  # 字段含义
        
        "IQC明细不合格数量": "IQC明细不合格数量"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("IQC明细", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@quality_mcp.tool()  # 注册工具
def QUALITY_INSPECT_IPQC_DET(access_token: str,qualityInspectIpqcDetFromCreateTime:str=None,qualityInspectIpqcDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    IPQC明细，工序首检业务查询
    
    Args:
        access_token: 访问令牌
        
        qualityInspectIpqcDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        qualityInspectIpqcDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "QUALITY_INSPECT_IPQC_DET"
    # 构建请求URL
    url = "/quality-inspect-ipqc-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "qualityInspectIpqcDetQualityInspectIpqcClazz": "QUALITY_INSPECT_IPQC",  # 固定参数
        
        "qualityInspectIpqcDetClazz": "QUALITY_INSPECT_IPQC_DET",  # 固定参数
        
        
        "qualityInspectIpqcDetFromCreateTime": qualityInspectIpqcDetFromCreateTime,  # 动态参数
        
        "qualityInspectIpqcDetToCreateTime": qualityInspectIpqcDetToCreateTime,  # 动态参数
        
        "key": "QUALITY_INSPECT_IPQC_DET",
        "from": qualityInspectIpqcDetFromCreateTime,
        "to": qualityInspectIpqcDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "YInspectIpqcDetQualityInspectIpqcPlannedOutputQuantity": {"name": "IPQC明细计划产出数量"},  # 字段映射
        
        "alityInspectIpqcDetQualityInspectIpqcProductionShiftId": {"name": "IPQC明细生产班次ID"},  # 字段映射
        
        "inspectIpqcDetQualityInspectIpqcAdjustmentTimeRequired": {"name": "IPQC明细调整需时"},  # 字段映射
        
        "qualityInspectIpqcDetAcceptQty": {"name": "IPQC明细接受数量"},  # 字段映射
        
        "qualityInspectIpqcDetActualTimeRequired": {"name": "IPQC明细实际需时"},  # 字段映射
        
        "qualityInspectIpqcDetAdjustmentTimeRequired": {"name": "IPQC明细调整需时"},  # 字段映射
        
        "qualityInspectIpqcDetAqlLevelId": {"name": "IPQC明细AQL检查等级id"},  # 字段映射
        
        "qualityInspectIpqcDetBasis": {"name": "IPQC明细质检依据"},  # 字段映射
        
        "qualityInspectIpqcDetBriefName": {"name": "IPQC明细简称"},  # 字段映射
        
        "qualityInspectIpqcDetCheckQuantity": {"name": "IPQC明细检验数量"},  # 字段映射
        
        "qualityInspectIpqcDetClosedStatus": {"name": "IPQC明细结案状态"},  # 字段映射
        
        "qualityInspectIpqcDetCompleteQuantity": {"name": "IPQC明细完成数量"},  # 字段映射
        
        "qualityInspectIpqcDetCompleteStatus": {"name": "IPQC明细完成状态"},  # 字段映射
        
        "qualityInspectIpqcDetDefectTotalQty": {"name": "IPQC明细缺陷总数"},  # 字段映射
        
        "qualityInspectIpqcDetDutyDept": {"name": "IPQC明细责任部门"},  # 字段映射
        
        "qualityInspectIpqcDetDutyUser": {"name": "IPQC明细责任人"},  # 字段映射
        
        "qualityInspectIpqcDetEndTime": {"name": "IPQC明细结束时间"},  # 字段映射
        
        "qualityInspectIpqcDetId": {"name": "IPQC明细PK"},  # 字段映射
        
        "qualityInspectIpqcDetQualityInspectIpqcCompleteQuantity": {"name": "IPQC明细完成数量"},  # 字段映射
        
        "qualityInspectIpqcDetQualityInspectIpqcDeliveryDate": {"name": "IPQC明细交货日期"},  # 字段映射
        
        "qualityInspectIpqcDetQualityInspectIpqcPlannedOutputQuantity": {"name": "IPQC明细计划产出数量"},  # 字段映射
        
        "qualityInspectIpqcDetQualityInspectIpqcQuantity": {"name": "IPQC明细任务数量"},  # 字段映射
        
        "qualityInspectIpqcDetQualityInspectIpqcReceiptDate": {"name": "IPQC明细单据日期"},  # 字段映射
        
        "qualityInspectIpqcDetQuantity": {"name": "IPQC明细任务数量"},  # 字段映射
        
        "qualityInspectIpqcDetReceiptDate": {"name": "IPQC明细单据日期"},  # 字段映射
        
        "qualityInspectIpqcDetReceiptType": {"name": "IPQC明细单据类型"},  # 字段映射
        
        "qualityInspectIpqcDetResults": {"name": "IPQC明细质检检验结果"},  # 字段映射
        
        "qualityInspectIpqcDetState": {"name": "IPQC明细通用状态"},  # 字段映射
        
        "qualityInspectIpqcDetSupervisorEmployee": {"name": "IPQC明细主管员工"},  # 字段映射
        
        "qualityInspectIpqcDetThirdPartyName": {"name": "IPQC明细第三方名称"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "IPQC明细计划产出数量": "IPQC明细计划产出数量",  # 字段含义
        
        "IPQC明细生产班次ID": "IPQC明细生产班次ID",  # 字段含义
        
        "IPQC明细调整需时": "IPQC明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "IPQC明细接受数量": "IPQC明细接受数量",  # 字段含义
        
        "IPQC明细实际需时": "IPQC明细实际需时(小时)",  # 字段含义
        
        "IPQC明细调整需时": "IPQC明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "IPQC明细AQL检查等级id": "IPQC明细AQL检查等级id",  # 字段含义
        
        "IPQC明细质检依据": "IPQC明细质检依据",  # 字段含义
        
        "IPQC明细简称": "IPQC明细简称",  # 字段含义
        
        "IPQC明细检验数量": "IPQC明细检验数量",  # 字段含义
        
        "IPQC明细结案状态": "IPQC明细结案状态",  # 字段含义
        
        "IPQC明细完成数量": "IPQC明细完成数量",  # 字段含义
        
        "IPQC明细完成状态": "IPQC明细完成状态",  # 字段含义
        
        "IPQC明细缺陷总数": "IPQC明细缺陷总数",  # 字段含义
        
        "IPQC明细责任部门": "IPQC明细责任部门",  # 字段含义
        
        "IPQC明细责任人": "IPQC明细责任人",  # 字段含义
        
        "IPQC明细结束时间": "IPQC明细结束时间",  # 字段含义
        
        "IPQC明细PK": "IPQC明细PK",  # 字段含义
        
        "IPQC明细完成数量": "IPQC明细完成数量",  # 字段含义
        
        "IPQC明细交货日期": "IPQC明细交货日期",  # 字段含义
        
        "IPQC明细计划产出数量": "IPQC明细计划产出数量",  # 字段含义
        
        "IPQC明细任务数量": "IPQC明细任务数量",  # 字段含义
        
        "IPQC明细单据日期": "IPQC明细单据日期",  # 字段含义
        
        "IPQC明细任务数量": "IPQC明细任务数量",  # 字段含义
        
        "IPQC明细单据日期": "IPQC明细单据日期",  # 字段含义
        
        "IPQC明细单据类型": "IPQC明细单据类型（一个常量值，与node里的defaultTypeId不一样，推荐使用字典）",  # 字段含义
        
        "IPQC明细质检检验结果": "IPQC明细质检检验结果(1合格，2不合格)",  # 字段含义
        
        "IPQC明细通用状态": "IPQC明细通用状态",  # 字段含义
        
        "IPQC明细主管员工": "IPQC明细主管员工",  # 字段含义
        
        "IPQC明细第三方名称": "IPQC明细第三方名称"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("IPQC明细", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@quality_mcp.tool()  # 注册工具
def QUALITY_INSPECT_OQC_DET(access_token: str,qualityInspectOqcDetFromCreateTime:str=None,qualityInspectOqcDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    OQC明细，巡检业务查询
    
    Args:
        access_token: 访问令牌
        
        qualityInspectOqcDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        qualityInspectOqcDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "QUALITY_INSPECT_OQC_DET"
    # 构建请求URL
    url = "/quality-inspect-oqc-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "qualityInspectOqcDetQualityInspectOqcClazz": "QUALITY_INSPECT_OQC",  # 固定参数
        
        "qualityInspectOqcDetClazz": "QUALITY_INSPECT_OQC_DET",  # 固定参数
        
        
        "qualityInspectOqcDetFromCreateTime": qualityInspectOqcDetFromCreateTime,  # 动态参数
        
        "qualityInspectOqcDetToCreateTime": qualityInspectOqcDetToCreateTime,  # 动态参数
        
        "key": "QUALITY_INSPECT_OQC_DET",
        "from": qualityInspectOqcDetFromCreateTime,
        "to": qualityInspectOqcDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "alityInspectOqcDetQualityInspectOqcPlannedTimeRequired": {"name": "OQC明细计划需时"},  # 字段映射
        
        "ityInspectOqcDetQualityInspectOqcPlannedOutputQuantity": {"name": "OQC明细计划产出数量"},  # 字段映射
        
        "qualityInspectOqcDetAdjustmentTimeRequired": {"name": "OQC明细调整需时"},  # 字段映射
        
        "qualityInspectOqcDetAqlLevelId": {"name": "OQC明细AQL检查等级id"},  # 字段映射
        
        "qualityInspectOqcDetAuditStatus": {"name": "OQC明细审核状态"},  # 字段映射
        
        "qualityInspectOqcDetBasis": {"name": "OQC明细质检依据"},  # 字段映射
        
        "qualityInspectOqcDetBeginTime": {"name": "OQC明细开始时间"},  # 字段映射
        
        "qualityInspectOqcDetBriefName": {"name": "OQC明细简称"},  # 字段映射
        
        "qualityInspectOqcDetCheckQuantity": {"name": "OQC明细检验数量"},  # 字段映射
        
        "qualityInspectOqcDetCheckStanId": {"name": "OQC明细质量检验标准id"},  # 字段映射
        
        "qualityInspectOqcDetClazz": {"name": "OQC明细子类"},  # 字段映射
        
        "qualityInspectOqcDetClosedReason": {"name": "OQC明细结案原因"},  # 字段映射
        
        "qualityInspectOqcDetClosedStatus": {"name": "OQC明细结案状态"},  # 字段映射
        
        "qualityInspectOqcDetDefectTotalQty": {"name": "OQC明细缺陷总数"},  # 字段映射
        
        "qualityInspectOqcDetDeliveryDate": {"name": "OQC明细交货日期"},  # 字段映射
        
        "qualityInspectOqcDetDutyDept": {"name": "OQC明细责任部门"},  # 字段映射
        
        "qualityInspectOqcDetDutyUser": {"name": "OQC明细责任人"},  # 字段映射
        
        "qualityInspectOqcDetEndTime": {"name": "OQC明细结束时间"},  # 字段映射
        
        "qualityInspectOqcDetGenerativeState": {"name": "OQC明细下发状态"},  # 字段映射
        
        "qualityInspectOqcDetId": {"name": "OQC明细PK"},  # 字段映射
        
        "qualityInspectOqcDetPlannedOutputQuantity": {"name": "OQC明细计划产出数量"},  # 字段映射
        
        "qualityInspectOqcDetQualityInspectOqcAuditStatus": {"name": "OQC明细审核状态"},  # 字段映射
        
        "qualityInspectOqcDetQualityInspectOqcClosedReason": {"name": "OQC明细结案原因"},  # 字段映射
        
        "qualityInspectOqcDetQualityInspectOqcCompleteQuantity": {"name": "OQC明细完成数量"},  # 字段映射
        
        "qualityInspectOqcDetQualityInspectOqcEndTimeRequired": {"name": "OQC明细最后需时"},  # 字段映射
        
        "qualityInspectOqcDetQualityInspectOqcExchangeRateId": {"name": "OQC明细币种汇率id"},  # 字段映射
        
        "qualityInspectOqcDetQualityInspectOqcPlannedOutputQuantity": {"name": "OQC明细计划产出数量"},  # 字段映射
        
        "qualityInspectOqcDetQualityInspectOqcQuantity": {"name": "OQC明细任务数量"},  # 字段映射
        
        "qualityInspectOqcDetResults": {"name": "OQC明细质检检验结果"},  # 字段映射
        
        "qualityInspectOqcDetSupervisorEmployee": {"name": "OQC明细主管员工"},  # 字段映射
        
        "qualityInspectOqcDetTarget": {"name": "OQC明细目标"},  # 字段映射
        
        "qualityInspectOqcDetUnitId": {"name": "OQC明细物料质检单位id"},  # 字段映射
        
        "qualityInspectOqcDetUnqualifiedQuantity": {"name": "OQC明细不合格数量"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "OQC明细计划需时": "OQC明细计划需时(小时)",  # 字段含义
        
        "OQC明细计划产出数量": "OQC明细计划产出数量",  # 字段含义
        
        "OQC明细调整需时": "OQC明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "OQC明细AQL检查等级id": "OQC明细AQL检查等级id",  # 字段含义
        
        "OQC明细审核状态": "OQC明细审核状态",  # 字段含义
        
        "OQC明细质检依据": "OQC明细质检依据",  # 字段含义
        
        "OQC明细开始时间": "OQC明细开始时间",  # 字段含义
        
        "OQC明细简称": "OQC明细简称",  # 字段含义
        
        "OQC明细检验数量": "OQC明细检验数量",  # 字段含义
        
        "OQC明细质量检验标准id": "OQC明细质量检验标准id",  # 字段含义
        
        "OQC明细子类": "OQC明细子类 类名（表和类一一对应）",  # 字段含义
        
        "OQC明细结案原因": "OQC明细结案原因",  # 字段含义
        
        "OQC明细结案状态": "OQC明细结案状态",  # 字段含义
        
        "OQC明细缺陷总数": "OQC明细缺陷总数",  # 字段含义
        
        "OQC明细交货日期": "OQC明细交货日期",  # 字段含义
        
        "OQC明细责任部门": "OQC明细责任部门",  # 字段含义
        
        "OQC明细责任人": "OQC明细责任人",  # 字段含义
        
        "OQC明细结束时间": "OQC明细结束时间",  # 字段含义
        
        "OQC明细下发状态": "OQC明细下发状态",  # 字段含义
        
        "OQC明细PK": "OQC明细PK",  # 字段含义
        
        "OQC明细计划产出数量": "OQC明细计划产出数量",  # 字段含义
        
        "OQC明细审核状态": "OQC明细审核状态",  # 字段含义
        
        "OQC明细结案原因": "OQC明细结案原因",  # 字段含义
        
        "OQC明细完成数量": "OQC明细完成数量",  # 字段含义
        
        "OQC明细最后需时": "OQC明细最后需时(小时)",  # 字段含义
        
        "OQC明细币种汇率id": "OQC明细币种汇率id",  # 字段含义
        
        "OQC明细计划产出数量": "OQC明细计划产出数量",  # 字段含义
        
        "OQC明细任务数量": "OQC明细任务数量",  # 字段含义
        
        "OQC明细质检检验结果": "OQC明细质检检验结果(1合格，2不合格)",  # 字段含义
        
        "OQC明细主管员工": "OQC明细主管员工",  # 字段含义
        
        "OQC明细目标": "OQC明细目标",  # 字段含义
        
        "OQC明细物料质检单位id": "OQC明细物料质检单位id",  # 字段含义
        
        "OQC明细不合格数量": "OQC明细不合格数量"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("OQC明细", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  

@quality_mcp.tool()  # 注册工具
def QUALITY_INSPECT_FQC_DET(access_token: str,qualityInspectFqcDetFromCreateTime:str=None,qualityInspectFqcDetToCreateTime:str=None) -> str:  # 定义工具函数
    """
    FQC明细，成品入库检业务查询
    
    Args:
        access_token: 访问令牌
        
        qualityInspectFqcDetFromCreateTime: 开始时间，格式为YYYY-%m-DD %H:%M:%S
        
        qualityInspectFqcDetToCreateTime: 结束时间，格式为YYYY-%m-DD %H:%M:%S
             
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    """
    # 当前方法名
    function_name = "QUALITY_INSPECT_FQC_DET"
    # 构建请求URL
    url = "/quality-inspect-fqc-det/findList"  # API地址
    # 构建请求体数据
    data = {
        
        "qualityInspectFqcDetQualityInspectFqcClazz": "QUALITY_INSPECT_FQC",  # 固定参数
        
        "qualityInspectFqcDetClazz": "QUALITY_INSPECT_FQC_DET",  # 固定参数
        
        
        "qualityInspectFqcDetFromCreateTime": qualityInspectFqcDetFromCreateTime,  # 动态参数
        
        "qualityInspectFqcDetToCreateTime": qualityInspectFqcDetToCreateTime,  # 动态参数
        
        "key": "QUALITY_INSPECT_FQC_DET",
        "from": qualityInspectFqcDetFromCreateTime,
        "to": qualityInspectFqcDetToCreateTime,
        
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        
        "alityInspectFqcDetQualityInspectFqcPlannedTimeRequired": {"name": "FQC明细计划需时"},  # 字段映射
        
        "ityInspectFqcDetQualityInspectFqcPlannedOutputQuantity": {"name": "FQC明细计划产出数量"},  # 字段映射
        
        "qualityInspectFqcDetAcceptQty": {"name": "FQC明细接受数量"},  # 字段映射
        
        "qualityInspectFqcDetAdjustmentTimeRequired": {"name": "FQC明细调整需时"},  # 字段映射
        
        "qualityInspectFqcDetAuditStatus": {"name": "FQC明细审核状态"},  # 字段映射
        
        "qualityInspectFqcDetBasis": {"name": "FQC明细质检依据"},  # 字段映射
        
        "qualityInspectFqcDetCheckQuantity": {"name": "FQC明细检验数量"},  # 字段映射
        
        "qualityInspectFqcDetClosedReason": {"name": "FQC明细结案原因"},  # 字段映射
        
        "qualityInspectFqcDetCompleteQuantity": {"name": "FQC明细完成数量"},  # 字段映射
        
        "qualityInspectFqcDetCompleteStatus": {"name": "FQC明细完成状态"},  # 字段映射
        
        "qualityInspectFqcDetDefectTotalQty": {"name": "FQC明细缺陷总数"},  # 字段映射
        
        "qualityInspectFqcDetDeliveryDate": {"name": "FQC明细交货日期"},  # 字段映射
        
        "qualityInspectFqcDetDutyDept": {"name": "FQC明细责任部门"},  # 字段映射
        
        "qualityInspectFqcDetDutyUser": {"name": "FQC明细责任人"},  # 字段映射
        
        "qualityInspectFqcDetId": {"name": "FQC明细PK"},  # 字段映射
        
        "qualityInspectFqcDetInUsed": {"name": "FQC明细是否被使用"},  # 字段映射
        
        "qualityInspectFqcDetIsManualModificationDate": {"name": "FQC明细是否手动修改计划生产时间"},  # 字段映射
        
        "qualityInspectFqcDetIsolation": {"name": "FQC明细智能节点数据隔离标识"},  # 字段映射
        
        "qualityInspectFqcDetPlannedOutputQuantity": {"name": "FQC明细计划产出数量"},  # 字段映射
        
        "qualityInspectFqcDetPlannedTimeRequired": {"name": "FQC明细计划需时"},  # 字段映射
        
        "qualityInspectFqcDetQualifiedQuantity": {"name": "FQC明细合格数量"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcActualTimeRequired": {"name": "FQC明细实际需时"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcAdjustmentTimeRequired": {"name": "FQC明细调整需时"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcBriefName": {"name": "FQC明细简称"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcClosedReason": {"name": "FQC明细结案原因"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcCompleteStatus": {"name": "FQC明细完成状态"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcDeliveryDate": {"name": "FQC明细交货日期"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcEndTime": {"name": "FQC明细结束时间"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcExtension": {"name": "FQC明细扩展数据"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcPlannedOutputQuantity": {"name": "FQC明细计划产出数量"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcPlannedTimeRequired": {"name": "FQC明细计划需时"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcQuantity": {"name": "FQC明细任务数量"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcReceiptDate": {"name": "FQC明细单据日期"},  # 字段映射
        
        "qualityInspectFqcDetQualityInspectFqcReceiptType": {"name": "FQC明细单据类型"},  # 字段映射
        
        "qualityInspectFqcDetResults": {"name": "FQC明细质检检验结果"},  # 字段映射
        
        "qualityInspectFqcDetSupervisorEmployee": {"name": "FQC明细主管员工"},  # 字段映射
        
        "qualityInspectFqcDetUnqualifiedQuantity": {"name": "FQC明细不合格数量"}  # 字段映射
        
    }  # 过滤字段字典结束
    meaning_list = {
        
        "FQC明细计划需时": "FQC明细计划需时(小时)",  # 字段含义
        
        "FQC明细计划产出数量": "FQC明细计划产出数量",  # 字段含义
        
        "FQC明细接受数量": "FQC明细接受数量",  # 字段含义
        
        "FQC明细调整需时": "FQC明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "FQC明细审核状态": "FQC明细审核状态",  # 字段含义
        
        "FQC明细质检依据": "FQC明细质检依据",  # 字段含义
        
        "FQC明细检验数量": "FQC明细检验数量",  # 字段含义
        
        "FQC明细结案原因": "FQC明细结案原因",  # 字段含义
        
        "FQC明细完成数量": "FQC明细完成数量",  # 字段含义
        
        "FQC明细完成状态": "FQC明细完成状态",  # 字段含义
        
        "FQC明细缺陷总数": "FQC明细缺陷总数",  # 字段含义
        
        "FQC明细交货日期": "FQC明细交货日期",  # 字段含义
        
        "FQC明细责任部门": "FQC明细责任部门",  # 字段含义
        
        "FQC明细责任人": "FQC明细责任人",  # 字段含义
        
        "FQC明细PK": "FQC明细PK",  # 字段含义
        
        "FQC明细是否被使用": "FQC明细是否被使用",  # 字段含义
        
        "FQC明细是否手动修改计划生产时间": "FQC明细是否手动修改计划生产时间",  # 字段含义
        
        "FQC明细智能节点数据隔离标识": "FQC明细智能节点数据隔离标识",  # 字段含义
        
        "FQC明细计划产出数量": "FQC明细计划产出数量",  # 字段含义
        
        "FQC明细计划需时": "FQC明细计划需时(小时)",  # 字段含义
        
        "FQC明细合格数量": "FQC明细合格数量",  # 字段含义
        
        "FQC明细实际需时": "FQC明细实际需时(小时)",  # 字段含义
        
        "FQC明细调整需时": "FQC明细调整需时(输入正负数来计算实际需时)(小时)",  # 字段含义
        
        "FQC明细简称": "FQC明细简称",  # 字段含义
        
        "FQC明细结案原因": "FQC明细结案原因",  # 字段含义
        
        "FQC明细完成状态": "FQC明细完成状态",  # 字段含义
        
        "FQC明细交货日期": "FQC明细交货日期",  # 字段含义
        
        "FQC明细结束时间": "FQC明细结束时间",  # 字段含义
        
        "FQC明细扩展数据": "FQC明细扩展数据",  # 字段含义
        
        "FQC明细计划产出数量": "FQC明细计划产出数量",  # 字段含义
        
        "FQC明细计划需时": "FQC明细计划需时(小时)",  # 字段含义
        
        "FQC明细任务数量": "FQC明细任务数量",  # 字段含义
        
        "FQC明细单据日期": "FQC明细单据日期",  # 字段含义
        
        "FQC明细单据类型": "FQC明细单据类型（一个常量值，与node里的defaultTypeId不一样，推荐使用字典）",  # 字段含义
        
        "FQC明细质检检验结果": "FQC明细质检检验结果(1合格，2不合格)",  # 字段含义
        
        "FQC明细主管员工": "FQC明细主管员工",  # 字段含义
        
        "FQC明细不合格数量": "FQC明细不合格数量"  # 字段含义
        
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("FQC明细", function_name, data, access_token, filtered_fields, meaning_list)  # 返回数据  
