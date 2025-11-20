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
system_prompt = """你是获取令牌助手
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
