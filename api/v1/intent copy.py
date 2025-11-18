import copy  # 导入 copy 模块，用于深度复制对象
from fastapi import APIRouter, HTTPException, Request
from dashscope import Application
from dashscope import Generation
from http import HTTPStatus
import json
import os
from datetime import datetime
from api.v1.models import ChatIntentRequest
from services.llm_service import dashscope_chat_block, dashscope_chat_stream, dashscope_chat_tool, dashscope_chat_intent
from services.R import log

# 创建路由器实例
router = APIRouter(tags=["意图识别"])


tools = {
    "天气": {
        "keywords": ["天气", "气温", "温度", "下雨", "晴天", "阴天", "多云", "雨", "雪", "风", "气候"],
        "hint": "今天是"+datetime.now().strftime("%Y-%m-%d"),
        "tool": {
            "name": "get_current_weather",
            "description": "你想查询指定城市的天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "城市": {
                            "type": "string",
                            "description": "城市，默认值NONE",
                        },
                        "时间": {
                            "type": "string",
                            "description": "查询的时间，格式为YYYY-MM-DD HH:MM:SS，默认值NONE",
                        }
                    },
                }
        }
    },
    "起名": {
        "keywords": ["起名", "取名", "名字", "命名", "叫什么", "姓名",],
        "hint": "",
        "tool": {
            "name": "naming",
            "description": "你想根据您的信息起名",
            "parameters": {
                "type": "object",
                "properties": {
                    "姓氏": {
                        "type": "string",
                        "description": "您的姓氏，默认值NONE",
                    },
                    "性别": {
                        "type": "string",
                        "description": "男/女，默认值NONE",
                    },
                    "出生日期": {
                        "type": "string",
                        "description": "您的出生日期,格式为YYYY-MM-DD，默认值NONE",
                    },
                    "出生时间": {
                        "type": "string",
                        "description": "您的出生时间，格式为HH:MM:SS",
                    },
                    "出生城市": {
                        "type": "string",
                        "description": "您的出生城市，默认值NONE",
                    },
                    "字数要求": {
                        "type": "string",
                        "description": "单字/双字，默认值NONE",
                    },
                    "特殊要求": {
                        "type": "string",
                        "description": "偏好，特殊要求，默认值NONE",
                    },
                },
            }
        }
    }
}


def search_intent_by_keywords(question: str) -> str:
    """
    通过关键词检索判断意图（支持加权匹配）

    Args:
        question: 用户输入的问题

    Returns:
        str: 匹配到的意图，如果没有匹配返回"其他"

    匹配规则：
    1. 从 tools 字典中读取每个意图的关键词
    2. 统计每个意图匹配到的关键词数量（权重）
    3. 返回权重最高的意图
    4. 如果没有任何匹配，返回"其他"
    """
    # 将问题转换为小写，便于匹配
    question_lower = question.lower()

    # 记录每个意图的匹配权重
    intent_scores = {}

    # 遍历 tools 字典中的每个意图
    for intent, config in tools.items():
        # 跳过"其他"意图，它没有关键词
        if intent == "其他":
            continue

        # 获取该意图的关键词列表
        keywords = config.get("keywords", [])
        if not keywords:  # 如果没有配置关键词，跳过
            continue

        score = 0  # 当前意图的匹配得分
        matched = []  # 匹配到的关键词列表

        # 检查问题中是否包含关键词
        for keyword in keywords:
            if keyword.lower() in question_lower:
                score += 1  # 每匹配一个关键词，得分+1
        # 如果有匹配，记录得分
        if score > 0:
            intent_scores[intent] = score

        # 如果没有任何匹配，返回"其他"
    if not intent_scores:
        return None

        # 找出得分最高的意图
    best_intent = max(intent_scores, key=intent_scores.get)

    # 如果有多个意图得分相同，返回第一个（可以根据需要调整策略）
    return best_intent


