import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

class NewsService:
    def __init__(self):
        self.api_url = "https://feed.mix.sina.com.cn/api/roll/get"
        self.params = {
            'pageid': '153',
            'lid': '2509',
            'num': '20',
            'page': '1',
            'r': str(datetime.now().timestamp())
        }
        
        # 城市关键词映射
        self.city_keywords = {
            '北京': ['北京', '首都', '京津冀', '华北', '中关村', '望京', '朝阳', '海淀'],
            '上海': ['上海', '魔都', '长三角', '华东', '浦东', '黄浦', '徐汇', '静安'],
            '广州': ['广州', '羊城', '珠三角', '华南', '天河', '越秀', '荔湾', '海珠'],
            '深圳': ['深圳', '鹏城', '珠三角', '华南', '南山', '福田', '罗湖', '宝安'],
            '杭州': ['杭州', '西湖', '浙江', '华东', '滨江', '余杭', '萧山'],
            '南京': ['南京', '金陵', '江苏', '华东', '鼓楼', '玄武', '秦淮'],
            '成都': ['成都', '蓉城', '四川', '西南', '锦江', '青羊', '武侯'],
            '重庆': ['重庆', '山城', '西南', '渝中', '江北', '南岸'],
            '武汉': ['武汉', '江城', '湖北', '华中', '武昌', '汉口', '汉阳'],
            '西安': ['西安', '古都', '陕西', '西北', '雁塔', '碑林', '莲湖'],
            '天津': ['天津', '津门', '华北', '和平', '河东', '河西'],
            '青岛': ['青岛', '山东', '华东', '市南', '市北', '李沧'],
            '大连': ['大连', '辽宁', '东北', '中山', '西岗', '沙河口'],
            '厦门': ['厦门', '福建', '华东', '思明', '湖里', '集美'],
            '苏州': ['苏州', '江苏', '华东', '姑苏', '吴中', '相城'],
            '无锡': ['无锡', '江苏', '华东', '梁溪', '锡山', '惠山'],
            '宁波': ['宁波', '浙江', '华东', '海曙', '江北', '北仑'],
            '长沙': ['长沙', '湖南', '华中', '芙蓉', '天心', '岳麓'],
            '郑州': ['郑州', '河南', '华中', '金水', '二七', '管城'],
            '济南': ['济南', '山东', '华东', '历下', '市中', '槐荫']
        }

    def get_news(self, limit: int = 10) -> List[Dict]:
        """
        获取热点新闻
        """
        try:
            response = requests.get(self.api_url, params=self.params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('result', {}).get('status', {}).get('code') == 0:
                news_list = []
                items = data.get('result', {}).get('data', [])
                
                for item in items[:limit]:
                    # 确保URL是有效的
                    news_url = item.get('url', '')
                    if not news_url or news_url == '#':
                        # 如果没有有效URL，尝试构建一个
                        news_url = f"https://news.sina.com.cn/roll/#pageid=153&lid=2509&num=1&page=1&r={datetime.now().timestamp()}"

                    news_list.append({
                        'title': item.get('title', ''),
                        'url': news_url,
                        'summary': item.get('intro', ''),
                        'source': '新浪新闻',
                        'publish_time': item.get('ctime', ''),
                        'category': item.get('category', '热点')
                    })
                
                return news_list
            else:
                print("获取新闻失败，使用模拟数据")
                return self._get_mock_news(limit)
                
        except Exception as e:
            print(f"获取新闻信息时出错: {e}")
            return self._get_mock_news(limit)

    def filter_news_by_city(self, news_list: List[Dict], city: str) -> List[Dict]:
        """
        根据城市筛选相关新闻
        """
        if not city or city not in self.city_keywords:
            return news_list[:5]  # 如果城市不在支持列表中，返回前5条
        
        city_keywords = self.city_keywords[city]
        relevant_news = []
        
        for news in news_list:
            title = news.get('title', '').lower()
            summary = news.get('summary', '').lower()
            
            # 检查标题和摘要中是否包含城市关键词
            is_relevant = any(keyword.lower() in title or keyword.lower() in summary 
                            for keyword in city_keywords)
            
            if is_relevant:
                relevant_news.append(news)
        
        # 如果没有找到相关新闻，返回前3条作为备选
        if not relevant_news:
            return news_list[:3]
        
        return relevant_news[:5]  # 最多返回5条相关新闻

    def analyze_news_relevance(self, news_list: List[Dict], city: str) -> Dict:
        """
        分析新闻与城市的相关性
        """
        if not city or city not in self.city_keywords:
            return {
                'relevant_count': 0,
                'total_count': len(news_list),
                'relevance_rate': 0,
                'relevant_news': news_list[:3]
            }
        
        city_keywords = self.city_keywords[city]
        relevant_news = []
        relevance_scores = []
        
        for news in news_list:
            title = news.get('title', '').lower()
            summary = news.get('summary', '').lower()
            
            # 计算相关性分数
            score = 0
            for keyword in city_keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in title:
                    score += 2  # 标题匹配权重更高
                if keyword_lower in summary:
                    score += 1  # 摘要匹配权重较低
            
            if score > 0:
                relevant_news.append(news)
                relevance_scores.append(score)
        
        # 按相关性分数排序
        if relevant_news:
            sorted_news = [x for _, x in sorted(zip(relevance_scores, relevant_news), reverse=True)]
        else:
            sorted_news = news_list[:3]  # 备选新闻
        
        return {
            'relevant_count': len(relevant_news),
            'total_count': len(news_list),
            'relevance_rate': len(relevant_news) / len(news_list) if news_list else 0,
            'relevant_news': sorted_news[:5]
        }

    def _get_mock_news(self, limit: int = 10) -> List[Dict]:
        """
        获取模拟新闻数据
        """
        mock_news = [
            {
                'title': '人工智能技术发展迅速，ChatGPT引领AI革命',
                'url': 'https://news.sina.com.cn/tech/2024/01/15/ai-development.html',
                'summary': '人工智能技术在全球范围内快速发展，ChatGPT等大语言模型引领AI革命，推动各行业数字化转型。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 10:30:00',
                'category': '科技'
            },
            {
                'title': '新能源汽车销量持续增长，绿色出行成为趋势',
                'url': 'https://news.sina.com.cn/auto/2024/01/15/ev-sales-growth.html',
                'summary': '新能源汽车市场持续火爆，销量大幅增长，绿色出行理念深入人心，推动汽车产业转型升级。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 09:15:00',
                'category': '汽车'
            },
            {
                'title': '北京科技创新中心建设加速推进',
                'url': 'https://news.sina.com.cn/tech/2024/01/15/beijing-innovation.html',
                'summary': '北京作为全国科技创新中心，正在加速推进各项创新项目，吸引全球顶尖人才和科技企业。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 08:45:00',
                'category': '科技'
            },
            {
                'title': '上海自贸区深化改革，营商环境持续优化',
                'url': 'https://news.sina.com.cn/finance/2024/01/15/shanghai-ftz.html',
                'summary': '上海自贸区深化改革措施不断，营商环境持续优化，吸引更多外资企业投资兴业。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 08:20:00',
                'category': '财经'
            },
            {
                'title': '广州数字经济蓬勃发展，智慧城市建设提速',
                'url': 'https://news.sina.com.cn/tech/2024/01/15/guangzhou-digital.html',
                'summary': '广州数字经济蓬勃发展，智慧城市建设全面提速，为城市发展注入新动能。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 07:55:00',
                'category': '科技'
            }
        ]
        
        return mock_news[:limit] 