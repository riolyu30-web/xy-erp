
# e:/tx-erp/erp-service/api/v1/health.py

from fastapi import APIRouter, Request, Depends # 导入FastAPI模块
from dotenv import dotenv_values, set_key # 导入dotenv_values读取环境变量，set_key设置环境变量
import os # 导入os模块用于文件路径操作
from api.v1.dependencies import get_current_user,get_supabase_manager # 导入共享的认证依赖
from api.v1.models import QuestionRequest # 导入请求模型
from services.llm_manager import dashscope_chat_stream # 导入LLM服务
from services.supabase_manager import SupabaseManager # 导入Supabase管理器
from dotenv import load_dotenv
from pydantic import BaseModel
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

@router.get("/env/get")
def get_env():
    """获取环境变量接口，读取.env文件内容"""
    # 定义.env文件的相对路径
    env_path = ".env"
    # 使用dotenv_values读取环境变量文件并解析为字典
    env_config = dotenv_values(env_path)
    # 返回环境变量字典
    return env_config

@router.post("/env/set")
def set_env(env_config: dict):
    """设置环境变量接口，将字典写入.env文件"""
    # 定义.env文件的相对路径
    env_path = ".env"
    # 遍历请求体中的配置项
    for key, value in env_config.items():
        # 使用set_key逐个更新环境变量，若key不存在则创建
        set_key(env_path, key, str(value))
    
    # 重新读取.env文件以返回最新状态
    current_env = dotenv_values(env_path)
    # 返回更新后的环境变量字典
    return current_env

class LoginInput(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(item: LoginInput):
    # 加载.env文件中的环境变量
    load_dotenv()
    if item.username == os.getenv("USER_NAME") and item.password == os.getenv("USER_PASSWORD"):
        return {"token": os.getenv("USER_TOKEN")}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
