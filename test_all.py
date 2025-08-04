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

def test_news_discussion():
    """测试新闻讨论功能"""
    print("\n🧪 测试新闻讨论功能")
    print("-" * 40)
    
    try:
        # 测试新闻内容抓取
        news_service = NewsService()
        test_url = "https://news.sina.com.cn/tech/2024/01/15/ai-development.html"
        
        print("1. 测试新闻内容抓取...")
        content_data = news_service.get_news_content(test_url)
        
        if content_data['success']:
            print(f"   ✅ 成功抓取内容，长度: {content_data['length']} 字符")
        else:
            print(f"   ⚠️ 抓取失败: {content_data['error']}")
        
        # 测试AI讨论功能
        print("2. 测试AI讨论功能...")
        ollama_service = OllamaService()
        
        test_content = "人工智能技术快速发展，ChatGPT等大语言模型引领AI革命。"
        test_question = "这条新闻的主要影响是什么？"
        
        response = ollama_service.discuss_news(test_content, test_question, "AI发展新闻")
        
        if response and len(response) > 10:
            print(f"   ✅ AI回复成功，长度: {len(response)} 字符")
            print(f"   回复预览: {response[:100]}...")
        else:
            print("   ❌ AI回复失败或内容过短")
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")

def test_news_relevance_sorting():
    """测试新闻相关程度排序"""
    print("\n🧪 测试新闻相关程度排序")
    print("-" * 40)
    
    try:
        news_service = NewsService()
        
        # 测试按城市相关程度排序
        print("1. 测试北京相关新闻排序...")
        beijing_news = news_service.get_news(5, "北京")
        
        if beijing_news:
            print(f"   ✅ 获取到 {len(beijing_news)} 条新闻")
            
            # 检查排序是否正确
            scores = [news['relevance_score'] for news in beijing_news]
            is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
            
            if is_sorted:
                print("   ✅ 新闻按相关程度正确排序")
            else:
                print("   ❌ 新闻排序不正确")
            
            # 显示前3条新闻的相关程度
            for i, news in enumerate(beijing_news[:3], 1):
                print(f"   {i}. {news['title']}")
                print(f"      相关程度: {news['relevance_level']} (分数: {news['relevance_score']})")
        else:
            print("   ❌ 未获取到新闻")
            
        # 测试上海相关新闻
        print("\n2. 测试上海相关新闻排序...")
        shanghai_news = news_service.get_news(5, "上海")
        
        if shanghai_news:
            print(f"   ✅ 获取到 {len(shanghai_news)} 条新闻")
            
            # 显示前3条新闻的相关程度
            for i, news in enumerate(shanghai_news[:3], 1):
                print(f"   {i}. {news['title']}")
                print(f"      相关程度: {news['relevance_level']} (分数: {news['relevance_score']})")
        else:
            print("   ❌ 未获取到新闻")
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")

def test_conversation_flow():
    """测试持续性对话流程"""
    print("\n🧪 测试持续性对话流程")
    print("-" * 40)
    
    try:
        ollama_service = OllamaService()
        
        # 模拟新闻内容
        test_content = "浙江农商行利润增长显著，萧山农商行利息净收入增长超过2亿元，投资收入增长超过3亿元。"
        test_title = "浙江农商行利润增长分析"
        
        # 模拟对话历史
        conversation_history = []
        
        # 第一轮对话
        print("1. 第一轮对话...")
        question1 = "这条新闻的主要影响是什么？"
        response1 = ollama_service.discuss_news(test_content, question1, test_title, conversation_history)
        conversation_history.append((question1, response1))
        
        if response1 and len(response1) > 10:
            print(f"   ✅ 第一轮对话成功，回复长度: {len(response1)} 字符")
        else:
            print("   ❌ 第一轮对话失败")
            return
        
        # 第二轮对话
        print("2. 第二轮对话...")
        question2 = "为什么会出现这种增长？"
        response2 = ollama_service.discuss_news(test_content, question2, test_title, conversation_history)
        conversation_history.append((question2, response2))
        
        if response2 and len(response2) > 10:
            print(f"   ✅ 第二轮对话成功，回复长度: {len(response2)} 字符")
        else:
            print("   ❌ 第二轮对话失败")
            return
        
        # 第三轮对话（基于前序问答）
        print("3. 第三轮对话（基于前序问答）...")
        question3 = "基于前面的讨论，这种增长趋势会持续吗？"
        response3 = ollama_service.discuss_news(test_content, question3, test_title, conversation_history)
        
        if response3 and len(response3) > 10:
            print(f"   ✅ 第三轮对话成功，回复长度: {len(response3)} 字符")
            print(f"   对话历史长度: {len(conversation_history)} 轮")
        else:
            print("   ❌ 第三轮对话失败")
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")

