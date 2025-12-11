from fastmcp import FastMCP  # 导入FastMCP框架
from dotenv import load_dotenv  # 导入环境变量加载器
import os  # 导入操作系统模块
import requests  # 导入HTTP请求库
# 导入JSON转换CSV函数和数据绑定函数
from services.tool import json_to_csv, get_csv_header, get_ids, append_data
from services.cache import cache_save  # 导入缓存保存函数

# 加载环境变量
load_dotenv()  # 加载.env文件中的环境变量

# 从环境变量获取配置
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")  # 获取基础URL

finance_mcp = FastMCP(name="finance")  # 创建财务服务MCP实例


@finance_mcp.tool()
def find_pay_settle(access_token: str,
                    create_time_start: str,
                    create_time_end: str,
                    supplier_name: str = "") -> str:
    """
    获取财务数据表，主表，字段为供应商简称,供应商全称,币种,结账日,来源单号,来源日期,到货物料名称, 汇率,应结算金额,实际结算金额,采购数量,采购单价,采购金额,采购结算金额
    Args:
        access_token: 访问令牌
        create_time_start: 创建开始时间，格式为2025-07-02 00:00:00
        create_time_end: 创建结束时间，格式为2025-07-04 23:59:59
        supplier_name: 供应商名称，可选参数，默认值为空字符串

    Returns:
        table_token: 财务数据表令牌
    """
    return finance_find_pay_settle(access_token,
                                   pay_settle_det_pay_settle_from_receipt_date=create_time_start,
                                   pay_settle_det_pay_settle_to_receipt_date=create_time_end,
                                   supplier_name=supplier_name)


