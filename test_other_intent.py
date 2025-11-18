#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试"其他"意图功能

验证当用户输入不匹配任何关键词时，系统能正确返回"其他"意图
"""

import requests
import json

# API 配置
API_URL = "http://127.0.0.1:8000/api/v1/chat/intent"

# 测试用例
test_cases = [
    {
        "name": "天气查询 - 应该匹配",
        "question": "今天北京天气怎么样？",
        "expected_intent": "天气",
    },
    {
        "name": "起名 - 应该匹配",
        "question": "帮我给孩子起个名字",
        "expected_intent": "起名",
    },
    {
        "name": "模糊表达 - 应该返回其他",
        "question": "帮我查询一下",
        "expected_intent": "其他",
    },
    {
        "name": "无关内容 - 应该返回其他",
        "question": "你好",
        "expected_intent": "其他",
    },
    {
        "name": "随机内容 - 应该返回其他",
        "question": "abc123",
        "expected_intent": "其他",
    },
    {
        "name": "问候语 - 应该返回其他",
        "question": "早上好",
        "expected_intent": "其他",
    },
]


def send_request(question: str):
    """发送请求"""
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
        return None


def run_tests():
    """运行测试"""
    print("=" * 80)
    print("🧪 测试'其他'意图功能")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}: {test['name']}")
        print(f"   问题: {test['question']}")
        
        result = send_request(test['question'])
        
        if not result:
            print(f"   ❌ 测试失败: 无法获取响应")
            failed += 1
            continue
        
        detected_intent = result.get('intent', '')
        expected_intent = test['expected_intent']
        
        if detected_intent == expected_intent:
            print(f"   ✅ 测试通过: 正确识别为 '{detected_intent}'")
            passed += 1
        else:
            print(f"   ❌ 测试失败: 预期 '{expected_intent}', 实际 '{detected_intent}'")
            failed += 1
        
        # 显示响应信息
        if result.get('hint'):
            print(f"   💡 提示: {result['hint']}")
        if result.get('flag'):
            print(f"   🏷️  状态: {result['flag']}")
    
    # 总结
    print()
    print("=" * 80)
    print("📊 测试结果汇总")
    print("=" * 80)
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"📈 通过率: {passed / (passed + failed) * 100:.1f}%")
    print()
    
    # 显示"其他"意图的行为
    print("\n💡 '其他'意图特点:")
    print("   - 当用户输入不匹配任何关键词时触发")
    print("   - 返回友好的提示信息，引导用户说明需求")
    print("   - flag 标记为 '[other]'")
    print("   - 不会调用任何具体的工具")


if __name__ == "__main__":
    run_tests()

