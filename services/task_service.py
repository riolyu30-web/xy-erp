from fastmcp import FastMCP  # 导入FastMCP框架
from dotenv import load_dotenv  # 导入环境变量加载器
import os  # 导入操作系统模块
import requests  # 导入HTTP请求库
from services.tool import json_to_csv, get_csv_header, clear_data, get_ids, append_data  # 导入JSON转换CSV函数
from services.cache import cache_save

# 加载环境变量
load_dotenv()  # 加载.env文件中的环境变量

# 从环境变量获取配置
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")  # 获取基础URL

task_mcp = FastMCP(name="task")  # 创建任务服务MCP实例


@task_mcp.tool()
def find_schedule(access_token: str, plan_type: str = "瓦楞",
                  start_date: str = "", end_date: str = ""):
    """
    获取任务排程表，主表，字段为排程单号,创建人,生产日期,下推状态,任务状态,客户简称,班组,工序名称,模出,工作中心名称,生产单号,产品名称,数量,完成数,交货日期,颜色描述,客户批次,调机小时,产品编码,门幅,入库数,总加工面积,客方货号,盒型编码,盒型名称,创建时间,纸 质,楞别,纸箱面积,计划开始时间,颜色数量,计划结束时间,订单规格,工作中心编码,印版编码,备注,刀模编码,首选机台,急单 排单编号,排度单号,创建人,生产日期,下发状态,任务状态,客户简称,班次,工序,模出,设备名称,纸箱生产单号,产品名称,数量,完成数,交期,颜色描述,客户批次,调机 小时,产品编码,门幅,入库数,总加工面积,客方货号,盒型编码,盒型名称,创建日期, 纸质,楞别,纸箱面积,计划开始时间,颜色数量,计划结束时间,订单规格,工作中心编 码,印版编码,备注,刀模编码,首选机台,急单类型,托数,加工状态,完成状态,客户po,纸板生产单号,裁切数,门幅,修改后门幅,工单产出数量,剖数,修改后剖数,纸板总面积,修边,生产线编码,长度(米),纸质全称,损耗率,利用率,展宽,净边,纸长,纸板面积,压线(一),压线(二),压线(三),压线(四),线上时间,产品编码,下发人,调整需时（小时）,用纸备注,订单编号,生产进度,用纸明细,压线类型,订单数,订单类型,批次号,部件名称,上工序计划完成时间
    Args:
        access_token: 访问令牌
        plan_type: 计划类型 瓦楞/纸箱，默认为"瓦楞"
        start_date: 创建开始时间，格式为2025-07-02
        end_date: 创建结束时间，格式为2025-07-04

    Returns:
        table_token: 任务排程表令牌
    """
    return find_schedule(access_token, plan_type, start_date, end_date)


