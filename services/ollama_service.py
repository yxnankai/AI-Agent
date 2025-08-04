import ollama
import json
from datetime import datetime

class OllamaService:
    def __init__(self, model_name=None):
        """
        初始化Ollama服务
        model_name: 使用的模型名称，如果为None则自动选择第一个可用模型
        """
        self.client = ollama.Client()
        self.model_name = model_name
        self._initialize_model()
        
    def _initialize_model(self):
        """初始化模型，自动选择可用模型"""
        try:
            models = self.get_available_models()
            if models:
                if self.model_name is None:
                    # 优先选择qwen模型，如果没有则选择第一个
                    qwen_models = [m for m in models if 'qwen' in m['name'].lower()]
                    if qwen_models:
                        self.model_name = qwen_models[0]['name']
                    else:
                        self.model_name = models[0]['name']
                    print(f"自动选择模型: {self.model_name}")
                else:
                    # 检查指定的模型是否存在
                    model_names = [m['name'] for m in models]
                    if self.model_name not in model_names:
                        print(f"指定的模型 {self.model_name} 不存在，使用第一个可用模型")
                        self.model_name = models[0]['name']
            else:
                print("警告: 未找到可用模型")
                self.model_name = "qwen:latest"  # 默认模型
        except Exception as e:
            print(f"初始化模型时出错: {e}")
            self.model_name = "qwen:latest"  # 默认模型
    
    def get_available_models(self):
        """
        获取可用的模型列表
        """
        try:
            models = self.client.list()
            model_list = []
            for model in models['models']:
                model_list.append({
                    'name': model['name'],
                    'size': model.get('size', '未知'),
                    'modified_at': model.get('modified_at', '未知'),
                    'digest': model.get('digest', '未知')
                })
            return model_list
        except Exception as e:
            print(f"获取模型列表失败: {e}")
            return []
    
    def set_model(self, model_name):
        """
        设置使用的模型
        """
        try:
            # 检查模型是否存在
            models = self.get_available_models()
            model_names = [m['name'] for m in models]
            
            if model_name in model_names:
                self.model_name = model_name
                return True
            else:
                print(f"模型 {model_name} 不存在")
                return False
        except Exception as e:
            print(f"设置模型失败: {e}")
            return False
        
    def generate_summary(self, weather_data, news_data, city=None):
        """
        生成AI汇总报告，包含地域相关性分析
        """
        try:
            # 如果提供了城市信息，进行地域相关性分析
            if city and news_data:
                from services.news_service import NewsService
                news_service = NewsService()
                
                # 分析新闻与城市的相关性
                relevance_analysis = news_service.analyze_news_relevance(news_data, city)
                
                # 使用相关性分析后的新闻
                filtered_news = relevance_analysis['relevant_news']
                
                # 构建包含地域分析信息的提示词
                prompt = self._build_prompt_with_relevance(weather_data, filtered_news, city, relevance_analysis)
            else:
                # 如果没有城市信息，使用原始新闻
                filtered_news = news_data
                prompt = self._build_prompt(weather_data, filtered_news)
            
            # 调用Ollama生成汇总
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                stream=False
            )
            
            return response['response']
            
        except Exception as e:
            print(f"Ollama调用失败: {e}")
            # 使用备用汇总方案
            if city and news_data:
                from services.news_service import NewsService
                news_service = NewsService()
                relevance_analysis = news_service.analyze_news_relevance(news_data, city)
                filtered_news = relevance_analysis['relevant_news']
                return self._generate_fallback_summary_with_relevance(weather_data, filtered_news, city, relevance_analysis)
            else:
                return self._generate_fallback_summary(weather_data, news_data)

    def _build_prompt_with_relevance(self, weather_data, news_data, city, relevance_analysis):
        """
        构建包含地域相关性分析的提示词
        """
        weather_text = f"""
**天气信息：**
- 城市：{weather_data.get('city', '未知')}
- 温度：{weather_data.get('temperature', '未知')}°C
- 体感温度：{weather_data.get('feels_like', '未知')}°C
- 天气状况：{weather_data.get('description', '未知')}
- 湿度：{weather_data.get('humidity', '未知')}%
- 风速：{weather_data.get('wind_speed', '未知')} km/h
- 风向：{weather_data.get('wind_direction', '未知')}
- 能见度：{weather_data.get('visibility', '未知')} km
- 气压：{weather_data.get('pressure', '未知')} hPa
- 更新时间：{weather_data.get('update_time', '未知')}
"""

        # 地域相关性分析信息
        relevance_info = f"""
**地域相关性分析：**
- 目标城市：{city}
- 相关新闻数量：{relevance_analysis['relevant_count']}/{relevance_analysis['total_count']}
- 相关性比例：{relevance_analysis['relevance_rate']:.1%}
- 筛选策略：优先展示与{city}相关的热点新闻
"""

        news_text = "**相关热点新闻：**\n"
        for i, news in enumerate(news_data[:5], 1):
            news_text += f"{i}. {news.get('title', '未知标题')}\n"
            news_text += f"   来源：{news.get('source', '未知')} | 分类：{news.get('category', '未知')}\n"
            news_text += f"   摘要：{news.get('summary', '无摘要')}\n\n"

        prompt = f"""
请根据以下天气信息和地域相关热点新闻，生成一份简洁的汇总报告。

**输出要求：**
1. 直接输出markdown格式的汇总报告
2. 报告结构必须包含以下三个部分：
   - ## 今日天气概况
   - ## 热点新闻聚焦（{city}相关）
   - ## 生活工作建议
3. 语言简洁明了，突出重点信息
4. 总字数控制在300字以内
5. 使用规范的markdown语法
6. 不要包含任何分析过程、思维链、思考过程或过渡语句
7. 不要使用"根据以上信息"、"基于天气和新闻"、"现在构思具体内容"等表述
8. 不要输出"我会把这些内容组织成简洁的段落"等思考过程
9. 直接输出结果，不要解释或说明
10. 不要包含任何模型思考、构思或分析步骤
11. 在热点新闻部分，重点突出与{city}相关的新闻内容

{relevance_info}

**输入信息：**

{weather_text}

{news_text}

请直接输出markdown格式的汇总报告：
"""
        
        return prompt

    def _generate_fallback_summary_with_relevance(self, weather_data, news_data, city, relevance_analysis):
        """
        当Ollama调用失败时的备用汇总方案（包含地域相关性）
        """
        city_name = weather_data.get('city', city)
        temp = weather_data.get('temperature', '未知')
        weather_desc = weather_data.get('description', '未知')
        humidity = weather_data.get('humidity', '未知')
        wind_speed = weather_data.get('wind_speed', '未知')
        
        news_titles = [news.get('title', '') for news in news_data[:3]]
        
        summary = f"""# AI智能汇总报告

## 今日天气概况

{city_name}今日天气{weather_desc}，气温{temp}°C，湿度{humidity}%，风速{wind_speed}km/h。

## 热点新闻聚焦（{city}相关）

{chr(10).join([f"• {title}" for title in news_titles if title])}

## 生活工作建议

根据{city}天气情况合理安排出行，关注本地热点新闻动态，保持信息敏感度。"""
        
        return summary
    
    def _build_prompt(self, weather_data, news_data):
        """
        构建规范化的提示词
        """
        weather_text = f"""
**天气信息：**
- 城市：{weather_data.get('city', '未知')}
- 温度：{weather_data.get('temperature', '未知')}°C
- 体感温度：{weather_data.get('feels_like', '未知')}°C
- 天气状况：{weather_data.get('description', '未知')}
- 湿度：{weather_data.get('humidity', '未知')}%
- 风速：{weather_data.get('wind_speed', '未知')} km/h
- 风向：{weather_data.get('wind_direction', '未知')}
- 能见度：{weather_data.get('visibility', '未知')} km
- 气压：{weather_data.get('pressure', '未知')} hPa
- 更新时间：{weather_data.get('update_time', '未知')}
"""

        news_text = "**热点新闻：**\n"
        for i, news in enumerate(news_data[:5], 1):
            news_text += f"{i}. {news.get('title', '未知标题')}\n"
            news_text += f"   来源：{news.get('source', '未知')} | 分类：{news.get('category', '未知')}\n"
            news_text += f"   摘要：{news.get('summary', '无摘要')}\n\n"

        prompt = f"""
请根据以下天气信息和热点新闻，生成一份简洁的汇总报告。

**输出要求：**
1. 直接输出markdown格式的汇总报告
2. 报告结构必须包含以下三个部分：
   - ## 今日天气概况
   - ## 热点新闻聚焦  
   - ## 生活工作建议
3. 语言简洁明了，突出重点信息
4. 总字数控制在300字以内
5. 使用规范的markdown语法
6. 不要包含任何分析过程、思维链、思考过程或过渡语句
7. 不要使用"根据以上信息"、"基于天气和新闻"、"现在构思具体内容"等表述
8. 不要输出"我会把这些内容组织成简洁的段落"等思考过程
9. 直接输出结果，不要解释或说明
10. 不要包含任何模型思考、构思或分析步骤

**输入信息：**

{weather_text}

{news_text}

请直接输出markdown格式的汇总报告：
"""
        
        return prompt

    def _generate_fallback_summary(self, weather_data, news_data):
        """
        当Ollama调用失败时的备用汇总方案
        """
        city = weather_data.get('city', '当前城市')
        temp = weather_data.get('temperature', '未知')
        weather_desc = weather_data.get('description', '未知')
        humidity = weather_data.get('humidity', '未知')
        wind_speed = weather_data.get('wind_speed', '未知')
        
        news_titles = [news.get('title', '') for news in news_data[:3]]
        
        summary = f"""# AI智能汇总报告

## 今日天气概况

{city}今日天气{weather_desc}，气温{temp}°C，湿度{humidity}%，风速{wind_speed}km/h。

## 热点新闻聚焦

{chr(10).join([f"• {title}" for title in news_titles if title])}

## 生活工作建议

根据天气情况合理安排出行，关注热点新闻动态，保持信息敏感度。"""
        
        return summary
    
    def test_connection(self):
        """
        测试Ollama连接
        """
        try:
            # 尝试列出可用模型
            models = self.client.list()
            print(f"可用模型: {[model['name'] for model in models['models']]}")
            return True
        except Exception as e:
            print(f"Ollama连接测试失败: {e}")
            return False 