def finance_find_pay_settle(access_token: str,
                            pay_settle_det_pay_settle_from_receipt_date: str,
                            pay_settle_det_pay_settle_to_receipt_date: str,
                            supplier_name: str = "",) -> str:
    """
    获取财务数据保存CSV格式字符串到缓存。
    Args:
        access_token: 访问令牌
        pay_settle_det_pay_settle_from_receipt_date: 应付结算开始日期，格式为2025-09-01 00:00:00
        pay_settle_det_pay_settle_to_receipt_date: 应付结算结束日期，格式为2025-09-22 23:59:59
        supplier_name: 供应商名称，可选参数，默认值为空字符串
    Returns:
        result (str): 有效数据的列名清单，表示这些列有数据 / 没有数据
    """
    # 调用接口1获取财务数据
    interface1_data = call_pay_settle_interface1(access_token,
                                                 pay_settle_det_pay_settle_from_receipt_date,
                                                 pay_settle_det_pay_settle_to_receipt_date,
                                                 supplier_name=supplier_name)
    # 第二步：从接口1返回的data中提取matIds，调用接口2
    mat_ids = get_ids(interface1_data, "procOrderDetMaterialId")  # 提取物料ID列表

    # 调用接口2获取物料信息
    interface2_data = call_material_interface2(
        access_token, mat_ids)  # 调用物料接口2获取物料数据

    # 将接口2的数据绑定到接口1的数据中
    append_data(interface1_data, interface2_data,
                "procOrderDetMaterialId", "matId")  # 将物料数据绑定到主数据

    # 第三步：从接口1返回的data中提取supplierIds，调用接口4
    supplier_ids = get_ids(
        interface1_data, "paySettleDetPaySettleSupplierId")  # 提取供应商ID列表

    # 调用接口4获取供应商信息
    interface4_data = call_supplier_interface4(
        access_token, supplier_ids)  # 调用供应商接口4获取供应商数据
   # 将接口4的数据绑定到接口1的数据中
    append_data(interface1_data, interface4_data,
                "paySettleDetPaySettleSupplierId", "supplierId")  # 将供应商数据绑定到主数据

    # 定义字段映射（根据实际响应数据结构定义）
    grid_list = {
        # "paySettleDetId": "paySettleDetId",
        "frontFirstPaySettleAuditStatusDictName": "审核状态",
        # "paySettleDetPaySettleUserCode": "paySettleDetPaySettleUserCode",
        "frontFirstPaySettleMonth": "结算月份",
        "frontFirstPaySettleReceiptDate": "结算日期",
        "frontFirstPaySettleUserCode": "结算单号",
        "frontFirstSupplierClassificationName": "供应商分类",
        "frontFirstSupplierUserCode": "供应商编码",
        "supplierShortName": "供应商简称",  # "frontFirstSupplierShortName": "供应商简称"
        "supplierName": "供应商全称",  # "frontFirstSupplierName": "供应商全称"
        "supplierCurrencyId": "币种",  # "frontFirstSupplierCurrencyId": "币种"
        "frontFirstSupplierDefaultSettlementTypeName": "结算方式",
        "totalPaySettleTotalAmount": "总应结算金额",
        "totalPaySettleLocTotalAmount": "本币总应结算金额",
        "totalPaySettleTotalOtherExpense": "总其他费用",
        "frontFirstSupplierAccountPeriod": "结账天数",
        "totalPaySettleLocTotalOtherExpense": "本币总其他费用",
        "totalPaySettleTotalActAmount": "总实际结算金额",
        "totalPaySettleLocTotalActAmount": "本币总实际结算金额",
        "totalPaySettleTotalActDiffAmount": "总实际结算差额",
        # "frontFirstSupplierReconciliationDate": "结账日"
        "supplierReconciliationDate": "结账日",
        # "totalPaySettleLocTotalActDiffAmount": "本币总实际结算差额",
        "totalPaySettleTotalInvoicedAmount": "总已开票金额",
        "totalPaySettleLocTotalLocInvoicedAmount": "本币总已开票金额",
        "frontFirstPaySettleDescription": "总备注",
        "frontFirstPaySettlePrintTimes": "打印次数",
        "frontFirstPaySettleCreator": "制单人",
        "frontFirstAuditor": "审核人",
        "frontFirstPaySettleCreateTime": "制单时间",
        "frontFirstPaySettleAuditDate": "审核时间",
        "paySettleDetSourceTypeDictName": "数据来源",
        "frontFirstPaySettleUpdater": "最后修改人",
        "payableDetPayableUserCode": "来源单号",
        "frontPayableMonth": "来源月份",
        "payableDetPayableReceiptDate": "来源日期",
        "frontMatUserCode": "到货物料编码",
        "frontFirstPaySettleUpdateTime": "最后修改时间",
        "matName": "到货物料名称",  # "frontMatName": "到货物料名称",
        "frontFrontSpecName": "到货物料规格类型",
        "frontFrontUnitName": "到货物料单位",
        "payableDetExchangeRate": "汇率",
        # "payableDetOffActAmount": "来源结算金额",
        # "payableDetLocOffActAmount": "本币来源结算金额",
        "frontFrontMaterialClassName": "到货物料分类",
        "paySettleDetQuantity": "应结算金额",
        "paySettleDetOtherExpense": "其他费用",
        "paySettleDetActAmount": "实际结算金额",
        # "paySettleDetLocAmount": "本币应结算金额",
        # "paySettleDetLocActAmount": "本币实际结算金额",
        "paySettleDetActDiffAmount": "实际结算差额",
        # "paySettleDetLocActDiffAmount": "本币实际结算差额",
        "paySettleDetDescription": "明细备注",
        "paySettleDetCompleteStatusDictName": "单据状态",
        "发票号码": "发票号码",
        "paySettleDetCompleteQuantity": "已收票金额",
        "paySettleDetLocInvoicedAmount": "本币已收票金额",
        "payableDetSourceTypeDictName": "对账类型",
        "frontStatementMonth": "对账月份",
        "frontStatementUserCode": "对账单号",
        "frontStatementSettleAmount": "对账结算金额",
        "frontStatementLocSettleAmount": "本币对账结算金额",
        "frontDocumentTypeName": "单据类型",
        "frontArrUserCode": "到货单号",
        "frontArrSourceReceiptTypeName": "业务类型",
        "frontProcUserCode": "采购单号",
        "frontProcDeliveryDate": "采购交货日期",
        "procOrderDetQuantity": "采购数量",  # "frontProcQuantity": "采购数量"
        "procOrderDetGiftQty": "采购赠送数",  # "frontProcGiftQty": "采购赠送数"
        "procOrderDetSumQty": "采购总数",  # "frontProcSumQty": "采购总数"
        "procOrderDetLocUnitPrice": "采购单价",  # "frontPocUnitPriceTax": "采购单价"
        "procOrderDetLocalAmount": "采购金额",  # "frontProcLocalAmount": "采购金额"
        "frontProcOtherExpenses": "采购其他费用",  # "frontProcOtherExpenses": "采购其他费用"
        "procOrderDetSettleAmount": "采购结算金额",  # "frontProcSettleAmount": "采购结算金额"
        "frontProcDescription": "采购明细备注",  # "frontProcDescription": "采购明细备注"
        # "paySettleDetPaySettleId": "paySettleId",
        "paySettleDetPaySettleBankName": "我司银行名称",
        "paySettleDetPaySettleBankAcctNum": "银行账号",
        "paySettleDetPaySettleAcctHolderName": "账号持有人",
        "paySettleDetPaySettleBankBranchInfo": "开户行信息",
        "paySettleDetPaySettleAuditStatus": "审核状态"
    }  # 字段映射字典，需要根据实际数据结构填充

    csv_str = json_to_csv(interface1_data, grid_list)  # 转换为CSV格式

    print(f"finance_find_all 转换为CSV格式数据: {csv_str}")

    if csv_str:  # 如果转换成功
        key = f"财务数据表_{access_token}"
        cache_save(key, csv_str)  # 保存到缓存
        #header = get_csv_header(csv_str)  # 获取CSV头部
        return key  # 返回列名清单
    else:
        return "没有数据"  # 没有数据时返回提示


