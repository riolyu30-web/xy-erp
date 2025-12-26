from fastmcp import FastMCP
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
import time

auth_mcp = FastMCP(name="auth")


@auth_mcp.tool()
def login() -> str:
    """
    登录ERP系统,获取访问权限
    Args:
        无需参数
    Returns:
        access_token: 访问令牌字符串
    Raises:
        Exception: 当登录失败时抛出异常
    """
    # return local_login()
    return auth_login()


def local_login() -> str:
    # 获取当前时间戳（浮点数形式）
    timestamp = time.time()

    # 将时间戳转换为字符串并编码为字节
    timestamp_str = str(timestamp).encode('utf-8')

    # 生成MD5哈希值
    md5_hash = hashlib.md5(timestamp_str).hexdigest()
    return md5_hash


def auth_login() -> str:

    # 加载环境变量
    load_dotenv()

    # 从环境变量获取配置
    BASE_URL = os.getenv("BASE_URL", "http://192.168.0.156:28002")

    # 构建OAuth2令牌请求URL
    url = f"{BASE_URL}/oauth2/token"
    print(url)

    # 设置请求参数
    params = {
        "grant_type": "password",  # OAuth2密码授权类型
        "client_id": "2caf3cb6216111eea71b49e0880a97d9",  # 客户端ID
        "username": "lutao",  # 用户名
        "password": "123456"   # 密码
    }

    try:
        # 发送POST请求获取令牌
        response = requests.get(url, params=params, timeout=30)
        # 检查HTTP状态码
        response.raise_for_status()

        # 解析JSON响应
        response_data = response.json()

        # 检查业务逻辑是否成功
        if response_data.get("code") == 0 and response_data.get("msg") == "SUCCESS":
            # 返回访问令牌
            access_token = response_data["data"]["access_token"]
            return access_token
        else:
            # 登录失败，抛出异常
            error_msg = response_data.get("msg", "未知错误")
            raise Exception(f"登录失败: {error_msg}")

    except requests.exceptions.RequestException as e:
        # 网络请求异常
        raise Exception(f"网络请求失败: {str(e)}")
    except json.JSONDecodeError as e:
        # JSON解析异常
        raise Exception(f"响应数据解析失败: {str(e)}")
    except KeyError as e:
        # 数据结构异常
        raise Exception(f"响应数据结构异常: {str(e)}")
