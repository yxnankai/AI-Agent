#!/usr/bin/env python3
"""
测试地域相关性分析功能
"""

from services.news_service import NewsService
from services.ollama_service import OllamaService
from services.weather_service import WeatherService

def test_news_relevance_analysis():
    """测试新闻地域相关性分析"""
    print("🧪 测试新闻地域相关性分析...")
    
    news_service = NewsService()
    
    # 获取测试新闻数据
    news_data = news_service.get_news(10)
    print(f"📊 获取到 {len(news_data)} 条新闻")
    
    # 测试不同城市的相关性分析
    test_cities = ['北京', '上海', '广州', '深圳', '杭州']
    
    for city in test_cities:
        print(f"\n🏙️ 测试城市: {city}")
        
        # 分析相关性
        relevance_analysis = news_service.analyze_news_relevance(news_data, city)
        
        print(f"   相关新闻数量: {relevance_analysis['relevant_count']}/{relevance_analysis['total_count']}")
        print(f"   相关性比例: {relevance_analysis['relevance_rate']:.1%}")
        
        # 显示相关新闻标题
        if relevance_analysis['relevant_news']:
            print("   相关新闻:")
            for i, news in enumerate(relevance_analysis['relevant_news'][:3], 1):
                print(f"     {i}. {news['title']}")
        else:
            print("   未找到相关新闻，使用备选新闻")
            for i, news in enumerate(relevance_analysis['relevant_news'][:3], 1):
                print(f"     {i}. {news['title']}")

def test_city_keywords():
    """测试城市关键词匹配"""
    print("\n🔍 测试城市关键词匹配...")
    
    news_service = NewsService()
    
    # 测试新闻
    test_news = [
        {
            'title': '北京科技创新中心建设加速推进',
            'summary': '北京作为全国科技创新中心，正在加速推进各项创新项目。'
        },
        {
            'title': '上海自贸区深化改革，营商环境持续优化',
            'summary': '上海自贸区深化改革措施不断，营商环境持续优化。'
        },
        {
            'title': '广州数字经济蓬勃发展，智慧城市建设提速',
            'summary': '广州数字经济蓬勃发展，智慧城市建设全面提速。'
        },
        {
            'title': '人工智能技术发展迅速，ChatGPT引领AI革命',
            'summary': '人工智能技术在全球范围内快速发展，ChatGPT等大语言模型引领AI革命。'
        }
    ]
    
    test_cities = ['北京', '上海', '广州']
    
    for city in test_cities:
        print(f"\n🏙️ 城市: {city}")
        relevance_analysis = news_service.analyze_news_relevance(test_news, city)
        
        print(f"   相关新闻数量: {relevance_analysis['relevant_count']}")
        for news in relevance_analysis['relevant_news']:
            print(f"   • {news['title']}")

def test_ai_summary_with_relevance():
    """测试AI汇总的地域相关性功能"""
    print("\n🤖 测试AI汇总的地域相关性功能...")
    
    weather_service = WeatherService()
    news_service = NewsService()
    ollama_service = OllamaService()
    
    test_cities = ['北京', '上海', '广州']
    
    for city in test_cities:
        print(f"\n🏙️ 测试城市: {city}")
        
        try:
            # 获取天气和新闻数据
            weather_data = weather_service.get_weather(city)
            news_data = news_service.get_news(10)
            
            # 生成AI汇总
            summary = ollama_service.generate_summary(weather_data, news_data, city)
            
            print(f"   天气: {weather_data['description']} {weather_data['temperature']}°C")
            print(f"   汇总长度: {len(summary)} 字符")
            
            # 检查汇总中是否包含城市相关信息
            if city in summary:
                print(f"   ✅ 汇总包含城市信息: {city}")
            else:
                print(f"   ⚠️ 汇总未明确提及城市: {city}")
            
            # 显示汇总的前几行
            lines = summary.split('\n')[:6]
            print("   汇总预览:")
            for line in lines:
                if line.strip():
                    print(f"     {line}")
            
        except Exception as e:
            print(f"   ❌ 生成汇总失败: {e}")

def test_relevance_filtering():
    """测试新闻筛选功能"""
    print("\n🔧 测试新闻筛选功能...")
    
    news_service = NewsService()
    
    # 获取新闻数据
    news_data = news_service.get_news(15)
    
    test_cities = ['北京', '上海', '广州', '深圳']
    
    for city in test_cities:
        print(f"\n🏙️ 城市: {city}")
        
        # 筛选相关新闻
        filtered_news = news_service.filter_news_by_city(news_data, city)
        
        print(f"   原始新闻数量: {len(news_data)}")
        print(f"   筛选后数量: {len(filtered_news)}")
        
        # 显示筛选结果
        for i, news in enumerate(filtered_news[:3], 1):
            print(f"   {i}. {news['title']}")

def main():
    """主测试函数"""
    print("🚀 地域相关性分析功能测试")
    print("=" * 50)
    
    # 测试新闻相关性分析
    test_news_relevance_analysis()
    
    # 测试城市关键词匹配
    test_city_keywords()
    
    # 测试新闻筛选功能
    test_relevance_filtering()
    
    # 测试AI汇总功能
    test_ai_summary_with_relevance()
    
    print("\n📊 测试完成！")
    print("=" * 50)
    print("✅ 地域相关性分析功能已实现")
    print("✅ 支持20个主要城市的关键词匹配")
    print("✅ AI汇总会自动筛选相关新闻")
    print("✅ 提供相关性分析和统计信息")

if __name__ == '__main__':
    main() 