# ERP AI 服务

基于 FastAPI 和 DashScope 的流式 AI 问答服务。

## 功能特性

- ✅ 流式响应输出
- ✅ 支持 Qwen-Plus 模型
- ✅ RESTful API 接口
- ✅ 健康检查端点
- ✅ 异步处理

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行服务

```bash
python main.py
```

服务将在 `http://localhost:8001` 启动。

### 测试接口

**方式一：使用 curl**

```bash
curl -X POST http://localhost:8001/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "请介绍一下自己"}'
```

**方式二：使用测试页面**

在浏览器中打开 `test.html` 文件，输入问题即可测试。

## API 文档

### POST /stream

**请求参数：**

```json
{
  "question": "你的问题"
}
```

**响应格式：**

- Content-Type: `text/plain`
- 流式响应，逐步返回 AI 回复内容

### GET /health

**响应示例：**

```json
{
  "status": "ok",
  "message": "Service is running"
}
```

## 部署说明

详见 [服务部署文档](docs/服务部署.md)

## 技术栈

- **FastAPI** - Web 框架
- **Uvicorn** - ASGI 服务器
- **DashScope** - 阿里云 AI 模型服务
- **Pydantic** - 数据验证

## 项目结构

```
erp-service/
├── main.py              # 主程序入口
├── test.py              # DashScope 测试脚本
├── test.html            # 前端测试页面
├── requirements.txt     # Python 依赖
├── .gitignore          # Git 忽略文件
├── README.md           # 项目说明
└── docs/               # 文档目录
    ├── 接口设计.md      # 接口设计文档
    └── 服务部署.md      # 部署指南
```

## 注意事项

1. 需要配置有效的 DashScope API Key
2. 确保服务器有足够的网络带宽支持流式响应
3. 生产环境建议使用 Nginx 进行反向代理
4. 建议使用 systemd 管理服务进程

## 许可证

MIT License

