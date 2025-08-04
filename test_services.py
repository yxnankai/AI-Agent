#!/usr/bin/env python3
"""
服务测试脚本
用于测试天气服务、新闻服务和Ollama服务是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.weather_service import WeatherService
from services.news_service import NewsService
from services.ollama_service import OllamaService
import json

def test_weather_service():
    """测试天气服务"""
    print("🌤️  测试天气服务...")
    try:
        weather_service = WeatherService()
        weather_data = weather_service.get_weather("北京")
        print("✅ 天气服务测试成功")
        print(f"   城市: {weather_data['city']}")
        print(f"   温度: {weather_data['temperature']}°C")
        print(f"   天气: {weather_data['description']}")
        return True
    except Exception as e:
        print(f"❌ 天气服务测试失败: {e}")
        return False

def test_news_service():
    """测试新闻服务"""
    print("📰 测试新闻服务...")
    try:
        news_service = NewsService()
        news_data = news_service.get_news(5)
        print("✅ 新闻服务测试成功")
        print(f"   获取到 {len(news_data)} 条新闻")
        for i, news in enumerate(news_data[:3], 1):
            print(f"   {i}. {news['title'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ 新闻服务测试失败: {e}")
        return False

def test_ollama_service():
    """测试Ollama服务"""
    print("🤖 测试Ollama服务...")
    try:
        ollama_service = OllamaService()
        
        # 测试连接
        if not ollama_service.test_connection():
            print("❌ Ollama服务连接失败")
            return False
        
        # 测试汇总功能
        weather_data = {
            'city': '北京',
            'temperature': '22',
            'description': '多云',
            'humidity': '65'
        }
        
        news_data = [
            {
                'title': '测试新闻标题',
                'summary': '这是一条测试新闻的摘要',
                'source': '测试来源',
                'category': '测试'
            }
        ]
        
        summary = ollama_service.generate_summary(weather_data, news_data)
        print("✅ Ollama服务测试成功")
        print(f"   生成汇总长度: {len(summary)} 字符")
        return True
    except Exception as e:
        print(f"❌ Ollama服务测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始服务测试...\n")
    
    results = []
    
    # 测试天气服务
    results.append(("天气服务", test_weather_service()))
    print()
    
    # 测试新闻服务
    results.append(("新闻服务", test_news_service()))
    print()
    
    # 测试Ollama服务
    results.append(("Ollama服务", test_ollama_service()))
    print()
    
    # 输出测试结果
    print("📊 测试结果汇总:")
    print("-" * 40)
    
    all_passed = True
    for service_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{service_name:<15} {status}")
        if not passed:
            all_passed = False
    
    print("-" * 40)
    
    if all_passed:
        print("🎉 所有服务测试通过！应用可以正常启动。")
        return 0
    else:
        print("⚠️  部分服务测试失败，请检查相关配置。")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 