def find_schedule(access_token: str, plan_type: str = "瓦楞",
                  start_date: str = "", end_date: str = ""):
    # 构建API URL
    url = f"{BASE_URL}/work/erp-production-plan/tasksToBeArrangedES"

    # 构建请求参数
    params = {
        # "uuid": "W3dvcqefxRAH4uDE",  # 固定UUID
        "access_token": access_token  # 访问令牌作为查询参数
    }

    # 构建请求体
    payload = {
        # 设备GUID转换为数组
        "startDate": start_date,  # 开始日期
        "endDate": end_date  # 结束日期
    }
    if plan_type == "瓦楞":
        payload["planType"] = 1
        payload["isCorrugation"] = "true"
    elif plan_type == "纸箱":
        payload["planType"] = 2
        payload["isCorrugation"] = "false"
    try:
        # 构建请求头
        headers = {  # 构建HTTP请求头
            "Authorization": f"bearer {access_token}",  # 设置Bearer认证头
            "Content-Type": "application/json"  # 设置内容类型
        }

        # 发送HTTP POST请求
        response = requests.post(
            url, params=params, json=payload, headers=headers, timeout=30)  # 发送POST请求并设置超时时间和请求头
        response.raise_for_status()  # 检查HTTP响应状态

        # 解析响应数据
        response_data = response.json()  # 解析JSON响应
        # print(response_data)

        # 检查业务逻辑是否成功
        if response_data.get("code") == 0 and response_data.get("msg") == "SUCCESS":
            # 检查是否有数据
            if response_data and 'data' in response_data:
                data_dict = response_data['data']  # 获取数据字典

                # 将所有排单编号的数据合并为一个列表
                all_records = []  # 初始化记录列表
                for schedule_number, records in data_dict.items():  # 遍历每个排单编号
                    if isinstance(records, list):  # 确保是列表类型
                        for record in records:  # 遍历每条记录
                            # 添加排单编号字段
                            record['scheduleNumber'] = schedule_number
                            all_records.append(record)  # 添加到总记录列表

                if all_records:  # 如果有记录
                    # 定义列名映射（根据实际返回数据结构调整）
                    column_mapping = {
                        "scheduleNumber": "排单编号",
                        "planNumber": "排度单号",
                        "creator": "创建人",
                        "frontPlanDate": "生产日期",
                        "generativeStateName": "下发状态",
                        "tasksStateName": "任务状态",
                        "customerName": "客户简称",
                        "teamName": "班次",
                        "productionProcessesTypeName": "工序",
                        "modulus": "模出",
                        "equipmentName": "设备名称",
                        "workorderNumber": "纸箱生产单号",
                        "productName": "产品名称",
                        "plannedQuantity": "数量",
                        "checkQuantity": "完成数",
                        "requiredDeliveryTime": "交期",
                        "colorDescription": "颜色描述",
                        "customerBatchNumber": "客户批次",
                        "调机小时": "调机小时",
                        "productionProcessVO.productCode": "产品编码",
                        "materialWidth": "门幅",
                        "outInventoryQuantity": "入库数",
                        "totalCartonArea": "总加工面积",
                        "externalMaterialCode": "客方货号",
                        "searchCode": "盒型编码",
                        "materialClassificationName": "盒型名称",
                        "createDate": "创建日期",
                        "basicPaper": "纸质",
                        "corrugatedPaperUsageName": "楞别",
                        "cartonArea": "纸箱面积",
                        "plannedStartTime": "计划开始时间",
                        "colorNumber": "颜色数量",
                        "plannedEndTime": "计划结束时间",
                        "specification": "订单规格",
                        "equipmentCode": "工作中心编码",
                        "printCode": "印版编码",
                        "description": "备注",
                        "dieCuttingCode": "刀模编码",
                        "equipmentModelName": "首选机台",
                        "isUrgent": "急单类型",
                        "productionProcessVO.trayLoadCount": "托数",
                        "operationTypeName": "加工状态",
                        "tasksStateGuid": "完成状态",
                        "externalTrackingNumber": "客户po",
                        "extendNumber": "纸板生产单号",
                        "processQuantity": "裁切数",
                        "useWidth2": "门幅",
                        "widthOfFabric": "修改后门幅",
                        "outputQuantity": "工单产出数量",
                        "aperture": "剖数",
                        "proportion": "修改后剖数",
                        "totalArea": "纸板总面积",
                        "deburring": "修边",
                        "brand": "生产线编码",
                        "length": "长度(米)",
                        "fullPaperName": "纸质全称",
                        "attritionRate": "损耗率",
                        "utilizationRate": "利用率",
                        "openWidth": "展宽",
                        "cleanEdge": "净边",
                        "openLength": "纸长",
                        "boardArea": "纸板面积",
                        "line1": "压线(一)",
                        "line2": "压线(二)",
                        "line3": "压线(三)",
                        "line4": "压线(四)",
                        "plannedTimeRequired": "线上时间",
                        "productCode": "产品编码",
                        "generativePeople": "下发人",
                        "adjustmentTimeRequired": "调整需时（小时）",
                        "userPaperCode": "用纸备注",
                        "orderNumber": "订单编号",
                        "生产进度": "生产进度",
                        "userPaperName": "用纸明细",
                        "lineType": "压线类型",
                        "orderQuantity": "订单数",
                        "orderType": "订单类型",
                        "externalMaterialBarCode": "批次号",
                        "componentName": "部件名称",
                        "previousProcessPlannedEndTime": "上工序计划完成时间"
                    }

                    # 将数据转换为CSV格式
                    csv_str = json_to_csv(all_records, column_mapping)

                    # 保存到缓存
                    if csv_str:
                        key = f"任务表_{access_token}"
                        cache_save(key, csv_str)  # 保存CSV数据到缓存
                        #header = get_csv_header(csv_str)  # 获取列名列表
                        return key  # 返回列名列表
                    return "没有数据"  # 转换失败返回提示信息
                else:
                    return "没有数据"  # 没有记录返回提示信息
            else:
                return "没有数据"  # 没有数据返回提示信息
        else:
            error_msg = response_data.get("msg", "未知错误")  # 获取错误信息
            return error_msg  # 返回错误信息

    except requests.exceptions.RequestException as e:  # 捕获请求异常
        print(f"HTTP请求失败: {str(e)}")  # 打印错误信息
        return f"请求失败: {str(e)}"  # 返回错误信息
    except Exception as e:  # 捕获其他异常
        print(f"处理失败: {str(e)}")  # 打印错误信息
        return f"处理失败: {str(e)}"  # 返回错误信息


