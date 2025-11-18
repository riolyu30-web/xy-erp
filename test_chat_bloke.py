#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 dashscope_chat_bloke 函数

演示如何使用 LLM 返回普通文本
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.llm_service import dashscope_chat_bloke


def test_simple_qa():
    """测试 1：简单问答"""
    print("=" * 80)
    print("测试 1：简单问答")
    print("=" * 80)
    
    system_prompt = "你是一个友好的助手，用简短的话回答问题"
    user_prompt = "什么是人工智能？"
    
    print(f"系统提示: {system_prompt}")
    print(f"用户问题: {user_prompt}")
    print(f"\nAI 回答: ", end="", flush=True)
    
    answer = dashscope_chat_bloke(system_prompt, user_prompt)
    print(answer)
    print()


def test_text_generation():
    """测试 2：文本生成"""
    print("=" * 80)
    print("测试 2：文本生成（广告语）")
    print("=" * 80)
    
    system_prompt = "你是一个广告文案专家，生成简洁有力的广告语"
    user_prompt = "为一款智能手表写一句广告语"
    
    print(f"系统提示: {system_prompt}")
    print(f"用户问题: {user_prompt}")
    print(f"\nAI 回答: ", end="", flush=True)
    
    answer = dashscope_chat_bloke(system_prompt, user_prompt)
    print(answer)
    print()


def test_sentiment_analysis():
    """测试 3：情感分析"""
    print("=" * 80)
    print("测试 3：情感分析")
    print("=" * 80)
    
    system_prompt = "分析以下文本的情感，只返回：正面、负面或中性"
    
    test_texts = [
        "这个产品太棒了，非常满意！",
        "质量一般般，不太满意",
        "收到了，正在使用中"
    ]
    
    for text in test_texts:
        print(f"文本: {text}")
        print(f"情感: ", end="", flush=True)
        
        sentiment = dashscope_chat_bloke(system_prompt, text)
        print(sentiment)
        print()


def test_summary():
    """测试 4：文本摘要"""
    print("=" * 80)
    print("测试 4：文本摘要")
    print("=" * 80)
    
    system_prompt = "你是一个摘要专家，用一句话总结文本的核心内容"
    user_prompt = """
    人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，
    它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    """
    
    print(f"系统提示: {system_prompt}")
    print(f"原文: {user_prompt.strip()[:50]}...")
    print(f"\nAI 摘要: ", end="", flush=True)
    
    summary = dashscope_chat_bloke(system_prompt, user_prompt)
    print(summary)
    print()


def test_translation():
    """测试 5：翻译"""
    print("=" * 80)
    print("测试 5：翻译")
    print("=" * 80)
    
    system_prompt = "你是一个专业翻译，将以下中文翻译成英文"
    user_prompt = "今天天气很好"
    
    print(f"系统提示: {system_prompt}")
    print(f"中文: {user_prompt}")
    print(f"英文: ", end="", flush=True)
    
    translated = dashscope_chat_bloke(system_prompt, user_prompt)
    print(translated)
    print()


def test_keyword_extraction():
    """测试 6：关键词提取"""
    print("=" * 80)
    print("测试 6：关键词提取")
    print("=" * 80)
    
    system_prompt = "提取以下文本的关键词，用逗号分隔，不超过5个"
    user_prompt = "人工智能技术正在快速发展，机器学习和深度学习成为研究热点"
    
    print(f"系统提示: {system_prompt}")
    print(f"文本: {user_prompt}")
    print(f"关键词: ", end="", flush=True)
    
    keywords = dashscope_chat_bloke(system_prompt, user_prompt)
    print(keywords)
    print()


def interactive_mode():
    """交互式测试模式"""
    print("=" * 80)
    print("🎮 交互式测试模式")
    print("=" * 80)
    print("输入 'quit' 退出")
    print()
    
    system_prompt = input("请输入系统提示词（留空使用默认）: ").strip()
    if not system_prompt:
        system_prompt = "你是一个友好的助手"
    
    print(f"\n使用系统提示: {system_prompt}")
    print()
    
    while True:
        user_prompt = input("💬 请输入问题: ").strip()
        
        if user_prompt.lower() in ['quit', 'exit', 'q']:
            print("👋 再见！")
            break
        
        if not user_prompt:
            continue
        
        print(f"\n🤖 AI 回答: ", end="", flush=True)
        
        try:
            answer = dashscope_chat_bloke(system_prompt, user_prompt)
            print(answer)
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
        
        print()


def run_all_tests():
    """运行所有测试"""
    print("\n")
    print("🧪 开始测试 dashscope_chat_bloke 函数")
    print("\n")
    
    tests = [
        test_simple_qa,
        test_text_generation,
        test_sentiment_analysis,
        test_summary,
        test_translation,
        test_keyword_extraction
    ]
    
    for i, test_func in enumerate(tests, 1):
        try:
            test_func()
        except Exception as e:
            print(f"❌ 测试 {i} 失败: {str(e)}")
            print()
        
        # 测试之间暂停一下
        if i < len(tests):
            input("按 Enter 继续下一个测试...")
            print()
    
    print("=" * 80)
    print("✅ 所有测试完成")
    print("=" * 80)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        # 交互式模式
        interactive_mode()
    else:
        # 自动测试模式
        run_all_tests()
        
        # 询问是否进入交互模式
        print()
        choice = input("是否进入交互式测试模式？(y/n): ").strip().lower()
        if choice == 'y':
            print()
            interactive_mode()

