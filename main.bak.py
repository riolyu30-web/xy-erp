import os  # 导入操作系统模块
from http import HTTPStatus  # 导入HTTP状态码
from fastapi import FastAPI  # 导入FastAPI框架
from fastapi.middleware.cors import CORSMiddleware  # 导入CORS中间件
from fastapi.responses import StreamingResponse  # 导入流式响应
from pydantic import BaseModel  # 导入数据验证模型
import dashscope  # 导入dashscope SDK
from dashscope import Generation  # 导入Generation模块
import uvicorn  # 导入ASGI服务器

# 配置API Key
dashscope.api_key = "sk-65c47bda48984792b84cb3f1cac3f723"

# 创建FastAPI应用实例
app = FastAPI(title="ERP AI Service", version="1.0.0")

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,  # 添加CORS中间件
    allow_origins=["*"],  # 允许所有源访问（生产环境建议指定具体域名）
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)


# 定义请求模型
class QuestionRequest(BaseModel):
    question: str  # 用户提问的问题


# 定义流式生成器函数
async def generate_stream(question: str):
    """异步生成器函数，用于流式输出AI响应"""
    # 构建消息列表
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},  # 系统角色设定
        {"role": "user", "content": question},  # 用户提问
    ]

    try:
        # 调用dashscope的Generation.call进行流式请求
        responses = Generation.call(
            model="qwen-plus",  # 使用qwen-plus模型
            messages=messages,  # 传入消息列表
            result_format="message",  # 返回格式为消息
            stream=True,  # 开启流式输出
            incremental_output=True,  # 开启增量输出以提升性能
        )

        # 遍历流式响应
        for resp in responses:
            if resp.status_code == HTTPStatus.OK:  # 检查响应状态码
                content = resp.output.choices[0].message.content  # 获取AI回复内容
                yield content  # 使用yield返回增量内容

                # 检查是否是最后一个数据包
                if resp.output.choices[0].finish_reason == "stop":
                    break  # 结束流式输出
            else:
                # 处理错误情况
                error_msg = f"\n错误: code={resp.code}, message={resp.message}"  # 构建错误信息
                yield error_msg  # 返回错误信息
                break  # 终止生成器

    except Exception as e:  # 捕获异常
        yield f"\n发生错误: {str(e)}"  # 返回异常信息


# 创建POST接口
@app.post("/stream")
async def stream_response(request: QuestionRequest):
    """流式响应接口，接收问题并返回AI的流式回复"""
    return StreamingResponse(
        generate_stream(request.question),  # 调用生成器函数
        media_type="text/plain",  # 设置响应内容类型为纯文本
    )


# 健康检查接口
@app.get("/health")
async def health_check():
    """健康检查接口，用于验证服务是否正常运行"""
    return {"status": "ok", "message": "Service is running"}  # 返回服务状态


# 主函数
if __name__ == "__main__":
    # 启动uvicorn服务器
    uvicorn.run(
        app,  # FastAPI应用实例
        host="0.0.0.0",  # 监听所有网络接口
        port=8001,  # 监听端口8001
        log_level="info",  # 日志级别
    )
