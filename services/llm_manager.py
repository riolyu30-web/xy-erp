
import json
# 导入环境变量处理库
import os
from pickletools import read_bytes4
import re
from datetime import datetime
from http import HTTPStatus
import requests  # 导入requests库
import json  # 导入json库
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse  # 导入流式响应
from sse_starlette.sse import EventSourceResponse
from starlette.concurrency import iterate_in_threadpool

import dashscope  # 导入dashscope SDK
from dashscope import Generation
from dashscope import ImageSynthesis

# 导入R模块
from services.R import log
# 导入qwen_agent
from qwen_agent.agents import Assistant


# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取DASHSCOPE_API_KEY
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

    # 构建消息列表
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt+",please response in json format"}
    ]
    # 调用生成接口
    response = Generation.call(
        model=model,
        messages=messages,
        enable_thinking=enable_thinking,
        result_format='message',
        response_format={'type': 'json_object'}
    )
    try:
        # 尝试解析JSON字符串
        json_string = response.output.choices[0].message.content
        json_data = json.loads(json_string)
        return json_data
    except json.JSONDecodeError:
        # 解析失败返回None
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
    # 记录请求日志
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
        # 发生异常返回空字符串
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

    # 定义系统提示
    system_prompt = f"""你是一个智能助手，你可以调用以下工具来回答用户的问题，工具的参数必须从用户的问题中提取，不能自己编造参数值：
    {tools_string}
    Response in NORMAL_MODE."""
    # 构建消息列表
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    # 调用生成接口
    response = Generation.call(
        model=model,
        messages=messages,
        result_format="message"
    )
    # 获取响应内容
    json_string = response.output.choices[0].message.content
    # 解析文本内容
    json_data = _parse_text(json_string)
    return json_data


def _parse_text(text):
    # 如果文本为空，则返回None
    if text is None:
        return None
    # 定义工具调用正则表达式
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    # 使用正则表达式查找匹配的内容
    tool_call_match = re.search(tool_call_pattern, text, re.DOTALL)
    # 提取匹配的内容，如果没有匹配到则返回空字符串
    tool_call = tool_call_match.group(1).strip() if tool_call_match else ""
    # 解析tool_call为JSON格式
    try:
        tool_call_json = json.loads(tool_call)
    except json.JSONDecodeError:
        # 解析失败则返回原始文本
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
    # 将字典转换为JSON字符串
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
    # 获取响应内容
    json_string = response.output.choices[0].message.content
    # 如果响应内容是意图字典的键，则返回对应的值
    if json_string in intent_dict.keys():
        return intent_dict[json_string]
    # 否则返回None
    return None


def create_assistant(system_message, tools: list[dict], model: str = "qwen-plus-latest"):
    # LLM 配置
    llm_cfg = {
        "model": model,
        "model_server": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
    }
    # 创建Assistant实例
    assistant = Assistant(
        llm=llm_cfg,  # 设置语言模型配置
        system_message=system_message,  # 设置系统消息
        function_list=tools,  # 设置功能列表
    )
    return assistant  # 返回Assistant实例