def call_pay_settle_interface1(access_token: str,
                               pay_settle_det_pay_settle_from_receipt_date: str = "",
                               pay_settle_det_pay_settle_to_receipt_date: str = "",
                               supplier_name: str = "",
                               pay_settle_det_pay_settle_clazz: str = "PAY_SETTLE",
                               pay_settle_det_pay_settle_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pay_settle_det_pay_settle_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pay_settle_det_clazz: str = "PAY_SETTLE_DET",
                               pay_settle_det_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pay_settle_det_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mat_arr_det_clazz: str = "MAT_ARR_DET",
                               mat_arr_det_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mat_arr_det_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mat_arr_det_mat_arr_clazz: str = "MAT_ARR",
                               mat_arr_det_mat_arr_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mat_arr_det_mat_arr_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               proc_order_det_clazz: str = "PROCUREMENT_ORDER_DETAIL",
                               proc_order_det_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               proc_order_det_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               proc_order_det_proc_order_clazz: str = "PROCUREMENT_ORDER",
                               proc_order_det_proc_order_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               proc_order_det_proc_order_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               work_order_clazz: str = "WORK_ORDER",
                               work_order_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               work_order_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               biz_order_detail_clazz: str = "BUSINESS_ORDER_DETAIL",
                               biz_order_detail_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               biz_order_detail_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               biz_order_detail_biz_order_clazz: str = "BUSINESS_ORDER",
                               biz_order_detail_biz_order_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               biz_order_detail_biz_order_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pur_requ_det_clazz: str = "PURCHASE_REQUISITION_DETAIL",
                               pur_requ_det_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pur_requ_det_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pur_requ_det_pur_requ_clazz: str = "PURCHASE_REQUISITION",
                               pur_requ_det_pur_requ_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pur_requ_det_pur_requ_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mat_clazz: str = "MATERIAL",
                               mat_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mat_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               bom_node_clazz: str = "BOM_PROCESS",
                               bom_node_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               bom_node_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               bom_node_quantity_clazz: str = "MATERIAL-BOM_PROCESS",
                               bom_node_quantity_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               bom_node_quantity_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pur_frt_det_pur_frt_clazz: str = "PURCHASE_FORECASTING",
                               pur_frt_det_pur_frt_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pur_frt_det_pur_frt_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pur_frt_det_clazz: str = "PURCHASE_FORECASTING_DET",
                               pur_frt_det_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               pur_frt_det_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mkt_frt_det_mkt_frt_clazz: str = "MARKET_FORECASTING",
                               mkt_frt_det_mkt_frt_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mkt_frt_det_mkt_frt_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mkt_frt_det_clazz: str = "MARKET_FORECASTING_DET",
                               mkt_frt_det_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               mkt_frt_det_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               supp_statement_det_supp_statement_clazz: str = "SUPP_STATEMENT",
                               supp_statement_det_supp_statement_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               supp_statement_det_supp_statement_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               supp_statement_det_clazz: str = "SUPP_STATEMENT_DET",
                               supp_statement_det_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               supp_statement_det_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               payable_det_payable_clazz: str = "PAYABLE",
                               payable_det_payable_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               payable_det_payable_isolation: str = "2caf3cb6216111eea71b49e0880a97d9",
                               payable_det_clazz: str = "PAYABLE_DET",
                               payable_det_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                               payable_det_isolation: str = "2caf3cb6216111eea71b49e0880a97d9") -> str:
    # 构建请求URL
    url = f"{BASE_URL}/pay-settle-det/paySettleDet_payableDet_suppStatementDet_matArrDet_ProcOrderDet_PurRequDet_PutBomNodeQuantity_BizOrderDetail__WorkOrderLeft/findList?access_token={access_token}"
    print(url)  # 打印请求URL用于调试

    # 构建请求体
    payload = {  # 构建POST请求的数据体
        "supplierName": supplier_name,  # 供应商全称
        "paySettleDetPaySettleClazz": pay_settle_det_pay_settle_clazz,  # 应付结算类别
        "paySettleDetPaySettleTenantId": pay_settle_det_pay_settle_tenant_id,  # 应付结算租户ID
        "paySettleDetPaySettleIsolation": pay_settle_det_pay_settle_isolation,  # 应付结算隔离ID
        "paySettleDetClazz": pay_settle_det_clazz,  # 应付结算明细类别
        "paySettleDetTenantId": pay_settle_det_tenant_id,  # 应付结算明细租户ID
        "paySettleDetIsolation": pay_settle_det_isolation,  # 应付结算明细隔离ID
        "matArrDetClazz": mat_arr_det_clazz,  # 物料到货明细类别
        "matArrDetTenantId": mat_arr_det_tenant_id,  # 物料到货明细租户ID
        "matArrDetIsolation": mat_arr_det_isolation,  # 物料到货明细隔离ID
        "matArrDetMatArrClazz": mat_arr_det_mat_arr_clazz,  # 物料到货类别
        "matArrDetMatArrTenantId": mat_arr_det_mat_arr_tenant_id,  # 物料到货租户ID
        "matArrDetMatArrIsolation": mat_arr_det_mat_arr_isolation,  # 物料到货隔离ID
        "procOrderDetClazz": proc_order_det_clazz,  # 采购订单明细类别
        "procOrderDetTenantId": proc_order_det_tenant_id,  # 采购订单明细租户ID
        "procOrderDetIsolation": proc_order_det_isolation,  # 采购订单明细隔离ID
        "procOrderDetProcOrderClazz": proc_order_det_proc_order_clazz,  # 采购订单类别
        "procOrderDetProcOrderTenantId": proc_order_det_proc_order_tenant_id,  # 采购订单租户ID
        "procOrderDetProcOrderIsolation": proc_order_det_proc_order_isolation,  # 采购订单隔离ID
        "workOrderClazz": work_order_clazz,  # 工单类别
        "workOrderTenantId": work_order_tenant_id,  # 工单租户ID
        "workOrderIsolation": work_order_isolation,  # 工单隔离ID
        "bizOrderDetailClazz": biz_order_detail_clazz,  # 业务订单明细类别
        "bizOrderDetailTenantId": biz_order_detail_tenant_id,  # 业务订单明细租户ID
        "bizOrderDetailIsolation": biz_order_detail_isolation,  # 业务订单明细隔离ID
        "bizOrderDetailBizOrderClazz": biz_order_detail_biz_order_clazz,  # 业务订单类别
        "bizOrderDetailBizOrderTenantId": biz_order_detail_biz_order_tenant_id,  # 业务订单租户ID
        "bizOrderDetailBizOrderIsolation": biz_order_detail_biz_order_isolation,  # 业务订单隔离ID
        "purRequDetClazz": pur_requ_det_clazz,  # 采购申请明细类别
        "purRequDetTenantId": pur_requ_det_tenant_id,  # 采购申请明细租户ID
        "purRequDetIsolation": pur_requ_det_isolation,  # 采购申请明细隔离ID
        "purRequDetPurRequClazz": pur_requ_det_pur_requ_clazz,  # 采购申请类别
        "purRequDetPurRequTenantId": pur_requ_det_pur_requ_tenant_id,  # 采购申请租户ID
        "purRequDetPurRequIsolation": pur_requ_det_pur_requ_isolation,  # 采购申请隔离ID
        "matClazz": mat_clazz,  # 物料类别
        "matTenantId": mat_tenant_id,  # 物料租户ID
        "matIsolation": mat_isolation,  # 物料隔离ID
        "bomNodeClazz": bom_node_clazz,  # BOM节点类别
        "bomNodeTenantId": bom_node_tenant_id,  # BOM节点租户ID
        "bomNodeIsolation": bom_node_isolation,  # BOM节点隔离ID
        "bomNodeQuantityClazz": bom_node_quantity_clazz,  # BOM节点数量类别
        "bomNodeQuantityTenantId": bom_node_quantity_tenant_id,  # BOM节点数量租户ID
        "bomNodeQuantityIsolation": bom_node_quantity_isolation,  # BOM节点数量隔离ID
        "purFrtDetPurFrtClazz": pur_frt_det_pur_frt_clazz,  # 采购预测类别
        "purFrtDetPurFrtTenantId": pur_frt_det_pur_frt_tenant_id,  # 采购预测租户ID
        "purFrtDetPurFrtIsolation": pur_frt_det_pur_frt_isolation,  # 采购预测隔离ID
        "purFrtDetClazz": pur_frt_det_clazz,  # 采购预测明细类别
        "purFrtDetTenantId": pur_frt_det_tenant_id,  # 采购预测明细租户ID
        "purFrtDetIsolation": pur_frt_det_isolation,  # 采购预测明细隔离ID
        "mktFrtDetMktFrtClazz": mkt_frt_det_mkt_frt_clazz,  # 市场预测类别
        "mktFrtDetMktFrtTenantId": mkt_frt_det_mkt_frt_tenant_id,  # 市场预测租户ID
        "mktFrtDetMktFrtIsolation": mkt_frt_det_mkt_frt_isolation,  # 市场预测隔离ID
        "mktFrtDetClazz": mkt_frt_det_clazz,  # 市场预测明细类别
        "mktFrtDetTenantId": mkt_frt_det_tenant_id,  # 市场预测明细租户ID
        "mktFrtDetIsolation": mkt_frt_det_isolation,  # 市场预测明细隔离ID
        "suppStatementDetSuppStatementClazz": supp_statement_det_supp_statement_clazz,  # 供应商对账单类别
        "suppStatementDetSuppStatementTenantId": supp_statement_det_supp_statement_tenant_id,  # 供应商对账单租户ID
        "suppStatementDetSuppStatementIsolation": supp_statement_det_supp_statement_isolation,  # 供应商对账单隔离ID
        "suppStatementDetClazz": supp_statement_det_clazz,  # 供应商对账单明细类别
        "suppStatementDetTenantId": supp_statement_det_tenant_id,  # 供应商对账单明细租户ID
        "suppStatementDetIsolation": supp_statement_det_isolation,  # 供应商对账单明细隔离ID
        "payableDetPayableClazz": payable_det_payable_clazz,  # 应付账款类别
        "payableDetPayableTenantId": payable_det_payable_tenant_id,  # 应付账款租户ID
        "payableDetPayableIsolation": payable_det_payable_isolation,  # 应付账款隔离ID
        "payableDetClazz": payable_det_clazz,  # 应付账款明细类别
        "payableDetTenantId": payable_det_tenant_id,  # 应付账款明细租户ID
        "payableDetIsolation": payable_det_isolation,  # 应付账款明细隔离ID
        "orderBys": [  # 排序条件
            {
                "field": "paySettleDetPaySettleReceiptDate",  # 排序字段为应付结算单据日期
                "order": "DESC"  # 降序排列
            }
        ]
    }

    # 添加日期过滤条件
    if pay_settle_det_pay_settle_from_receipt_date:  # 如果有开始日期
        # 设置开始日期
        payload["paySettleDetPaySettleFromReceiptDate"] = pay_settle_det_pay_settle_from_receipt_date
    if pay_settle_det_pay_settle_to_receipt_date:  # 如果有结束日期
        # 设置结束日期
        payload["paySettleDetPaySettleToReceiptDate"] = pay_settle_det_pay_settle_to_receipt_date

    try:
        # 构建请求头
        headers = {  # 构建HTTP请求头
            "Authorization": f"bearer {access_token}",  # 设置Bearer认证头
            "Content-Type": "application/json"  # 设置内容类型
        }

        # 发送HTTP POST请求
        response = requests.post(
            url, json=payload, headers=headers, timeout=30)  # 发送POST请求并设置超时时间和请求头
        response.raise_for_status()  # 检查HTTP响应状态

        # 解析响应数据
        response_data = response.json()  # 解析JSON响应

        # 检查业务逻辑是否成功
        if response_data.get("code") == 0 and response_data.get("msg") == "SUCCESS":
            data_list = response_data["data"]  # 获取数据列表
            return data_list  # 返回数据列表
        else:
            error_msg = response_data.get("msg", "未知错误")  # 获取错误信息
            return f"接口调用失败: {error_msg}"  # 返回错误信息

    except requests.exceptions.RequestException as e:  # 捕获请求异常
        print(f"HTTP请求失败: {str(e)}")  # 打印错误信息
        return f"请求失败: {str(e)}"  # 返回错误信息
    except Exception as e:  # 捕获其他异常
        print(f"处理失败: {str(e)}")  # 打印错误信息
        return f"处理失败: {str(e)}"  # 返回错误信息


