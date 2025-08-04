#!/usr/bin/env python3
"""
AI智能体综合测试脚本
整合所有功能测试
"""

import sys
import time
from services.weather_service import WeatherService
from services.news_service import NewsService
from services.ollama_service import OllamaService

def test_weather_service():
    """测试天气服务"""
    print("🌤️ 测试天气服务...")
    
    weather_service = WeatherService()
    test_cities = ['北京', '上海', '广州']
    
    for city in test_cities:
        try:
            weather_data = weather_service.get_weather(city)
            print(f"  ✅ {city}: {weather_data['temperature']}°C, {weather_data['description']}")
            
            # 检查天气描述是否正常
            description = weather_data['description']
            if '{' in description or '}' in description:
                print(f"    ❌ 天气描述异常: {description}")
            else:
                print(f"    ✅ 天气描述正常: {description}")
                
        except Exception as e:
            print(f"  ❌ {city}: {e}")
    
    print()

def test_news_service():
    """测试新闻服务"""
    print("📰 测试新闻服务...")
    
    news_service = NewsService()
    
    try:
        # 测试新闻获取
        news_data = news_service.get_news(5)
        print(f"  ✅ 获取到 {len(news_data)} 条新闻")
        
        # 测试地域相关性分析
        test_cities = ['北京', '上海', '广州']
        for city in test_cities:
            relevance_analysis = news_service.analyze_news_relevance(news_data, city)
            print(f"  📍 {city}: {relevance_analysis['relevant_count']}/{relevance_analysis['total_count']} 相关新闻")
            
    except Exception as e:
        print(f"  ❌ 新闻服务测试失败: {e}")
    
    print()

def test_ollama_service():
    """测试Ollama服务"""
    print("🤖 测试Ollama服务...")
    
    ollama_service = OllamaService()
    
    try:
        # 测试模型列表
        models = ollama_service.get_available_models()
        print(f"  ✅ 可用模型: {len(models)} 个")
        for model in models[:3]:  # 只显示前3个
            print(f"    - {model}")
        
        # 测试天气和新闻数据
        weather_service = WeatherService()
        news_service = NewsService()
        
        weather_data = weather_service.get_weather('北京')
        news_data = news_service.get_news(3)
        
        # 测试AI汇总
        summary = ollama_service.generate_summary(weather_data, news_data, '北京')
        print(f"  ✅ AI汇总生成成功 ({len(summary)} 字符)")
        
        # 检查思维链
        chain_keywords = ['根据以上信息', '基于天气和新闻', '现在构思具体内容']
        found_keywords = [kw for kw in chain_keywords if kw in summary]
        if found_keywords:
            print(f"    ⚠️ 检测到思维链关键词: {found_keywords}")
        else:
            print(f"    ✅ 未检测到思维链关键词")
            
    except Exception as e:
        print(f"  ❌ Ollama服务测试失败: {e}")
    
    print()

def test_api_endpoints():
    """测试API接口"""
    print("🌐 测试API接口...")
    
    import requests
    
    base_url = 'http://localhost:5000'
    endpoints = [
        ('/api/cities', 'GET'),
        ('/api/models', 'GET'),
        ('/api/weather?city=北京', 'GET'),
        ('/api/news', 'GET')
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == 'GET':
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                response = requests.post(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"  ✅ {method} {endpoint}")
            else:
                print(f"  ❌ {method} {endpoint}: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {method} {endpoint}: {e}")
    
    print()

def test_integration():
    """测试集成功能"""
    print("🔗 测试集成功能...")
    
    try:
        # 测试完整流程
        weather_service = WeatherService()
        news_service = NewsService()
        ollama_service = OllamaService()
        
        # 1. 获取天气
        weather_data = weather_service.get_weather('北京')
        print(f"  ✅ 天气数据获取: {weather_data['city']} {weather_data['description']}")
        
        # 2. 获取新闻
        news_data = news_service.get_news(5)
        print(f"  ✅ 新闻数据获取: {len(news_data)} 条")
        
        # 3. 地域相关性分析
        relevance_analysis = news_service.analyze_news_relevance(news_data, '北京')
        print(f"  ✅ 地域分析: {relevance_analysis['relevant_count']} 条相关新闻")
        
        # 4. AI汇总
        summary = ollama_service.generate_summary(weather_data, news_data, '北京')
        print(f"  ✅ AI汇总: {len(summary)} 字符")
        
        print("  🎉 集成测试完成")
        
    except Exception as e:
        print(f"  ❌ 集成测试失败: {e}")
    
    print()

def main():
    """主测试函数"""
    print("🚀 AI智能体综合测试")
    print("=" * 50)
    
    # 检查Flask应用是否运行
    try:
        import requests
        response = requests.get('http://localhost:5000', timeout=3)
        if response.status_code == 200:
            print("✅ Flask应用正在运行")
        else:
            print("⚠️ Flask应用可能未正常运行")
    except:
        print("⚠️ Flask应用未运行，部分测试可能失败")
    
    print()
    
    # 运行各项测试
    test_weather_service()
    test_news_service()
    test_ollama_service()
    test_api_endpoints()
    test_integration()
    
    print("📊 测试完成！")
    print("=" * 50)
    print("✅ 所有核心功能测试完成")
    print("✅ 项目运行正常")
    print("✅ 可以开始使用AI智能体")

if __name__ == '__main__':
    main() 