async def dashscope_mcp_stream(request: Request, bot: Assistant, user_prompt: str) -> StreamingResponse:
    """
    调用大模型进行MCP流式传输
    Args:
        request: FastAPI请求对象
        system_prompt: 系统提示词
        tools: 系统工具列表
        user_prompt: 用户提示词
        model: 使用的模型名称
    Returns:
        StreamingResponse: 大模型流式传输结果
    """
    # 消息列表
    messages = [{"role": "user", "content": user_prompt}]

    # 流式响应
    async def stream_generator():
        # 运行助手
        # 使用iterate_in_threadpool来异步迭代同步生成器
        bot_response = ""  # 记录已返回的响应内容
        is_tool_call = False  # 标记是否正在进行工具调用
        tool_call_info = {}  # 存储工具调用信息
        processed_len = 0 # 记录已处理的消息数量
        import asyncio

        async for response_chunk in iterate_in_threadpool(bot.run(messages)):
            if await request.is_disconnected():
                break
            
            # 遍历所有未处理的消息以及当前正在处理的消息（最后一条）
            for i in range(processed_len, len(response_chunk)):
                new_response = response_chunk[i]
                
                # 如果处理到了新的消息，重置bot_response
                if i > processed_len:
                    bot_response = ""
                    processed_len = i
                
                # 检查是否有函数调用
                if "function_call" in new_response:
                    is_tool_call = True
                    tool_call_info = new_response["function_call"]
                    # 不返回增量部分，等待完整的函数调用
                    continue
                    
                # 如果之前有函数调用，现在没有，说明函数调用完成
                elif "function_call" not in new_response and is_tool_call:
                    is_tool_call = False
                    # 返回完整的函数调用和结果
                    completed_data = [
                        {"role": "assistant", "content": "", "function_call": tool_call_info},
                        {"role": "function", "content": new_response.get("content", ""), "name": tool_call_info.get("name", "")}
                    ]
                    yield f"data: {json.dumps(completed_data, ensure_ascii=False)}\n\n"
                    # 发送完函数调用后，稍微暂停一下，避免消息发送过快
                    await asyncio.sleep(0.05)
                    
                # 处理普通的助手响应内容
                elif new_response.get("role") == "assistant" and "content" in new_response:
                    # 只返回新增的内容部分
                    incremental_content = new_response["content"][len(bot_response):]
                    if incremental_content:  # 只有当有新内容时才返回
                        bot_response += incremental_content
                        yield f"data: {json.dumps([{'role': 'assistant', 'content': incremental_content}], ensure_ascii=False)}\n\n"
                        # 如果不是最后一条消息，或者是最后一条消息但内容较多，可以适当延时
                        # 这里主要为了防止多条消息瞬间发送导致前端渲染问题
                        if i < len(response_chunk) - 1:
                            await asyncio.sleep(0.05)


        
    # 返回StreamingResponse
    return StreamingResponse(stream_generator(), media_type="text/event-stream")


