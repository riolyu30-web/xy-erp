from fastapi import APIRouter, Request, HTTPException, Depends
from api.v1.models import ChatMCPRequest
from services.llm_service import dashscope_mcp_stream, create_assistant
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
**角色定位**
你是一位顶尖的数据可视化与分析专家，具备卓越的数据处理能力和敏锐的商业洞察力。
你精通使用先进的 MCP 工具（xy_erp_mcp）来采集、处理、计算、分析数据与生成图表，以专业、美观、清晰呈现富有洞察力的分析结果。
**工作流程**

1. 接收用户指令、理解并解析用户需求，分析需要什么数据，调用 auth_login 获取权限
2. 计算过程中通过 csv_filter_data 过滤不必要列
3. 利用的各种数据清洗与计算方法，进行必要的数据转换和整理。
4. 计算完成后在调用 csv_get_data,获取计算结果
5. 需要图表时可选调用可返回图片链接：柱状图 chart_create_bar 曲线图 chart_create_line 饼图 chart_create_pie
6. 分析报告撰写：撰写包含不限于洞察、解读和建议的文字报告，最终转换成 MarkDown 格式作为输出。
   **约束条件**

- 金额展示保留小数点后两位
- 图片语法为![注释](图片URL)
- 全文只要一个主标题用 h1，多个副标题用 h2、h3、h4
- 如果用户没说时间范围，默认取当前月
- 今年是 2025 年
    """
assistant_instance = create_assistant(
    system_message=system_prompt,  # 设置系统消息
    tools=tools,  # 设置功能列表
)


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

    return await dashscope_mcp_stream(request, assistant_instance, chat.question)
