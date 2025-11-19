# 导入FastAPI框架和相关模块
from fastapi import FastAPI
# 导入CORS中间件用于处理跨域请求
from fastapi.middleware.cors import CORSMiddleware
# 导入认证路由器
from api.v1 import intent, auth, health, chat

import uvicorn  # 导入ASGI服务器

app = FastAPI()

# 添加CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    # 允许的源地址列表
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    # 允许携带凭证
    allow_credentials=True,
    # 允许的HTTP方法
    allow_methods=["*"],
    # 允许的请求头
    allow_headers=["*"],
)


app.include_router(health.router, prefix="/api/v1")
app.include_router(intent.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")


# 主函数
if __name__ == "__main__":
    # 启动uvicorn服务器
    uvicorn.run(
        "main:app",  # ✅ 使用导入字符串格式 "模块名:应用变量名"
        host="0.0.0.0",  # 监听所有网络接口
        port=8000,  # 监听端口8001
        log_level="info",  # 日志级别
        reload=True,  # 自动重新加载
    )