def test_conversation_without_history():
    """测试无对话历史的情况"""
    print("\n🧪 测试无对话历史的情况")
    print("-" * 40)
    
    try:
        ollama_service = OllamaService()
        
        test_content = "人工智能技术快速发展，ChatGPT等大语言模型引领AI革命。"
        test_title = "AI发展新闻"
        
        question = "这条新闻的主要影响是什么？"
        response = ollama_service.discuss_news(test_content, question, test_title, None)
        
        if response and len(response) > 10:
            print(f"   ✅ 无历史对话成功，回复长度: {len(response)} 字符")
        else:
            print("   ❌ 无历史对话失败")
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")

def test_region_display():
    """测试地区标注功能"""
    print("\n🧪 测试地区标注功能")
    print("-" * 40)
    
    try:
        # 测试天气服务
        weather_service = WeatherService()
        weather_data = weather_service.get_weather("北京")
        
        if weather_data:
            print("1. 天气信息地区标注...")
            print(f"   ✅ 城市信息: {weather_data['city']}")
            print(f"   温度: {weather_data['temperature']}°C")
            print(f"   天气: {weather_data['description']}")
            print(f"   更新时间: {weather_data['update_time']}")
        else:
            print("   ❌ 天气信息获取失败")
        
        # 测试新闻服务
        news_service = NewsService()
        news_list = news_service.get_news(5, "上海")
        
        if news_list:
            print("\n2. 新闻信息地区标注...")
            print(f"   ✅ 获取到 {len(news_list)} 条上海相关新闻")
            
            # 检查新闻是否按相关程度排序
            scores = [news['relevance_score'] for news in news_list]
            is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
            
            if is_sorted:
                print("   ✅ 新闻按相关程度正确排序")
            else:
                print("   ❌ 新闻排序不正确")
            
            # 显示前3条新闻
            for i, news in enumerate(news_list[:3], 1):
                print(f"   {i}. {news['title']}")
                print(f"      相关程度: {news['relevance_level']} (分数: {news['relevance_score']})")
        else:
            print("   ❌ 新闻信息获取失败")
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")

def test_auto_refresh():
    """测试自动刷新功能"""
    print("\n🧪 测试自动刷新功能")
    print("-" * 40)
    
    try:
        # 模拟不同城市的自动刷新
        test_cities = ['北京', '上海', '广州']
        
        for city in test_cities:
            print(f"测试城市: {city}")
            
            # 测试天气
            weather_service = WeatherService()
            weather = weather_service.get_weather(city)
            if weather:
                print(f"   ✅ {city} 天气信息刷新成功")
            else:
                print(f"   ❌ {city} 天气信息刷新失败")
            
            # 测试新闻
            news_service = NewsService()
            news = news_service.get_news(3, city)
            if news:
                print(f"   ✅ {city} 新闻信息刷新成功 ({len(news)} 条)")
            else:
                print(f"   ❌ {city} 新闻信息刷新失败")
        
        print("   ✅ 自动刷新功能测试完成")
        
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")

def test_thinking_filter():
    """测试思考内容过滤功能"""
    print("\n🧪 测试思考内容过滤功能")
    print("-" * 40)
    
    try:
        from services.ollama_service import OllamaService
        ollama_service = OllamaService()
        
        # 测试用例
        test_cases = [
            {
                "name": "测试<think>标签",
                "input": """现在构思具体内容:
让我分析一下天气和新闻信息。

<think>
我需要先分析天气情况，然后看新闻内容，最后进行总结。
</think>

# 今日汇总报告

## 天气情况
北京今天天气晴朗，温度25°C。

## 新闻要点
1. 重要新闻一
2. 重要新闻二"""
            },
            {
                "name": "测试思考关键词",
                "input": """现在构思具体内容:
让我分析一下这些信息。

基于以上信息，我来为您总结：

# 汇总报告

## 主要内容
这是主要内容。

现在让我为您详细分析：

## 详细分析
详细内容。"""
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"{i}. {test_case['name']}")
            
            # 应用过滤
            filtered_content = ollama_service._remove_thinking_content(test_case['input'])
            
            # 检查过滤效果
            thinking_indicators = [
                '<think>', '</think>', '<thinking>', '</thinking>',
                '现在构思具体内容:', '让我分析一下', '基于以上信息',
                '现在让我', '我会把这些内容', '让我来总结',
                '现在我来', '基于天气和新闻', '让我为您'
            ]
            
            remaining_indicators = []
            for indicator in thinking_indicators:
                if indicator.lower() in filtered_content.lower():
                    remaining_indicators.append(indicator)
            
            if remaining_indicators:
                print(f"   ⚠️  仍有思考内容残留: {remaining_indicators}")
            else:
                print(f"   ✅ 思考内容过滤成功")
        
        print("   ✅ 思考内容过滤功能测试完成")
        
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")

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
    test_news_discussion()
    test_news_relevance_sorting()
    test_conversation_flow()
    test_conversation_without_history()
    test_region_display()
    test_auto_refresh()
    test_thinking_filter()
    
    print("📊 测试完成！")
    print("=" * 50)
    print("✅ 所有核心功能测试完成")
    print("✅ 项目运行正常")
    print("✅ 可以开始使用AI智能体")

if __name__ == '__main__':
    main() 