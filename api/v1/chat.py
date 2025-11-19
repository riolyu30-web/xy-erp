from fastapi import APIRouter, Request, HTTPException
from api.v1.models import ChatMCPRequest
from services.supabase_manager import SupabaseManager
from services.llm_service import dashscope_mcp_stream, create_assistant

# 创建路由器实例
router = APIRouter(tags=["聊天"])
manager = SupabaseManager()

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
async def chat_mcp(chat: ChatMCPRequest, request: Request):
    """
    聊天模型
    Args:
        chat: ChatMCPRequest 聊天模型
    Returns:
        response: 聊天响应
    """
    # 从请求中获取访问令牌
    # 验证 token
    is_valid, _ = manager.verify_token(chat.token)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Token 无效或已过期")
    return await dashscope_mcp_stream(request, assistant_instance, chat.question)