@router.post("/chat/intent")
async def chat_intent(chat: ChatIntentRequest):
    """
    聊天意图识别
    """
    # 是否有memory
    if chat.memory:
        # 把memory转成对象
        memory = json.loads(chat.memory)
        intent = memory.get("intent")
        flag = memory.get("flag")

        if intent and flag == "[callback]":  # 有memory的方法
            val = tools.get(intent)
            tool = val.get("tool")
            #  取memory的tool 新question补充memory的question
            response = dashscope_chat_tool(
                tool, get_tool_call(chat.question, memory, intent))
            # 判断是否有tool调用
            if response:  # 识别到工具调用
                if "name" in response and "arguments" in response:  # 识别到工具调用的参数
                    memory["answer"] = response  # 覆盖答案
                    memory["question"] += "\n"+chat.question  # 累积问题
                    properties = analyze_tool_arguments(memory["answer"], tool)
                    memory["hint"] = get_hint(
                        intent, properties["has_value"], properties["missing_or_none"])
                    if properties["missing_or_none"]:  # 有参数缺失或为空
                        memory["flag"] = "[callback]"
                    else:
                        memory["flag"] = "[comfirm]"
                    return memory

        # 有memory，但是没有命中关键词，返回兜底意图
        if intent and flag == "[doubt]":
            val = tools.get(intent)
            tool = val.get("tool")
            other_list = ["其他"]
            reject_list = ["否定", "拒绝"]
            intent_list = ["确认"+tool.get("description", ""), "修改", "肯定"]
            comfirm = dashscope_chat_intent(
                reject_list+intent_list+other_list, chat.question)
            if comfirm in intent_list:
                #  取memory的tool 新question补充memory的question
                response = dashscope_chat_tool(
                    tool, get_tool_call(chat.question, memory, intent))
                # 判断是否有tool调用
                if response:  # 识别到工具调用
                    if "name" in response and "arguments" in response:  # 识别到工具调用的参数
                        memory["answer"] = response  # 覆盖答案
                        memory["question"] += "\n"+chat.question  # 累积问题
                        properties = analyze_tool_arguments(response, tool)
                        memory["hint"] = get_hint(
                            intent, properties["has_value"], properties["missing_or_none"])
                        if properties["missing_or_none"]:  # 有参数缺失或为空
                            memory["flag"] = "[callback]"
                        else:
                            memory["flag"] = "[comfirm]"
                        return memory
            if comfirm in reject_list:
                memory["flag"] = "[stream]"
                return memory

        if intent and flag == "[comfirm]":
            val = tools.get(intent)
            tool = val.get("tool")
            other_list = ["其他"]
            reject_list = ["否定", "修改"]
            comfirm_list = ["确认"+tool.get("description", "肯定")]
            comfirm = dashscope_chat_intent(
                reject_list+comfirm_list+other_list, chat.question)
            log(f"comfirm: {comfirm}")
            if comfirm in comfirm_list:
                memory["flag"] = "[function]"
                return memory
            if comfirm in reject_list:
                memory["flag"] = "[stream]"
                response = dashscope_chat_tool(
                    tool, get_tool_call(chat.question, memory, intent))
                # 判断是否有tool调用
                if response:  # 识别到工具调用
                    if "name" in response and "arguments" in response:  # 识别到工具调用的参数
                        memory["answer"] = response
                        memory["question"] += "\n"+chat.question  # 累积问题
                        properties = analyze_tool_arguments(response, tool)
                        memory["hint"] = get_hint(
                            intent, properties["has_value"], properties["missing_or_none"])
                        if properties["missing_or_none"]:  # 有参数缺失或为空
                            memory["flag"] = "[callback]"
                        else:
                            memory["flag"] = "[comfirm]"
                        return memory
    # 步骤1: 先通过关键词检索快速匹配意图
    memory = {
        "intent": "",
        "tool": {},
        "question": "",
        "answer": {},
        "hint": "",
        "flag": "",
    }
    reject_list = ["政治敏感", "违法犯罪", "违反道德"]
    talk_list = ["关于我"]
    intent_list = list(tools.keys())
    intent = dashscope_chat_intent(
        reject_list+intent_list+talk_list, chat.question)  # 有识别到意图
    memory["question"] = chat.question  # 记录原始问题
    if intent in reject_list:
        memory["answer"] = "不好意思！我好像没有理解您的意思。"
        memory["flag"] = "[reject]"
        return memory
    if intent in talk_list:
        memory["hint"] = "我是智能助手。"
        memory["flag"] = "[stream]"
        return memory

    if intent in intent_list:
        memory["intent"] = search_intent_by_keywords(chat.question)

        # 没有命中关键词，返回怀疑意图
        if not memory["intent"]:
            val = tools.get(intent)
            tool = val.get("tool")
            memory["intent"] = intent
            memory["hint"] = "不太确定您的意思，"+tool.get("description", "")+"？"
            memory["flag"] = "[doubt]"  # 标记为怀疑
            return memory

        val = tools.get(memory["intent"])
        if bool(val):  # 有意图对应的工具集
            tool = val.get("tool")
            if bool(tool):  # 有意图对应的方法
                response = dashscope_chat_tool(
                    tool, chat.question + "\n"+val.get("hint", ""))
                if response:  # 识别到工具调用
                    if "name" in response and "arguments" in response:  # 识别到工具调用的参数
                        memory["answer"] = response
                        properties = analyze_tool_arguments(response, tool)
                        memory["hint"] = get_hint(
                            intent, properties["has_value"], properties["missing_or_none"])
                        if properties["missing_or_none"]:  # 有参数缺失或为空
                            memory["flag"] = "[callback]"
                        else:
                            memory["flag"] = "[comfirm]"
                        return memory
        memory["flag"] = "[stream]"
    return memory


