
from fastapi import APIRouter, Request, HTTPException
from api.v1.models import QuestionRequest, SignUpRequest, SignInRequest, SignOutRequest
from services.supabase_manager import SupabaseManager
# 创建路由器实例
router = APIRouter(tags=["权限"])


@router.post("/auth/signup")
async def sign_up(request: SignUpRequest):
    """
    用户注册接口

    Args:
        request: 注册请求，包含 username 和 password

    Returns:
        注册成功返回成功信息，失败抛出异常
    """
    # 创建 Supabase 管理器实例
    manager = SupabaseManager()

    # 调用注册方法，使用 username 作为唯一标识
    result = manager.sign_up(
        {"username": request.username, "password": request.password},
        unique=["username"]
    )

    # 检查注册结果
    if result:
        return {
            "success": True,
            "message": "注册成功"
        }
    else:
        raise HTTPException(status_code=400, detail="注册失败，请检查用户名是否已存在")


@router.post("/auth/signin")
async def sign_in(request: SignInRequest):
    """
    用户登录接口

    Args:
        request: 登录请求，包含 username 和 password

    Returns:
        登录成功返回 token，失败抛出异常
    """
    # 创建 Supabase 管理器实例
    manager = SupabaseManager()

    # 调用登录方法，传入用户名和密码
    token = manager.sign_in({
        "username": request.username,
        "password": request.password
    })

    # 检查登录结果
    if token:
        return {
            "success": True,
            "message": "登录成功",
            "token": token,
        }
    else:
        raise HTTPException(status_code=401, detail="登录失败，用户名或密码错误")


@router.post("/auth/signout")
async def sign_out(request: SignOutRequest):
    """
    用户注销接口

    Args:
        request: 注销请求，包含 token

    Returns:
        注销成功返回成功信息，失败抛出异常
    """
    # 创建 Supabase 管理器实例
    manager = SupabaseManager()

    # 调用注销方法，传入 token
    result = manager.sign_out(request.token)

    # 检查注销结果
    if result:
        return {
            "success": True,
            "message": "注销成功"
        }
    else:
        raise HTTPException(status_code=400, detail="注销失败，token 无效或已过期")


@router.get("/auth/verify/{token}")
def verify_token(token: str):
    """
    验证 token 是否有效

    Args:
        token: 用户令牌

    Returns:
        返回 token 的有效性和用户信息
    """
    # 创建 Supabase 管理器实例
    manager = SupabaseManager()
    # 连接数据库
    if not manager.connect():
        raise HTTPException(status_code=500, detail="数据库连接失败")

    # 验证 token
    is_valid, user = manager.verify_token(token)

    # 如果 token 有效，获取用户信息
    if is_valid:
        if user:
            return {
                "success": True,
                "message": "Token 有效",
                "valid": True,
                "user": user
            }

    # token 无效或已过期
    return {
        "success": False,
        "message": "Token 无效或已过期",
        "valid": False
    }