def call_material_interface2(access_token: str, mat_ids: list,
                             mat_clazz: str = "MATERIAL",
                             mat_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                             mat_isolation: str = "2caf3cb6216111eea71b49e0880a97d9") -> list:
    """
    调用物料接口2获取物料信息
    Args:
        access_token: 访问令牌
        mat_ids: 物料ID列表
        mat_clazz: 物料类别
        mat_tenant_id: 物料租户ID
        mat_isolation: 物料隔离ID

    Returns:
        list: 物料数据列表
    """
    # 构建请求URL
    # 构建物料查询接口URL
    url = f"{BASE_URL}/material/findList?access_token={access_token}"
    print(url)  # 打印请求URL用于调试

    # 构建请求体
    payload = {  # 构建POST请求的数据体
        "gridList": [  # 需要返回的字段列表
            "matDefaultStatisticsSpecificationTypeId",  # 物料默认统计规格类型ID
            "matDefaultType",  # 物料默认类型
            "matDescription",  # 物料描述
            "matExtension",  # 物料扩展信息
            "matFlags",  # 物料标志
            "matId",  # 物料ID
            "matIsMatClassification",  # 是否为物料分类
            "matName",  # 物料名称
            "matParentId",  # 物料父级ID
            "matSearchCode",  # 物料搜索编码
            "matSerialNumber",  # 物料序列号
            "matSystemCode",  # 物料系统编码
            "matUserCode",  # 物料用户编码
            "matValueDTOS",  # 物料值DTO列表
            "matVersion",  # 物料版本
            "matTenantId",  # 物料租户ID
            "matIsolation",  # 物料隔离ID
            "matCreateTime",  # 物料创建时间
            "matUpdateTime",  # 物料更新时间
            "matAuditDate"  # 物料审核日期
        ],
        "matIds": mat_ids,  # 物料ID列表
        "matClazz": mat_clazz,  # 物料类别
        "matIsolation": mat_isolation,  # 物料隔离ID
        "matTenantId": mat_tenant_id  # 物料租户ID
    }

    try:
        # 构建请求头
        headers = {  # 构建HTTP请求头
            "Authorization": f"bearer {access_token}",  # 设置Bearer认证头
            "Content-Type": "application/json"  # 设置内容类型
        }

        # 发送HTTP POST请求
        response = requests.post(
            url, json=payload, headers=headers, timeout=30)  # 发送POST请求，超时30秒

        # 检查响应状态
        if response.status_code == 200:  # 如果响应状态为200
            result = response.json()  # 解析JSON响应
            if result.get("code") == 0:  # 如果响应码为0表示成功
                data_list = result.get("data", [])  # 获取数据列表
                # 打印获取的数据条数
                print(f"call_material_interface2 获取到 {len(data_list)} 条物料数据")
                return data_list  # 返回数据列表
            else:
                # 打印错误信息
                print(
                    f"call_material_interface2 接口返回错误: {result.get('msg', '未知错误')}")
                return []  # 返回空列表
    except requests.exceptions.RequestException as e:  # 捕获请求异常
        print(f"call_supplier_interface4 请求异常: {str(e)}")  # 打印异常信息
        return []  # 返回空列表
    except Exception as e:  # 捕获其他异常
        print(f"call_supplier_interface4 发生错误: {str(e)}")  # 打印错误信息
        return []  # 返回空列表