@task_mcp.tool()
def get_progress(access_token: str, start_time: str = "", end_time: str = "",
                 product_name: str = "", customer_short_name: str = ""):
    """
    获取任务进度表，保存CSV格式字符串到缓存
    数据列：工单号,工单日期,生产数量,订单号,客户编码,客户简称,客户全称,币种,产品编码,产品名称,订单数量,备品数量,交货日期,成品入库总数,成品销货总数
    Args:
        access_token: 访问令牌
        start_time: 开始时间，格式为YYYY-MM-DD HH:MM:SS
        end_time: 结束时间，格式为YYYY-MM-DD HH:MM:SS
        product_name: 产品名称
        customer_short_name: 用户简称

    Returns:
        table_token: 任务进度表令牌
    """
    return find_progress(access_token, start_time, end_time, product_name, customer_short_name)


def find_progress(access_token: str, start_time: str = "", end_time: str = "",
                  product_name: str = "", customer_short_name: str = ""):
  # 调用接口1获取数据
    interface1_data = call_interface1(
        access_token, product_name, start_time, end_time, customer_short_name)

    work_order_ids = get_ids(
        interface1_data, 'workOrderId')  # 提取workOrderId字段值

    # 从接口1数据中提取customerIds
    customer_ids = get_ids(
        interface1_data, 'bizOrderDetailBizOrderCustId')  # 提取客户ID字段值

    # 调用接口6获取客户信息数据
    interface6_data = call_interface6(
        access_token, customer_ids) if customer_ids else []  # 调用接口6

    if interface6_data:  # 如果接口6有返回数据
        # 将接口6的客户信息数据按bizOrderDetailBizOrderCustId绑定到接口1数据中
        interface1_data = append_data(
            interface1_data, interface6_data, 'bizOrderDetailBizOrderCustId', 'customerId')

    # 从接口1数据中提取bizOrderDetailBizOrderId字段值
    biz_order_detail_ids = get_ids(
        interface1_data, 'bizOrderDetailBizOrderId')  # 提取业务订单详情ID

    # 调用接口4获取销售出库数据
    if biz_order_detail_ids:  # 如果有业务订单详情ID
        interface4_data = call_interface4(
            access_token, biz_order_detail_ids)  # 调用接口4
        # 将接口4的销售出库数据按bizOrderDetailBizOrderId绑定到接口1数据中
        interface1_data = append_data(
            interface1_data, interface4_data, 'bizOrderDetailBizOrderId', 'bizOrderDetailBizOrderId')

    # 调用接口2获取生产详情数据
    interface2_data = call_interface2(
        access_token, work_order_ids)  # 调用接口2

    if interface2_data:  # 如果接口2有返回数据
        # 将接口2的生产详情数据按workOrderId绑定到接口1数据中
        interface1_data = append_data(
            interface1_data, interface2_data, 'workOrderId', 'workOrderId')

    mapping = {
        # "workOrderAuditStatusDictName": "审核状态",
        "workOrderAuditDate": "审核日期",
        "workOrderReceiptTypeDictName": "工单类型",
        "workOrderUserCode": "工单号",
        "workOrderReceiptDate": "工单日期",
        "bomNodeTotalQuantity": "生产数量",
        "结案状态": "结案状态",
        "bizOrderDetailBizOrderUserCode": "订单号",
        "merchanName": "业务员",
        "salesmanName": "跟单员",
        "fontCustomerClassificationName": "客户分类",
        "customerUserCode": "客户编码",
        "customerShortName": "客户简称",
        "customerName": "客户全称",
        "customerCurrencyId": "币种",
        "frontBoxClassName": "产品分类",
        "matUserCode": "产品编码",
        "matName": "产品名称",
        "frontSpecName": "规格类型",
        "bizOrderDetailQuantity": "订单数量",
        "bizOrderDetailGiftQty": "赠送数量",
        "bizOrderDetailSpareQty": "备品数量",
        "frontTotalQuantity": "订单总数",
        "bizOrderDetailDeliveryDate": "交货日期",
        "客户PO": "客户PO",
        "客户料号": "客户料号",
        "客户产品名称": "客户产品名称",
        "frontPurchaseOrderSituation": "采购订单情况(%)",
        "frontMaterialArrivalSituation": "物料到货情况(%)",
        "frontMaterialOutSituation": "物料出库情况(%)",
        "外发订单情况": "外发订单情况(%)",
        "外发到货情况": "外发到货情况(%)",
        "生产部件进度": "生产部件进度(%)",
        "工序进度": "工序进度(%)",
        "theoretical_cycle": "理论周期(分钟/件)",
    "performance_rate": "性能稼动率(%)",
    "giveaway_quantity": "交出量",
    "receive_quantity": "接收量",
        "prdIApyDetQuantity": "成品入库总数",
        "frontPrdIApySituation": "成品入库情况",
        "prdSalDetQuantity": "成品销货总数",
        "frontPrdSalSituation": "成品销货情况"
    }

    csv_str = json_to_csv(interface1_data, mapping)  # 转换为CSV格式

    if csv_str:  
        key = f"任务进度表_{access_token}"  # 如果转换成功
        cache_save(key, csv_str)  # 保存到缓存  
        #header = get_csv_header(csv_str)  # 获取CSV头部
        return key  # 返回列名清单
    return "没有数据"  # 没有数据时返回提示


