
from fastapi import APIRouter, Request
from api.v1.models import QuestionRequest
from services.llm_service import dashscope_chat_stream
from services.supabase_manager import SupabaseManager
# 创建路由器实例
router = APIRouter(tags=["网络"])
# 健康检查接口


@router.get("/health")
async def health_check():
    """健康检查接口，用于验证服务是否正常运行"""
    try:
        # 测试连接
        if SupabaseManager().connect():
            return "Service is running"  # 返回服务状态
        else:
            return "Supabase connection failed"
    except Exception as e:
        return f"Service error: {str(e)}"

# 聊天流式接口


@router.post("/chat/health")
async def chat_check(chat: QuestionRequest, request: Request):
    """聊天接口，流式返回AI响应"""
    system_prompt = "You are a helpful assistant."  # 系统提示词
    # 直接返回StreamingResponse，dashscope_chat_stream已封装好
    return dashscope_chat_stream(request, system_prompt, chat.question)
