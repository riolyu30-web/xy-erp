import os
from qwen_agent.agents import Assistant

# LLM 配置
llm_cfg = {
    "model": "qwen-plus-latest",
    "model_server": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    "api_key": "sk-65c47bda48984792b84cb3f1cac3f723",
}

# 系统消息
system = "你是会天气查询、地图查询、网页部署的助手"

# 工具列表
tools = [
    {
        "mcpServers": {
            "tavily-mcp": {
                "type": "sse",
                "url": "https://mcp.api-inference.modelscope.net/735f6649ac554b/sse"
            },
            "xy-erp-mcp": {
                "url": "https://mcp.riohome.top/sse"
            }
        }
    }
]

# 创建助手实例
bot = Assistant(
    llm=llm_cfg,
    name="助手",
    description="天气查询、地图查询、网页部署",
    system_message=system,
    function_list=tools,
)

messages = []

while True:
    query = input("\nuser question: ")
    if not query.strip():
        print("user question cannot be empty！")
        continue
    messages.append({"role": "user", "content": query})
    bot_response = ""
    is_tool_call = False
    tool_call_info = {}
    for response_chunk in bot.run(messages):
        new_response = response_chunk[-1]
        if "function_call" in new_response:
            is_tool_call = True
            tool_call_info = new_response["function_call"]
        elif "function_call" not in new_response and is_tool_call:
            is_tool_call = False
            print("\n" + "=" * 20)
            print("工具调用信息：", tool_call_info)
            print("工具调用结果：", new_response)
            print("=" * 20)
        elif new_response.get("role") == "assistant" and "content" in new_response:
            incremental_content = new_response["content"][len(bot_response):]
            print(incremental_content, end="", flush=True)
            bot_response += incremental_content
    messages.extend(response_chunk)