def analyze_tool_arguments(tool_call: dict, tool_schema: dict) -> dict:
    """
    # 定义一个方法，接收工具调用返回和配置，返回属性分析结果
    """
    # 从工具调用返回中安全地获取参数字典，如果不存在则默认为空字典
    provided_args = tool_call.get("arguments", {})
    # 从工具配置中安全地获取定义的属性，兼容不同层级的 schema 结构
    schema_properties = tool_schema.get(
        "parameters", {}).get("properties", {})

    # 初始化一个字典，用于存放有值的属性
    properties_with_value = []
    # 初始化一个字典，用于存放缺失或值为 NONE 的属性
    properties_missing_or_none = []
    # 遍历配置中定义的所有属性名
    for prop_name in schema_properties.keys():
        # 从调用方传入的参数中获取对应属性的值，若不存在则为 None
        value = provided_args.get(prop_name)
        # 检查获取到的值是否为 None (表示缺失) 或字符串 'NONE' (表示显式置空)
        if value is None or (isinstance(value, str) and (value.strip().upper() == 'NONE' or value.strip() == '')):
            # 如果是，则将该属性名记录到“缺失或为 NONE”的字典中
            properties_missing_or_none.append({prop_name: value})
        # 如果属性存在且有具体的值
        else:
            # 则将该属性及其值记录到“有值”的字典中
            properties_with_value.append({prop_name: value})
    # 返回一个包含两个分类结果的字典
    return {
        "has_value": properties_with_value,
        "missing_or_none": properties_missing_or_none
    }


def get_hint(intent: str, properties_with_value: dict, properties_missing_or_none: dict = {}) -> str:

    system_prompt = """
    你是一个助手，你根据用户的意图和工具的提示，返回一句友好提示语，引导用户核对已经输入的信息，以及提醒用户需要补充的信息。
    """
    if len(properties_missing_or_none) > 0:
        user_prompt = """   
        用户的意图：{intent}
        已经输入的信息：{properties_with_value}
        缺失的信息：{properties_missing_or_none}
        """
    else:
        user_prompt = """
        用户的意图：{intent}
        已经输入的信息：{properties_with_value}
        """
    hint = dashscope_chat_block(system_prompt, user_prompt.format(
        intent=intent, properties_with_value=properties_with_value, properties_missing_or_none=properties_missing_or_none))
    if hint:
        return hint
    else:
        return ""


def get_tool_call(question: str, memory: dict, intent: str) -> dict:
    """
    # 定义一个方法，用于从工具调用返回中提取工具调用的参数
    # answer: str - 工具调用返回的字符串
    # -> dict: 返回一个字典，包含工具调用的参数
    """
    val = tools.get(intent)
    hint = val.get("hint", "")
    answer = memory.get("question", "")
    response = f"{answer}\n{question}\n{hint}"
    log(f"get_tool_call: {response}")
    return response


def merge_objects(old_obj: dict, new_obj: dict) -> dict:
    """
    # 定义一个方法，用于深度合并两个字典对象
    # old_obj: dict - 被合并的旧对象
    # new_obj: dict - 用于合并的新对象，其值会覆盖旧对象
    # -> dict: 返回一个全新的、合并后的字典
    """
    # 创建一个旧对象的深度拷贝，以避免修改原始传入的对象
    merged = copy.deepcopy(old_obj)
    # 遍历新对象中的所有键值对
    for key, value in new_obj.items():
        # 检查当前键是否存在于合并后的对象中，并且对应的值是否都是字典类型
        if key in merged and isinstance(merged.get(key), dict) and isinstance(value, dict):
            # 如果都是字典，则递归调用本方法，继续合并下一层
            merged[key] = merge_objects(merged[key], value)
        # 如果不满足递归合并的条件（例如键不存在，或值不是字典）
        else:
            # 如果 value 是字符串，且为 NONE 或 空，则跳过
            if isinstance(value, str):
                if value.strip().upper() == 'NONE' or value.strip() == '':
                    continue
                merged[key] = value
            # 如果 value 为 None，跳过
            elif value is None:
                continue
            else:
                # 其他类型（例如 dict/list 等）直接覆盖
                merged[key] = value
    # 返回最终合并完成的对象
    return merged


# 定义一个函数，用于深度比较两个对象是否完全相等
def are_objects_equal(obj1, obj2) -> bool:
    # 如果两个对象是同一个对象，则直接返回 True
    if obj1 is obj2:
        # 返回 True
        return True
    # 如果两个对象的类型不同，则直接返回 False
    if type(obj1) is not type(obj2):
        # 返回 False
        return False
    # 如果对象是字典类型
    if isinstance(obj1, dict):
        # 检查两个字典的键是否完全相同
        if obj1.keys() != obj2.keys():
            # 如果键不同，则返回 False
            return False
        # 遍历字典的每一个键，递归比较对应的值
        for key in obj1:
            # 如果任何一个键的值不相等，则返回 False
            if not are_objects_equal(obj1[key], obj2[key]):
                # 返回 False
                return False
        # 如果所有键和值都相等，则返回 True
        return True
    # 如果对象是列表或元组类型
    if isinstance(obj1, (list, tuple)):
        # 检查两个列表或元组的长度是否相同
        if len(obj1) != len(obj2):
            # 如果长度不同，则返回 False
            return False
        # 遍历序列中的每一个元素，递归比较
        for i in range(len(obj1)):
            # 如果任何一个位置的元素不相等，则返回 False
            if not are_objects_equal(obj1[i], obj2[i]):
                # 返回 False
                return False
        # 如果所有元素都相等，则返回 True
        return True
    # 对于其他所有基本数据类型（如字符串、数字、布尔值等）
    # 直接使用相等运算符 (==) 进行比较
    return obj1 == obj2