def call_interface2(access_token: str, work_order_ids: list):
    """
    封装接口2：调用生产入库详情-成品入库-任务查询接口

    Args:
        access_token: 访问令牌
        work_order_ids: 工单ID列表，从接口1中提取的workOrderId字段值

    Returns:
        list: 接口返回的数据列表，失败时返回空列表
    """
    # 构建API URL
    url = f"{BASE_URL}/biz-order-detail/PrdIApyDet_FinInstorageDet_FinInwarehouseDetLeftOutputBomNode_MatRightBizOrderDetail_WorkOrder_TaskLeft/findList"

    # 构建请求参数
    params = {
        "access_token": access_token  # 访问令牌作为查询参数
    }

    # 构建请求体
    payload = {
        "bizOrderDetailClazz": "BUSINESS_ORDER_DETAIL",  # 业务订单详情分类
        "bizOrderDetailIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单详情隔离ID
        "bizOrderDetailTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单详情租户ID
        "bizOrderDetailBizOrderClazz": "BUSINESS_ORDER",  # 业务订单主表分类
        "bizOrderDetailBizOrderIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单主表隔离ID
        "bizOrderDetailBizOrderTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单主表租户ID
        "workOrderClazz": "WORK_ORDER",  # 工单分类
        "workOrderIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 工单隔离ID
        "workOrderTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 工单租户ID
        "matOutApyDetMatOutApyClazz": "MAT_OUT_APY",  # 物料出库申请分类
        "matOutApyDetMatOutApyIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 物料出库申请隔离ID
        "matOutApyDetMatOutApyTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 物料出库申请租户ID
        "matOutApyDetMatOutApyAuditStatus": "finish",  # 物料出库申请审核状态
        "matOutApyDetClazz": "MAT_OUT_APY_DET",  # 物料出库申请详情分类
        "matOutApyDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 物料出库申请详情隔离ID
        "matOutApyDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 物料出库申请详情租户ID
        "workOrderIds": work_order_ids  # 工单ID列表
    }

    # 构建请求头
    headers = {
        "Content-Type": "application/json",  # 内容类型
        "Accept": "application/json"  # 接受类型
    }

    try:
        # 发送POST请求
        response = requests.post(
            url, params=params, json=payload, headers=headers)
        response.raise_for_status()  # 检查HTTP错误

        # 解析响应数据
        result = response.json()

        if result.get('code') == 0:  # 请求成功
            return result.get('data', [])  # 返回数据列表
        else:
            print(f"接口2调用失败: {result.get('msg', '未知错误')}")  # 打印错误信息
            return []  # 返回空列表

    except requests.exceptions.RequestException as e:
        print(f"接口2请求异常: {str(e)}")  # 打印异常信息
        return []  # 返回空列表
    except Exception as e:
        print(f"接口2处理异常: {str(e)}")  # 打印处理异常
        return []  # 返回空列表