def dashscope_text2image(prompt: str, model: str = "wan2.6-t2i",size: str = "1920*1080"):
    """
    调用大模型进行图片生成
    Args:
        prompt: 图片描述提示词
        model: 使用的模型名称
        size: 图片尺寸 1920*1080 是观看电影的黄金标准，3840*2160 (4K) 能提供最佳体验
    Returns:
        list: 图片URL列表
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")  # 获取DASHSCOPE_API_KEY
    # 构建请求数据
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"  # 设置请求URL
    headers = {
        "Content-Type": "application/json",  # 设置Content-Type
        "Authorization": f"Bearer {api_key}"  # 设置Authorization
    }
    payload = {
        "model": model,  # 设置模型
        "input": {
            "messages": [
                {
                    "role": "user",  # 设置角色
                    "content": [
                        {
                            "text": prompt.strip()  # 设置提示词
                        }
                    ]
                }
            ]
        },
        "parameters": {
            "prompt_extend": True,  # 开启提示词扩展
            "watermark": False,  # 关闭水印
            "n": 1,  # 生成数量
            "negative_prompt": "",  # 负面提示词
            "size": size  # 图片尺寸
        }
    }

    # 发送请求
    response = requests.post(url, headers=headers, json=payload)  # 发送POST请求

    # 获取响应内容
    if response.status_code == HTTPStatus.OK:  # 检查响应状态码
        try:  # 尝试解析响应数据
            response_json = response.json()  # 解析JSON响应
            output = response_json.get("output", {})  # 获取output对象
            choices = output.get("choices", [])  # 获取choices列表
            if choices:  # 如果choices不为空
                message = choices[0].get("message", {})  # 获取message对象
                content = message.get("content", [])  # 获取content列表
                if content:  # 如果content不为空
                    return content[0].get("image")  # 返回图片URL
        except Exception as e:  # 捕获异常
            log(f"解析图片响应失败: {e}")  # 记录错误日志
            return None  # 返回None
    else:
        raise HTTPException(status_code=response.status_code, detail="Image synthesis failed")


def dashscope_image2image(prompt: str, images: list[str], model: str = "wan2.6-image", size: str = "1280*1280"):
    """
    调用大模型进行图生图
    Args:
        prompt: 图片描述提示词
        images: 参考图片URL列表
        model: 使用的模型名称
        size: 生成图片尺寸
    Returns:
        str: 图片URL
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")  # 获取DASHSCOPE_API_KEY
    # 构建请求数据
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"  # 设置请求URL
    headers = {
        "Content-Type": "application/json",  # 设置Content-Type
        "Authorization": f"Bearer {api_key}"  # 设置Authorization
    }

    # 构建消息内容
    content_list = [{"text": prompt}]  # 添加文本提示词
    for image_url in images:
        content_list.append({"image": image_url})  # 添加参考图片URL

    payload = {
        "model": model,  # 设置模型
        "input": {
            "messages": [
                {
                    "role": "user",  # 设置角色
                    "content": content_list
                }
            ]
        },
        "parameters": {
            "prompt_extend": True,  # 开启提示词扩展
            "watermark": False,  # 关闭水印
            "n": 1,  # 生成数量
            "enable_interleave": False,  # 关闭图文混排
            "size": size  # 图片尺寸
        }
    }

    # 发送请求
    response = requests.post(url, headers=headers, json=payload)  # 发送POST请求

    # 获取响应内容
    if response.status_code == HTTPStatus.OK:  # 检查响应状态码
        try:  # 尝试解析响应数据
            response_json = response.json()  # 解析JSON响应
            output = response_json.get("output", {})  # 获取output对象
            choices = output.get("choices", [])  # 获取choices列表
            if choices:  # 如果choices不为空
                message = choices[0].get("message", {})  # 获取message对象
                content = message.get("content", [])  # 获取content列表
                if content:  # 如果content不为空
                    return content[0].get("image")  # 返回图片URL
        except Exception as e:  # 捕获异常
            log(f"解析图生图响应失败: {e}")  # 记录错误日志
            return None  # 返回None
    else:
        raise HTTPException(status_code=response.status_code, detail="Image synthesis failed")

