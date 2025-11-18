# 导入Pydantic用于数据验证
from pydantic import BaseModel
from typing import Optional, List


class AuthRequest(BaseModel):
    token: str


class ChatIntentRequest(AuthRequest):

    """聊天意图模型"""
    question: str  # 问题
    memory: str  # 记忆


# 定义请求模型
class QuestionRequest(AuthRequest):
    question: str  # 用户提问的问题


class SignUpRequest(BaseModel):
    username: str
    password: str


class SignInRequest(BaseModel):
    username: str
    password: str


class SignOutRequest(BaseModel):
    token: str