def call_interface6(access_token: str, customer_ids: list):
    """
    封装接口6：调用客户信息查询接口

    Args:
        access_token: 访问令牌
        customer_ids: 客户ID列表，从接口1中提取的bizOrderDetailBizOrderCustId字段值

    Returns:
        list: 接口返回的数据列表，失败时返回空列表
    """
    # 构建API URL
    url = f"{BASE_URL}/client/findList"

    # 构建请求参数
    params = {
        "access_token": access_token  # 访问令牌作为查询参数
    }

    # 构建请求体
    payload = {
        "customerIds": customer_ids,  # 客户ID列表
        "customerClazz": "CUSTOMER",  # 客户分类
        "customerIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 客户隔离ID
        "customerTenantId": "2caf3cb6216111eea71b49e0880a97d9"  # 客户租户ID
    }

    # 构建请求头
    headers = {
        "Content-Type": "application/json",  # 内容类型
        "Accept": "application/json"  # 接受类型
    }

    try:
        # 发送POST请求
        response = requests.post(
            url, params=params, json=payload, headers=headers)
        response.raise_for_status()  # 检查HTTP错误

        # 解析响应数据
        result = response.json()

        if result.get('code') == 0:  # 请求成功
            return result.get('data', [])  # 返回数据列表
        else:
            print(f"接口6调用失败: {result.get('msg', '未知错误')}")  # 打印错误信息
            return []  # 返回空列表

    except requests.exceptions.RequestException as e:
        print(f"接口6请求异常: {str(e)}")  # 打印异常信息
        return []  # 返回空列表
    except Exception as e:
        print(f"接口6处理异常: {str(e)}")  # 打印处理异常
        return []  # 返回空列表


