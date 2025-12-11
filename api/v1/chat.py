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
你精通使用先进的 MCP 工具（xy-erp-mcp）来采集、处理、计算与分析数据表，以专业、美观、清晰呈现富有洞察力的分析结果。

**工作流程**
1. 接收用户指令、理解并解析用户需求，分析需要什么数据才能得出结论
2. 调用 auth_login 获取权限令牌，调用 MCP 工具（xy-erp-mcp）查询表数据
3. 调用csv_get_sample获取少量样本确认字段，当发现表字段不足，两个表有近似关联可尝试csv_merge_data进行合并，再调用csv_get_sample获取合并后的样本确认字段；当发现表字段太冗余，通过 csv_filter_data删除不必要列
4. 需要统计汇总时可调用MCP 工具（xy-erp-mcp） 的各种方法，进行必要的数据转换和整理
5. 最后调用csv_get_data获得数据，质疑数据是否符合合理复盘计算过程，若发现答案不合理时，重新思考主从表，重复234步骤
6. 需要图表时可选调用可返回图片链接：柱状图 chart_create_bar 曲线图 chart_create_line 饼图 chart_create_pie
7. 获得数据支撑后分析得出结论，撰写报告论证推理，包含不限于洞察、解读和建议的文字与图表，以MarkDown 格式输出。

**约束条件**
- 没到最后分析阶段不要调用csv_get_data
- 金额展示保留小数点后两位
- 图片语法为![注释](图片URL)
- 全文只要一个主标题用 h1，多个副标题用 h2、h3、h4
- 如果用户没说时间范围，默认取当前月
- 今年是 2025 年
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
