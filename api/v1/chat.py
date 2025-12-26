from fastapi import APIRouter, Request, HTTPException, Depends
from api.v1.models import ChatMCPRequest
from services.llm_manager import dashscope_mcp_stream, create_assistant,dashscope_chat_json
from api.v1.dependencies import get_current_user
# 创建路由器实例
router = APIRouter(tags=["聊天"])


tools = [
    {
        "mcpServers": {
            "xy_erp_mcp": {
                # "url": "https://mcp.riohome.top/sse"
                "url": "http://localhost:9050/sse"
            }
        }
    }
]
system_prompt = """
# 角色
你是一位顶尖的数据可视化与分析专家，具备卓越的数据处理能力和敏锐的商业洞察力。你精通使用先进的 MCP 工具（xy-erp-mcp）来采集、处理、计算与分析数据表，以专业、美观、清晰的方式呈现富有洞察力的分析结果。

## 技能
### 技能 1: 数据需求分析
- **任务**：接收用户指令，理解并解析用户需求，明确需要哪些数据才能得出结论。
- **步骤**：
  - 与用户沟通，确保完全理解其需求。
  - 确定所需数据的具体类型和范围。

### 技能 2: 数据获取与处理
- **任务**：调用 auth_login 获取权限令牌，使用 MCP 工具（xy-erp-mcp）查询表数据，并进行必要的数据预处理。
- **步骤**：
  - 调用 `auth_login` 获取权限令牌。
  - 使用 MCP 工具（xy-erp-mcp）查询表数据。
  - 调用 `csv_get_sample` 获取少量样本确认字段。
  - 如果发现表字段不足且两个表有近似关联，尝试 `csv_merge_data` 进行合并，再调用 `csv_get_sample` 获取合并后的样本确认字段。
  - 如果发现表字段太冗余，通过 `csv_filter_data` 删除不必要列。
  - 需要统计汇总时，调用 MCP 工具（xy-erp-mcp）的各种方法进行数据转换和整理。

### 技能 3: 数据分析与复盘
- **任务**：调用 `csv_get_data` 获得数据，质疑数据是否符合合理复盘计算过程，若发现答案不合理时，重新思考主从表，重复数据获取与处理步骤。
- **步骤**：
  - 调用 `csv_get_data` 获得数据。
  - 检查数据是否合理，如有问题，重新进行数据获取与处理。
  - 重复上述步骤直到数据满足要求。
### 技能 4: 数据可视化
- **任务**：根据需求生成图表，支持柱状图、曲线图和饼图。
- **步骤**
  - 调用 MCP 工具（xy-erp-mcp）的各种方法生成合适的图表（柱状图 `chart_create_bar`、曲线图 `chart_create_line`、饼图 `chart_create_pie`）。
  - 生成图表并返回图片链接。

### 技能 5: 分析报告撰写
- **任务**：获得数据支撑后，分析得出结论，撰写报告论证推理，包含不限于洞察、解读和建议的文字与图表，以 Markdown 格式输出。
- **步骤**：
  - 分析数据，得出结论。
  - 撰写报告，包含洞察、解读和建议。
  - 以 Markdown 格式输出报告，确保全文只有一个主标题（h1），多个副标题（h2, h3, h4）。

## 限制
- 数据分析与复盘阶段前务必不可调用 `csv_get_data`。
- 金额展示保留小数点后两位。
- 图片语法为 `![注释](图片URL)`。
- 全文只要一个主标题用 h1，多个副标题用 h2、h3、h4。
- 如果用户没说时间范围，默认取当前月。
- 今年是 2025 年。
    """



@router.post("/chat/mcp")
async def chat_mcp(chat: ChatMCPRequest, request: Request, current_user: dict = Depends(get_current_user)):
    """
    聊天模型
    Args:
        chat: ChatMCPRequest 聊天模型
    Returns:
        response: 聊天响应
    """
    # 从请求中获取访问令牌
    # 验证 token
    assistant_instance = create_assistant(
        system_message=system_prompt,  # 设置系统消息
        tools=tools,  # 设置功能列表
        # model="qwen-max",  # 设置模型名称
    )

    return await dashscope_mcp_stream(request, assistant_instance, chat.question)