def call_interface4(access_token: str, biz_order_detail_ids: list):
    """
    封装接口4：调用销售出库详情查询接口

    Args:
        access_token: 访问令牌
        biz_order_detail_ids: 业务订单详情ID列表，从接口1中提取的bizOrderDetailBizOrderId字段值

    Returns:
        list: 接口返回的数据列表，失败时返回空列表
    """
    # 构建API URL
    url = f"{BASE_URL}/biz-order-detail/BizOrderDetail_PrdOApyDet_TransPlanDet_PrdSalDetRightFinOutstorageDet_FinOutwarehouseDetLeft/findList"

    # 构建请求参数
    params = {
        "access_token": access_token  # 访问令牌作为查询参数
    }

    # 构建请求体
    payload = {
        "bizOrderDetailBizOrderIds": biz_order_detail_ids,  # 业务订单详情ID列表
        "bizOrderDetailBizOrderClazz": "BUSINESS_ORDER",  # 业务订单分类
        "bizOrderDetailBizOrderTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单租户ID
        "bizOrderDetailBizOrderIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单隔离ID
        "prdOApyDetPrdOApyClazz": "PRD_O_APY",  # 生产出库分类
        "prdOApyDetPrdOApyTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 生产出库租户ID
        "prdOApyDetPrdOApyIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 生产出库隔离ID
        "prdOApyDetClazz": "PRD_O_APY_DET",  # 生产出库详情分类
        "prdOApyDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 生产出库详情租户ID
        "prdOApyDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 生产出库详情隔离ID
        "transPlanDetClazz": "TRANS_PLAN_DET",  # 运输计划详情分类
        "transPlanDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 运输计划详情租户ID
        "transPlanDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 运输计划详情隔离ID
        "transPlanDetTransPlanClazz": "TRANS_PLAN",  # 运输计划分类
        "transPlanDetTransPlanTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 运输计划租户ID
        "transPlanDetTransPlanIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 运输计划隔离ID
        "prdSalDetClazz": "PRD_SAL_DET",  # 销售详情分类
        "prdSalDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 销售详情租户ID
        "prdSalDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 销售详情隔离ID
        "prdSalDetPrdSalClazz": "PRD_SAL",  # 销售分类
        "prdSalDetPrdSalTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 销售租户ID
        "prdSalDetPrdSalIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 销售隔离ID
        "finOutstorageDetClazz": "FIN_OUTSTORAGE_DET",  # 成品出库详情分类
        "finOutstorageDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 成品出库详情租户ID
        "finOutstorageDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 成品出库详情隔离ID
        "finOutstorageDetFinOutstorageClazz": "FIN_OUTSTORAGE",  # 成品出库分类
        "finOutstorageDetFinOutstorageTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 成品出库租户ID
        "finOutstorageDetFinOutstorageIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 成品出库隔离ID
        "finOutwarehouseDetClazz": "FIN_OUTWAREHOUSE_DET",  # 成品出仓详情分类
        "finOutwarehouseDetTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 成品出仓详情租户ID
        "finOutwarehouseDetIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 成品出仓详情隔离ID
        "finOutwarehouseDetFinOutwarehouseClazz": "FIN_OUTWAREHOUSE",  # 成品出仓分类
        "finOutwarehouseDetFinOutwarehouseTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 成品出仓租户ID
        "finOutwarehouseDetFinOutwarehouseIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 成品出仓隔离ID
        "gridList": [],  # 网格列表
        "bizOrderDetailClazz": "BUSINESS_ORDER_DETAIL",  # 业务订单详情分类
        "bizOrderDetailIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单详情隔离ID
        "bizOrderDetailTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单详情租户ID
        "prdSalDetPrdSalAuditStatus": "finish"  # 销售审核状态
    }

    # 构建请求头
    headers = {
        "Content-Type": "application/json",  # 内容类型
        "Accept": "application/json"  # 接受类型
    }

    try:
        # 发送POST请求
        response = requests.post(
            url, params=params, json=payload, headers=headers)
        response.raise_for_status()  # 检查HTTP错误

        # 解析响应数据
        result = response.json()

        if result.get('code') == 0:  # 请求成功
            return result.get('data', [])  # 返回数据列表
        else:
            print(f"接口4调用失败: {result.get('msg', '未知错误')}")  # 打印错误信息
            return []  # 返回空列表

    except requests.exceptions.RequestException as e:
        print(f"接口4请求异常: {str(e)}")  # 打印异常信息
        return []  # 返回空列表
    except Exception as e:
        print(f"接口4处理异常: {str(e)}")  # 打印处理异常
        return []  # 返回空列表


