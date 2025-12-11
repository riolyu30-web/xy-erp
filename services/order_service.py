from fastmcp import FastMCP  # 导入FastMCP框架
from dotenv import load_dotenv  # 导入环境变量加载器
import os  # 导入操作系统模块
import requests  # 导入HTTP请求库
from services.tool import json_to_csv, get_csv_header  # 导入JSON转换CSV函数
from services.cache import cache_save

# 加载环境变量
load_dotenv()  # 加载.env文件中的环境变量

# 从环境变量获取配置
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")  # 获取基础URL

order_mcp = FastMCP(name="order")  # 创建订单服务MCP实例


@order_mcp.tool()
def find_all(access_token: str, order_states: str = "", order_number: str = "", material_name: str = "", customer_short_name: str = "", material_classification_name: str = "", full_paper_name: str = "", create_time_start: str = "", create_time_end: str = "") -> str:
    """
    获取订单数据保存CSV格式字符串到缓存。
    数据列：审核状态,订单状态,订单号,创建时间,客方货号,产品编码,版本号,客户简称,产品名称,盒型,数量,入库数量,工单数,出库数量,备注（生产）,客户PO,长,宽,高,订单类型,含税报价单价,含税总金额,纸质,客户编码,库存数,创建人,盒型编码,货期,含税单价,跟单员,业务员,产品规格,不含税单价,不含税总金额,详细地址,后修改日期,是否生产,是否采购,预计交期,不含税报价单价,本币单价,本币金额,最后修改人,打印次数,订单状态,客户产品名称,结算单价,结算金额,单据日期,完成状态
    Args:
        access_token: 访问令牌
        order_states: 订单状态可多选用逗号连接，选项：正常、送货完成、生成完成、取消、完成，默认为所有状态
order_number: 订单号，默认为空字符串
        material_name: 产品名称，默认为空字符串
        customer_short_name: 客户简称，默认为空字符串
        material_classification_name: 盒型名称，默认为空字符串
        full_paper_name: 纸质名称，默认为空字符串
        create_time_start: 创建开始时间，格式为2025-07-02 00:00:00
        create_time_end: 创建结束时间，格式为2025-07-04 23:59:59
    Returns:
        table_token(str): 有效数据的表令牌，表示这些列有数据 / 没有数据
    """
    return order_find_all(access_token, order_states, order_number, material_name, customer_short_name, material_classification_name, full_paper_name, create_time_start, create_time_end)


def order_find_all(access_token: str, order_states: str = "", order_number: str = "", material_name: str = "", customer_short_name: str = "", material_classification_name: str = "", full_paper_name: str = "", create_time_start: str = "", create_time_end: str = "") -> str:

    # 状态映射字典：中文状态到数字状态的转换
    state_mapping = {
        "正常": "0",
        "送货完成": "1",
        "生成完成": "2",
        "取消": "3",
        "完成": "4"
    }

    # 转换中文状态为数字状态
    if order_states:
        # 将中文状态转换为对应的数字状态
        numeric_states = [state_mapping.get(
            state, state) for state in order_states if state in state_mapping]
    else:
        # 默认使用所有状态
        numeric_states = ["0"]
    # 构建请求URL
    # 构建完整请求URL
    url = f"{BASE_URL}/market/erp_business_mgt_order_notice/es/getExperienceData?access_token={access_token}"
    print(url)
    # 构建请求体
    payload = {  # 构建POST请求的数据体
        "model": {
            "createTimeStart": create_time_start,  # 设置开始时间
            "createTimeEnd": create_time_end,  # 设置结束时间
            "orderDataState": numeric_states,  # 设置订单状态过滤条件（使用转换后的数字状态）
            "orderNumber": order_number,  # 设置订单号过滤条件
            "materialName": material_name,  # 设置物料名称过滤条件
            "customerShortName": customer_short_name,  # 设置客户简称过滤条件
            "materialClassificationName": material_classification_name,  # 设置物料分类名称过滤条件
            "fullPaperName": full_paper_name  # 设置全纸名称过滤条件
        },
        "size": 10000000,  # 设置返回数据大小
        "current": 1,  # 设置当前页码
        "total": 0,  # 设置总数
        "loading": True,  # 设置加载状态
        "small": False,  # 设置小尺寸标志
        "pages": 20  # 设置总页数
    }

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
        # print(response_data)

        # 检查业务逻辑是否成功
        if response_data.get("code") == 0 and response_data.get("msg") == "SUCCESS":
            data_list = response_data["data"]["list"]
            grid_list = {
                "auditStatus": "审核状态",
                "orderDataStateName": "订单状态",
                "orderNumber": "订单号",
                "createDate": "创建时间",
                "externalMaterialCode": "客方货号",
                "materialCode": "产品编码",
                "boxVersion": "版本号",
                "customerShortName": "客户简称",
                "materialName": "产品名称",
                "materialClassificationName": "盒型",
                "quantity": "数量",
                "inventoryQuantity": "入库数量",
                "workQuantity": "工单数",
                "outQuantity": "出库数量",
                "description": "备注（生产）",
                "externalTrackingNumber": "客户PO",
                "length": "长",
                "width": "宽",
                "height": "高",
                "orderType": "订单类型",
                "quotationUnitPriceIncludingTax": "含税报价单价",
                "totalAmountIncludingTax": "含税总金额",
                "fullPaperName": "纸质",
                "customerCode": "客户编码",
                "inventoryQuantitys": "库存数",
                "creator": "创建人",
                "searchCode": "盒型编码",
                "deliveryDate": "货期",
                "unitPriceIncludingTax": "含税单价",
                "merchandiserName": "跟单员",
                "salesmanName": "业务员",
                "materialSpecification": "产品规格",
                "unitPriceWithoutTax": "不含税单价",
                "totalAmountWithoutTax": "不含税总金额",
                "deliveryAddress": "详细地址",
                "lastUpdateDate": "后修改日期",
                "isProduction": "是否生产",
                "isPurchase": "是否采购",
                "expectedReceiptDate": "预计交期",
                "quotationUnitPriceWithoutTax": "不含税报价单价",
                "localCurrencyUnitPrice": "本币单价",
                "localCurrencyTotalAmount": "本币金额",
                "lastUpdater": "最后修改人",
                "printTimes": "打印次数",
                "orderDateStateName": "订单状态",
                "externalMaterialName": "客户产品名称",
                "settlementUnitPrice": "结算单价",
                "settlementTotalAmount": "结算金额",
                "receiptDate": "单据日期",
                "farmatCompletionStatus": "完成状态"
            }
            csv_str = json_to_csv(data_list, grid_list)

            if csv_str:
                table_token = f"订单表_{access_token}"
                cache_save(table_token, csv_str)
                # header = get_csv_header(csv_str)
                return table_token

            return "没有数据"
        else:
            error_msg = response_data.get("msg", "未知错误")
            return error_msg

    except requests.exceptions.RequestException as e:  # 捕获请求异常
        print(f"HTTP请求失败: {str(e)}")  # 打印错误信息
        return f"请求失败: {str(e)}"  # 返回错误信息
    except Exception as e:  # 捕获其他异常
        print(f"处理失败: {str(e)}")  # 打印错误信息
        return f"处理失败: {str(e)}"  # 返回错误信息
