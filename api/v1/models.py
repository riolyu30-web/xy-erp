# 导入Pydantic用于数据验证
from pydantic import BaseModel
from typing import Optional, List


class ChatIntentRequest(BaseModel):
    """聊天意图模型"""
    question: str  # 问题
    memory: str  # 记忆


# 定义请求模型
class QuestionRequest(BaseModel):
    question: str  # 用户提问的问题

class SignUpRequest(BaseModel):
    username: str
    password: str

class SignInRequest(BaseModel):
    username: str
    password: str

class SignOutRequest(BaseModel):
    token: str