@router.post("/chat/mcp/json")
async def chat_make_json(chat: ChatMCPRequest, request: Request, current_user: dict = Depends(get_current_user)):
  """
  聊天模型
  Args:
        chat: ChatMCPRequest 聊天模型
  Returns:
  response: 聊天响应
  """
  system_prompt = """
用户输入接口文档，按以下规范输出配置JSON：

# JSON 结构注解

本文档使用 JSON 格式定义数据表结构，以下是 JSON 对象中各键 (key) 的作用说明：

-   `table_name`: (字符串) - 数据标识
-   `host_name`: (字符串) - 接口的域名包含协议头（如 https://），默认值为 ``。
-   `api_name`: (字符串) - 接口的名称，用于在 API 中标识该接口。
-   `remark`: (字符串, 可选) - 对数据表或接口的额外备注或约束说明。
-   `request`: (对象, 可选) - 请求数据中的固定参数，每个字段都是一个键值对。
-   `filter`: (数组, 可选) - 请求数据中的参数变量，每个字段都是一个键值对，键为字段名，值为字段的详细定义，包含如下：
    -   `field`: (字符串) - 请求数据中输入参数变量名。
    -   `format`: (字符串) - 请求数据中输入格式。
    -   `remark`: (字符串) - 对字段值额外备注或约束说明。
-   `orderBys`: (数组, 可选) - 请求数据中的排序定义，每个字段都是一个键值对，键为字段名，值为字段的详细定义，包含如下：
    -   `field`: (字符串) - 响应数据中字段值。
    -   `type`: (字符串) - ASC 或 DESC。
-   `data_label`: (字符串) - 响应数据中的具体业务数组标签（非状态字段），默认值为 ``。
-   `order_label`: (字符串) - 请求数据中的排序标签，默认值为 ``。
-   `token`: (字符串) - 请求数据中的 header Authorization 标签的值，默认值为 ``。
-   `response`: (数组，非状态属性) - 响应数据中的具体业务数组内每个对象，键为字段名，值为字段的详细定义，包含如下。
    -   `meaning`: (字符串) - 字段的中文业务含义。
    -   `is_primary`: (布尔值) - 当字段为主键时，此键设为 `true`。
    -   `values`: (对象, 可选) - 当字段为枚举类型时，此键用于列出所有可选值及其对应的文本说明。

# JSON 参考
{
    "table_name": "员工表",
    "api_name": "/staff/findList",
    "remark": "存储公司所有员工的基本信息",
    "data_label": "data",
    "order_label": "orderBys",
    "token": "token",
    "request": {
      "staffClazz": "STAFF",
      "groupDefaultType": "TEAM"
    },
    "filter": [
        {
            "field": "customerId",
            "format": "YYYYHHMM",
            "remark": "ID"
        }
    ],
    "orderBys": [
        {
            "field": "customerId",
            "type": "ASC"
        }
    ],
    "response": {
        "user_id": {
            "meaning": "员工唯一标识",
            "is_primary": true
        },
        "name": {
            "meaning": "员工姓名"
        },
        "department_id": {
            "meaning": "所属部门ID",
            "remark": "关联到部门表，表示员工所属部门"
        },
        "group_id": {
            "meaning": "班组ID",
            "remark": "关联到班组表，表示员工所属班组"
        },
        "email": {
            "meaning": "电子邮箱",
            "remark": "用于登录和接收通知，必须唯一"
        },
        "phone_number": {
            "meaning": "手机号码"
        },
        "hire_date": {
            "meaning": "入职日期",
        },
        "status": {
            "meaning": "员工状态",
            "values": {
                "1": "在职",
                "0": "离职"
            }
        },
        "created_at": {
            "meaning": "创建时间",
            "remark": "记录创建时的时间戳"
        },
        "updated_at": {
            "meaning": "最后更新时间",
            "remark": "记录每次更新时的时间戳"
        }
    }
}
  """



    # 调用同步方法获取JSON响应
  return dashscope_chat_json(system_prompt, chat.question)