def dashscope_image2video(prompt: str, img_url: str, audio_url: str = None, model: str = "wan2.6-i2v", resolution: str = "720P", duration: int = 10):
    """
    调用大模型进行图生视频
    Args:
        prompt: 视频描述提示词
        img_url: 参考图片URL
        audio_url: 音频URL (可选)
        model: 使用的模型名称
        resolution: 视频分辨率
        duration: 视频时长 (秒)
    Returns:
        str: 任务ID (task_id)
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")  # 获取DASHSCOPE_API_KEY
    # 构建请求数据
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"  # 设置请求URL
    headers = {
        "Content-Type": "application/json",  # 设置Content-Type
        "Authorization": f"Bearer {api_key}",  # 设置Authorization
        "X-DashScope-Async": "enable"  # 开启异步处理
    }

    input_data = {
        "prompt": prompt,  # 设置提示词
        "img_url": img_url  # 设置参考图片URL
    }
    if audio_url:
        input_data["audio_url"] = audio_url  # 如果有音频URL，则设置音频URL

    payload = {
        "model": model,  # 设置模型
        "input": input_data,
        "parameters": {
            "resolution": resolution,  # 设置分辨率
            "prompt_extend": True,  # 开启提示词扩展
            "duration": duration,  # 设置时长
            "audio": True if audio_url else False,  # 如果有音频URL，则开启音频生成
            "shot_type": "multi"  # 设置镜头类型
        }
    }

    # 发送请求
    response = requests.post(url, headers=headers, json=payload)  # 发送POST请求

    # 获取响应内容
    if response.status_code == HTTPStatus.OK:  # 检查响应状态码
        try:  # 尝试解析响应数据
            response_json = response.json()  # 解析JSON响应
            output = response_json.get("output", {})  # 获取output对象
            task_id = output.get("task_id")  # 获取task_id
            if task_id:  # 如果task_id不为空
                return task_id  # 返回task_id
        except Exception as e:  # 捕获异常
            log(f"解析图生视频响应失败: {e}")  # 记录错误日志
            return None  # 返回None
    else:
        log(f"图生视频请求失败: {response.text}")  # 记录错误日志
        raise HTTPException(status_code=response.status_code, detail="Video synthesis failed")

def dashscope_video2video(prompt: str, reference_video_urls: list[str], model: str = "wan2.6-r2v", size: str = "1280*720", duration: int = 10):
    """
    调用大模型进行视频生视频
    Args:
        prompt: 视频描述提示词
        reference_video_urls: 参考视频URL列表
        model: 使用的模型名称
        size: 视频分辨率
        duration: 视频时长 (秒)
    Returns:
        str: 任务ID (task_id)
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")  # 获取DASHSCOPE_API_KEY
    # 构建请求数据
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"  # 设置请求URL
    headers = {
        "Content-Type": "application/json",  # 设置Content-Type
        "Authorization": f"Bearer {api_key}",  # 设置Authorization
        "X-DashScope-Async": "enable"  # 开启异步处理
    }

    input_data = {
        "prompt": prompt,  # 设置提示词
        "reference_video_urls": reference_video_urls  # 设置参考视频URL列表
    }

    payload = {
        "model": model,  # 设置模型
        "input": input_data,
        "parameters": {
            "size": size,  # 设置分辨率
            "duration": duration,  # 设置时长
            "audio": True,  # 开启音频生成
            "shot_type": "multi"  # 设置镜头类型
        }
    }

    # 发送请求
    response = requests.post(url, headers=headers, json=payload)  # 发送POST请求

    # 获取响应内容
    if response.status_code == HTTPStatus.OK:  # 检查响应状态码
        try:  # 尝试解析响应数据
            response_json = response.json()  # 解析JSON响应
            output = response_json.get("output", {})  # 获取output对象
            task_id = output.get("task_id")  # 获取task_id
            if task_id:  # 如果task_id不为空
                return task_id  # 返回task_id
        except Exception as e:  # 捕获异常
            log(f"解析视频生视频响应失败: {e}")  # 记录错误日志
            return None  # 返回None
    else:
        log(f"视频生视频请求失败: {response.text}")  # 记录错误日志
        raise HTTPException(status_code=response.status_code, detail="Video synthesis failed")

def dashscope_task_status(task_id: str):
    """
    查询DashScope异步任务状态
    Args:
        task_id: 任务ID
    Returns:
        dict: 包含任务状态和结果的字典，如果任务成功完成，返回视频URL
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")  # 获取DASHSCOPE_API_KEY
    # 构建请求数据
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"  # 设置请求URL
    headers = {
        "Authorization": f"Bearer {api_key}"  # 设置Authorization
    }

    # 发送请求
    response = requests.get(url, headers=headers)  # 发送GET请求

    # 获取响应内容
    if response.status_code == HTTPStatus.OK:  # 检查响应状态码
        try:  # 尝试解析响应数据
            response_json = response.json()  # 解析JSON响应
            output = response_json.get("output", {})  # 获取output对象
            task_status = output.get("task_status")  # 获取任务状态
            
            if task_status == "SUCCEEDED":  # 如果任务成功
                video_url = output.get("video_url")  # 获取视频URL
                if video_url:  # 如果视频URL存在
                    return video_url  # 返回视频URL
            elif task_status == "FAILED":  # 如果任务失败
                 log(f"任务失败: {output}") # 记录失败信息
                 return None # 返回None
            
            # 如果任务仍在进行中（PENDING或RUNNING），返回状态
            return None
            
        except Exception as e:  # 捕获异常
            log(f"解析任务状态响应失败: {e}")  # 记录错误日志
            return None  # 返回None
    else:
        log(f"查询任务状态失败: {response.text}")  # 记录错误日志
        raise HTTPException(status_code=response.status_code, detail="Query task status failed")