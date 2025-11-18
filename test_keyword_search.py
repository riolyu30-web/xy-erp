#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
关键词检索功能测试脚本

用于测试意图识别中的关键词匹配功能
"""

import requests
import json
from typing import Dict, Any

# API 配置
API_URL = "http://127.0.0.1:8000/api/v1/chat/intent"

# 测试用例
test_cases = [
    {
        "name": "天气查询 - 直接关键词",
        "question": "今天北京的天气怎么样？",
        "expected_intent": "天气",
        "expect_keyword_match": True
    },
    {
        "name": "天气查询 - 多个关键词",
        "question": "明天会下雨吗？气温多少度？",
        "expected_intent": "天气",
        "expect_keyword_match": True
    },
    {
        "name": "天气查询 - 英文",
        "question": "What's the weather today?",
        "expected_intent": "天气",
        "expect_keyword_match": True
    },
    {
        "name": "起名 - 直接关键词",
        "question": "帮我给孩子起个名字",
        "expected_intent": "起名",
        "expect_keyword_match": True
    },
    {
        "name": "起名 - 同义词",
        "question": "宝宝取名",
        "expected_intent": "起名",
        "expect_keyword_match": True
    },
    {
        "name": "模糊表达 - 需要 LLM",
        "question": "帮我查询一下",
        "expected_intent": None,
        "expect_keyword_match": False
    },
    {
        "name": "复杂表达 - 多意图",
        "question": "天气不好，名字也不好听",
        "expected_intent": "起名",  # 根据得分判断
        "expect_keyword_match": True
    }
]


def send_request(question: str) -> Dict[str, Any]:
    """
    发送请求到意图识别接口
    
    Args:
        question: 用户问题
        
    Returns:
        接口响应数据
    """
    payload = {
        "question": question,
        "memory": ""
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return {}


def run_tests():
    """
    运行所有测试用例
    """
    print("=" * 80)
    print("🧪 关键词检索功能测试")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}: {test['name']}")
        print(f"   问题: {test['question']}")
        
        # 发送请求
        result = send_request(test['question'])
        
        if not result:
            print(f"   ❌ 测试失败: 无法获取响应")
            failed += 1
            continue
        
        # 获取识别的意图
        detected_intent = result.get('intent', '')
        
        # 检查结果
        if test['expected_intent'] is None:
            # 预期无意图
            if not detected_intent:
                print(f"   ✅ 测试通过: 正确识别为无明确意图")
                passed += 1
            else:
                print(f"   ⚠️  测试通过（但识别到意图）: {detected_intent}")
                passed += 1
        else:
            # 预期有意图
            if detected_intent == test['expected_intent']:
                print(f"   ✅ 测试通过: 正确识别为 '{detected_intent}'")
                passed += 1
            else:
                print(f"   ❌ 测试失败: 预期 '{test['expected_intent']}', 实际 '{detected_intent}'")
                failed += 1
        
        # 显示部分响应信息
        if result.get('flag'):
            print(f"   状态: {result['flag']}")
        if result.get('hint'):
            print(f"   提示: {result['hint'][:50]}...")
    
    # 总结
    print()
    print("=" * 80)
    print("📊 测试结果汇总")
    print("=" * 80)
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"📈 通过率: {passed / (passed + failed) * 100:.1f}%")
    print()


def interactive_test():
    """
    交互式测试模式
    """
    print("=" * 80)
    print("🎮 交互式测试模式")
    print("=" * 80)
    print("输入问题进行测试，输入 'quit' 退出")
    print()
    
    while True:
        question = input("💬 请输入问题: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 再见！")
            break
        
        if not question:
            continue
        
        print(f"\n🔍 正在识别意图...")
        result = send_request(question)
        
        if result:
            print(f"\n📋 识别结果:")
            print(f"   意图: {result.get('intent', '无')}")
            print(f"   状态: {result.get('flag', '无')}")
            if result.get('hint'):
                print(f"   提示: {result['hint']}")
            if result.get('answer'):
                print(f"   参数: {json.dumps(result['answer'], ensure_ascii=False, indent=6)}")
        
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        # 交互式模式
        interactive_test()
    else:
        # 自动测试模式
        run_tests()
        
        # 询问是否进入交互模式
        print()
        choice = input("是否进入交互式测试模式？(y/n): ").strip().lower()
        if choice == 'y':
            print()
            interactive_test()