def call_supplier_interface4(access_token: str, supplier_ids: list,
                             supplier_clazz: str = "XY_USERCENTER_ORGANIZATION",
                             supplier_tenant_id: str = "2caf3cb6216111eea71b49e0880a97d9",
                             supplier_isolation: str = "2caf3cb6216111eea71b49e0880a97d9") -> list:
    """
    调用供应商接口4获取供应商信息
    Args:
        access_token: 访问令牌
        supplier_ids: 供应商ID列表
        supplier_clazz: 供应商类别
        supplier_tenant_id: 供应商租户ID
        supplier_isolation: 供应商隔离ID

    Returns:
        list: 供应商数据列表
    """
    # 构建请求URL
    # 构建供应商查询接口URL
    url = f"{BASE_URL}/supplier/findList?access_token={access_token}"
    print(url)  # 打印请求URL用于调试

    # 构建请求体
    payload = {  # 构建POST请求的数据体
        "gridList": [  # 需要返回的字段列表
            "supplierShortName",  # 供应商简称
            "supplierName",  # 供应商名称
            "supplierUserCode",  # 供应商用户编码
            "supplierId",  # 供应商ID
            "supplierClassification",  # 供应商分类
            "supplierLevel",  # 供应商级别
            "supplierDefaultInvoiceTypeTaxRate",  # 供应商默认发票类型税率
            "supplierCurrencyId",  # 供应商币种ID
            "supplierDefaultDeliveryType",  # 供应商默认交货类型
            "supplierDefaultSettlementType",  # 供应商默认结算类型
            "supplierAccountPeriod",  # 供应商账期
            "supplierEnterpriseTaxIdentificationNumber",  # 供应商企业税务识别号
            "supplierMobile",  # 供应商手机号
            "supplierTelephone",  # 供应商电话
            "supplierEmail",  # 供应商邮箱
            "supplierFaxNo",  # 供应商传真号
            "supplierBankAccountId",  # 供应商银行账户ID
            "supplierSequenceNumber",  # 供应商序列号
            "supplierReconciliationDate",  # 供应商对账日期
            "supplierParentSupplierid",  # 供应商父级供应商ID
            "supplierRegistrationDistrict",  # 供应商注册区域
            "supplierLegalId",  # 供应商法人ID
            "supplierRegistrantId",  # 供应商注册人ID
            "supplierRegistrationProvince",  # 供应商注册省份
            "supplierBusinessScope",  # 供应商经营范围
            "supplierRegistrationAddress",  # 供应商注册地址
            "supplierRegistrationCapital",  # 供应商注册资本
            "supplierRegistrantName",  # 供应商注册人姓名
            "supplierLegalName",  # 供应商法人姓名
            "supplierTenantId",  # 供应商租户ID
            "supplierRegistrationDate",  # 供应商注册日期
            "supplierRegistrationCity",  # 供应商注册城市
            "supplierRegistrantIds",  # 供应商注册人ID列表
            "supplierLocationProvince",  # 供应商所在省份
            "supplierSomeoneContactId",  # 供应商联系人ID
            "supplierLocationAddress",  # 供应商所在地址
            "supplierSomeoneCertificateId",  # 供应商证件ID
            "supplierIdentification",  # 供应商身份识别
            "supplierNationality",  # 供应商国籍
            "supplierLocationDistrict",  # 供应商所在区域
            "supplierLocationCity",  # 供应商所在城市
            "supplierOrSomeoneList",  # 供应商或联系人列表
            "supplierExtension",  # 供应商扩展信息
            "supplierFlags",  # 供应商标志
            "supplierDescription",  # 供应商描述
            "supplierState",  # 供应商状态
            "supplierSerialNumber",  # 供应商序列号
            "supplierIsolation",  # 供应商隔离ID
            "supplierParentId",  # 供应商父级ID
            "supplierDefaultType",  # 供应商默认类型
            "supplierSystemCode",  # 供应商系统编码
            "supplierAuditStatus",  # 供应商审核状态
            "supplierCreateTime",  # 供应商创建时间
            "supplierUpdateTime",  # 供应商更新时间
            "supplierAuditDate"  # 供应商审核日期
        ],
        "supplierIds": supplier_ids,  # 供应商ID列表
        "supplierClazz": supplier_clazz,  # 供应商类别
        "supplierIsolation": supplier_isolation,  # 供应商隔离ID
        "supplierTenantId": supplier_tenant_id  # 供应商租户ID
    }

    try:
        # 构建请求头
        headers = {  # 构建HTTP请求头
            "Authorization": f"bearer {access_token}",  # 设置Bearer认证头
            "Content-Type": "application/json"  # 设置内容类型
        }

        # 发送HTTP POST请求
        response = requests.post(
            url, json=payload, headers=headers, timeout=30)  # 发送POST请求，超时30秒

        # 检查响应状态
        if response.status_code == 200:  # 如果响应状态为200
            result = response.json()  # 解析JSON响应
            if result.get("code") == 0:  # 如果响应码为0表示成功
                data_list = result.get("data", [])  # 获取数据列表
                # 打印获取的数据条数
                print(f"call_supplier_interface4 获取到 {len(data_list)} 条供应商数据")
                return data_list  # 返回数据列表
            else:
                # 打印错误信息
                print(
                    f"call_supplier_interface4 接口返回错误: {result.get('msg', '未知错误')}")
                return []  # 返回空列表
        else:
            # 打印HTTP错误状态
            print(
                f"call_supplier_interface4 HTTP请求失败，状态码: {response.status_code}")
            return []  # 返回空列表

    except requests.exceptions.RequestException as e:  # 捕获请求异常
        print(f"call_material_interface2 请求异常: {str(e)}")  # 打印异常信息
        return []  # 返回空列表
    except Exception as e:  # 捕获其他异常
        print(f"call_material_interface2 发生错误: {str(e)}")  # 打印错误信息
        return []  # 返回空列表
