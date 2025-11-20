# e:/tx-erp/erp-service/api/v1/dependencies.py

from fastapi import Depends, HTTPException, status # 导入FastAPI的依赖注入和异常处理模块
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # 导入HTTP Bearer认证模块
from services.supabase_manager import SupabaseManager # 导入Supabase管理器

# 创建HTTPBearer实例，用于从请求头中提取Token
security = HTTPBearer()

# 全局SupabaseManager实例
manager = None

def get_supabase_manager():
    """依赖项：获取SupabaseManager的单例"""
    global manager # 声明 manager 是全局变量
    if manager is None:
        manager = SupabaseManager() # 如果实例不存在，则创建
    return manager # 返回实例

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    依赖项：从Authorization头中获取并验证Bearer token
    """
    supabase = get_supabase_manager() # 获取SupabaseManager实例
    token = credentials.credentials # 提取token
    is_valid, user_info = supabase.verify_token(token) # 验证token

    if not is_valid:
        # 如果token无效，抛出401异常
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_info # 返回用户信息