def call_interface1(access_token: str, product_name: str = "", start_time: str = "",
                    end_time: str = "", customer_short_name: str = ""):
    """
    封装接口1：调用生产工单BOM节点业务订单明细左连接查询接口

    Args:
        access_token: 访问令牌
        product_name: 产品名称，用于过滤查询
        start_time: 开始时间
        end_time: 结束时间
        customer_short_name: 客户简称

    Returns:
        list: 接口返回的数据列表，失败时返回空列表
    """
    # 构建API URL
    url = f"{BASE_URL}/biz-order-detail/productWorkOrder_BomNode_BizOrderDetailLeft/findList"

    # 构建请求参数
    params = {
        "access_token": access_token  # 访问令牌作为查询参数
    }

    # 处理时间参数，如果没有提供则使用默认值
    if not start_time:
        start_time = "2025-08-01 00:00:00"  # 默认开始时间
    if not end_time:
        end_time = "2025-09-30 23:59:59"  # 默认结束时间

    # 提取日期部分用于dateRange
    start_date = start_time.split(
        " ")[0] if " " in start_time else start_time  # 提取日期部分
    end_date = end_time.split(
        " ")[0] if " " in end_time else end_time  # 提取日期部分

    # 构建请求体（根据生产进度.txt中的真实请求参数）
    payload = {
        "bizOrderDetailClazz": "BUSINESS_ORDER_DETAIL",  # 业务订单明细分类
        "bizOrderDetailIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单明细隔离ID
        "bizOrderDetailTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单明细租户ID
        "bizOrderDetailBizOrderClazz": "BUSINESS_ORDER",  # 业务订单分类
        "bizOrderDetailBizOrderIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单隔离ID
        "bizOrderDetailBizOrderTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 业务订单租户ID
        "workOrderClazz": "WORK_ORDER",  # 工单分类
        "workOrderIsolation": "2caf3cb6216111eea71b49e0880a97d9",  # 工单隔离ID
        "workOrderTenantId": "2caf3cb6216111eea71b49e0880a97d9",  # 工单租户ID
        "dateRange": [start_date, end_date],  # 日期范围数组
        "workOrderUserCode": "",  # 工单用户编码
        "matUserCode": None,  # 物料用户编码
        "matName": product_name if product_name else "",  # 物料名称
        "customerUserCode": None,  # 客户用户编码
        "customerShortName": customer_short_name if customer_short_name else "",  # 客户简称
        "workOrderFromCreateTime": start_time,  # 工单创建开始时间
        "workOrderToCreateTime": end_time,  # 工单创建结束时间
        "bizOrderDetailBizOrderCustIds": [],  # 业务订单客户ID数组
        "bizOrderDetailMaterialIds": []  # 业务订单物料ID数组
    }

    try:
        # 构建请求头
        headers = {
            "Authorization": f"bearer {access_token}",  # 设置Bearer认证头
            "Content-Type": "application/json"  # 设置内容类型
        }

        # 发送HTTP POST请求
        response = requests.post(
            url, params=params, json=payload, headers=headers, timeout=30)
        response.raise_for_status()  # 检查HTTP响应状态

        # 解析响应数据
        response_data = response.json()

        # 检查业务逻辑是否成功
        if response_data.get("code") == 0 and response_data.get("msg") == "SUCCESS":
            # 返回数据列表
            return response_data.get("data", [])
        else:
            error_msg = response_data.get("msg", "未知错误")
            print(f"接口1调用失败: {error_msg}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"接口1 HTTP请求失败: {str(e)}")
        return []
    except Exception as e:
        print(f"接口1处理失败: {str(e)}")
        return []
