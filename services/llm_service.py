
import json
# 导入环境变量处理库
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi import Request
from fastapi.responses import StreamingResponse  # 导入流式响应
from dashscope import Generation
from http import HTTPStatus
import dashscope  # 导入dashscope SDK
import json
import os
import re
from sse_starlette.sse import EventSourceResponse
from services.R import log

# 加载环境变量

# 加载环境变量
load_dotenv()

# 配置API Key
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def dashscope_chat_json(system_prompt: str, user_prompt: str, model: str = "qwen-flash", enable_thinking: bool = False) -> str:
    """
    大语言模型请求方法，返回JSON格式的响应

    Args:
        system_prompt (str): 系统提示，描述模型的行为和限制
        user_prompt (str): 用户输入的文本内容
        model (str, optional): 模型名称，默认值为"qwen-flash"
        enable_thinking (bool, optional): 是否开启深度思考，默认值为False
    Returns:
        str: 模型返回的JSON格式文本内容
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt+",please response in json format"}
    ]
    response = Generation.call(
        model=model,
        messages=messages,
        enable_thinking=enable_thinking,
        result_format='message',
        response_format={'type': 'json_object'}
    )
    try:
        json_string = response.output.choices[0].message.content
        json_data = json.loads(json_string)
        return json_data
    except json.JSONDecodeError:
        return None


def dashscope_chat_block(system_prompt: str, user_prompt: str, model: str = "qwen-flash", enable_thinking: bool = False) -> str:
    """
    大语言模型请求方法，返回普通文本

    Args:
        system_prompt (str): 系统提示，描述模型的行为和限制
        user_prompt (str): 用户输入的文本内容
        model (str, optional): 模型名称，默认值为"qwen-flash"
        enable_thinking (bool, optional): 是否开启深度思考，默认值为False

    Returns:
        str: 模型返回的文本内容
    """
    # 构建消息列表
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    log(f"dashscope_chat_block: {messages}")
    # 调用大模型API（非流式）
    response = Generation.call(
        model=model,
        messages=messages,
        enable_thinking=enable_thinking,
        result_format='message',
        stream=False,  # 开启流式传输
    )

    try:
        # 提取返回的文本内容
        text_content = response.output.choices[0].message.content
        return text_content
    except Exception as e:
        return ""


def dashscope_chat_stream(request: Request, system_prompt: str, user_prompt: str, model: str = "qwen-flash", enable_thinking: bool = False) -> StreamingResponse:
    """
    大语言模型流式请求方法，返回StreamingResponse

    Args:
        request (Request): FastAPI请求对象，用于检查连接状态
        system_prompt (str): 系统提示词
        user_prompt (str): 用户输入的问题
        model (str, optional): 模型名称，默认值为"qwen-flash"
        enable_thinking (bool, optional): 是否开启深度思考，默认值为False

    Returns:
        StreamingResponse: FastAPI流式响应对象
    """
    # 定义内部生成器函数，用于生成流式内容
    async def _stream_generator():
        try:
            # 构建消息列表
            if system_prompt and user_prompt:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                # 调用dashscope API获取流式响应
                responses = Generation.call(
                    # 可按需更换为其它深度思考模型
                    model=model or "qwen-plus-2025-04-28",
                    messages=messages,
                    result_format="message",  # Qwen3开源版模型只支持设定为"message"；为了更好的体验，其它模型也推荐您优先设定为"message"
                    # 开启深度思考，该参数对qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ、DeepSeek-R1 模型无效
                    enable_thinking=enable_thinking,
                    stream=True,  # 开启流式传输
                    incremental_output=True,  # Qwen3开源版模型只支持 true；为了更好的体验，其它模型也推荐您优先设定为 true
                )

                # 遍历流式响应
                for resp in responses:
                    # 检查客户端是否断开连接
                    if await request.is_disconnected():
                        break
                    # 检查响应状态码
                    if resp.status_code == HTTPStatus.OK:
                        print(resp)
                        # 获取AI回复内容
                        content = resp.output.choices[0].message.content
                        yield content  # 使用yield返回增量内容

                        # 检查是否是最后一个数据包
                        if resp.output.choices[0].finish_reason == "stop":
                            break  # 结束流式输出
                    else:
                        # 处理错误情况
                        # 构建错误信息
                        error_msg = f"\n错误: code={resp.code}, message={resp.message}"
                        yield error_msg  # 返回错误信息
                        break  # 终止生成器

        except Exception as e:  # 捕获异常
            yield f"\n发生错误: {str(e)}"  # 返回异常信息

    # 返回StreamingResponse对象，包装生成器函数
    return StreamingResponse(
        _stream_generator(),
        media_type="text/plain; charset=utf-8"  # 设置响应内容类型
    )


def dashscope_chat_tool(tools_string: str, user_prompt: str, model: str = "tongyi-intent-detect-v3") -> dict:

    system_prompt = f"""你是一个智能助手，你可以调用以下工具来回答用户的问题，工具的参数必须从用户的问题中提取，不能自己编造参数值：
    {tools_string}
    Response in NORMAL_MODE."""
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    response = Generation.call(
        model=model,
        messages=messages,
        result_format="message"
    )
    json_string = response.output.choices[0].message.content
    json_data = _parse_text(json_string)
    return json_data


def _parse_text(text):
    if text is None:
        return None
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    # 使用正则表达式查找匹配的内容
    tool_call_match = re.search(tool_call_pattern, text, re.DOTALL)
    # 提取匹配的内容，如果没有匹配到则返回空字符串
    tool_call = tool_call_match.group(1).strip() if tool_call_match else ""
    # 解析tool_call为JSON格式
    try:
        tool_call_json = json.loads(tool_call)
    except json.JSONDecodeError:
        tool_call_json = text
    return tool_call_json


def dashscope_chat_intent(intent_list: list[str], user_prompt: str, model: str = "tongyi-intent-detect-v3") -> dict:
    """
    将意图列表转换为字典格式并调用大模型进行意图识别
    Args:
        intent_list: 意图字符串列表 不要超26个
        model: 使用的模型名称
    Returns:
        dict: 意图识别结果字典
    """
    # 将intent_list转换为字典格式
    intent_dict = {}
    # 生成字母键值对应
    for i, intent in enumerate(intent_list):
        # 使用A-Z作为键
        key = chr(ord('A') + i)
        intent_dict[key] = intent
    intent_string = json.dumps(intent_dict, ensure_ascii=False)
    # 系统提示词
    system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. 
You should choose one tag from the tag list:
{intent_string}
Just reply with the chosen tag."""
    # 构建消息列表
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    # 调用大模型API
    response = Generation.call(
        model=model,
        messages=messages,
        result_format="message"
    )
    json_string = response.output.choices[0].message.content
    if json_string in intent_dict.keys():
        return intent_dict[json_string]
    return None
