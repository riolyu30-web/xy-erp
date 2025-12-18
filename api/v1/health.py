
# e:/tx-erp/erp-service/api/v1/health.py

from fastapi import APIRouter, Request, Depends # 导入FastAPI模块
from api.v1.dependencies import get_current_user,get_supabase_manager # 导入共享的认证依赖
from api.v1.models import QuestionRequest # 导入请求模型
from services.llm_manager import dashscope_chat_stream # 导入LLM服务
from services.supabase_manager import SupabaseManager # 导入Supabase管理器

# 创建路由器实例
router = APIRouter(tags=["网络"])

# 健康检查接口
@router.get("/health")
async def health_check():
    """健康检查接口，用于验证服务是否正常运行"""
    try:
        # 测试连接
        if get_supabase_manager().connect():
            return "Service is running"  # 返回服务状态
        else:
            return "Supabase connection failed" # 返回数据库连接失败
    except Exception as e:
        return f"Service error: {str(e)}" # 返回服务错误

# 聊天流式接口
@router.post("/chat/health")
async def chat_check(chat: QuestionRequest, request: Request, current_user: dict = Depends(get_current_user)): # 添加认证依赖
    """聊天接口，流式返回AI响应"""
    system_prompt = "You are a helpful assistant."  # 系统提示词
    # 直接返回StreamingResponse，dashscope_chat_stream已封装好
    return dashscope_chat_stream(request, system_prompt, chat.question)
