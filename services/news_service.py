import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

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

    def get_news(self, limit: int = 10, city: str = None) -> List[Dict]:
        """
        获取热点新闻，支持按城市相关程度排序
        """
        try:
            response = requests.get(self.api_url, params=self.params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('result', {}).get('status', {}).get('code') == 0:
                news_list = []
                items = data.get('result', {}).get('data', [])
                
                for item in items[:limit * 2]:  # 获取更多新闻用于筛选
                    # 确保URL是有效的
                    news_url = item.get('url', '')
                    if not news_url or news_url == '#':
                        # 如果没有有效URL，尝试构建一个
                        news_url = f"https://news.sina.com.cn/roll/#pageid=153&lid=2509&num=1&page=1&r={datetime.now().timestamp()}"

                    news_item = {
                        'title': item.get('title', ''),
                        'url': news_url,
                        'summary': item.get('intro', ''),
                        'source': '新浪新闻',
                        'publish_time': item.get('ctime', ''),
                        'category': item.get('category', '热点'),
                        'relevance_score': 0,  # 默认相关程度
                        'relevance_level': '一般'  # 默认相关级别
                    }
                    
                    # 如果指定了城市，计算相关程度
                    if city:
                        relevance_info = self._calculate_relevance(news_item, city)
                        news_item['relevance_score'] = relevance_info['score']
                        news_item['relevance_level'] = relevance_info['level']
                    
                    news_list.append(news_item)
                
                # 如果指定了城市，按相关程度排序
                if city:
                    news_list.sort(key=lambda x: x['relevance_score'], reverse=True)
                
                return news_list[:limit]
            else:
                print("获取新闻失败，使用模拟数据")
                return self._get_mock_news(limit, city)
                
        except Exception as e:
            print(f"获取新闻信息时出错: {e}")
            return self._get_mock_news(limit, city)

    def get_news_content(self, url: str) -> Dict:
        """
        从新闻链接中提取正文内容
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尝试多种选择器来提取正文
            content_selectors = [
                '.article-content',
                '.article-body',
                '.content',
                '.main-content',
                '.article',
                '.news-content',
                '#artibody',
                '.article-content-left',
                '.article-body-content'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = elements[0].get_text(strip=True)
                    break
            
            # 如果没有找到特定选择器，尝试提取所有段落
            if not content:
                paragraphs = soup.find_all('p')
                content = '\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
            
            # 清理内容
            content = self._clean_content(content)
            
            # 提取标题
            title_selectors = [
                'h1',
                '.article-title',
                '.title',
                '.headline',
                '.article-headline'
            ]
            
            title = ""
            for selector in title_selectors:
                elements = soup.select(selector)
                if elements:
                    title = elements[0].get_text(strip=True)
                    break
            
            if not title:
                title = soup.find('title')
                title = title.get_text(strip=True) if title else "未知标题"
            
            return {
                'success': True,
                'title': title,
                'content': content,
                'url': url,
                'length': len(content)
            }
            
        except Exception as e:
            print(f"提取新闻内容失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'title': '',
                'content': '',
                'url': url,
                'length': 0
            }

    def _clean_content(self, content: str) -> str:
        """
        清理新闻内容
        """
        if not content:
            return ""
        
        # 移除多余的空白字符
        content = re.sub(r'\s+', ' ', content)
        
        # 移除常见的无关文本
        patterns_to_remove = [
            r'点击查看详情',
            r'相关阅读',
            r'更多精彩内容',
            r'关注我们',
            r'分享到',
            r'责任编辑',
            r'编辑：',
            r'作者：',
            r'来源：',
            r'发布时间：',
            r'阅读量：',
            r'点赞数：',
            r'评论数：'
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # 限制内容长度
        if len(content) > 5000:
            content = content[:5000] + "..."
        
        return content.strip()

    def _calculate_relevance(self, news_item: Dict, city: str) -> Dict:
        """
        计算新闻与城市的相关程度
        """
        if not city or city not in self.city_keywords:
            return {'score': 0, 'level': '一般'}
        
        city_keywords = self.city_keywords[city]
        title = news_item.get('title', '').lower()
        summary = news_item.get('summary', '').lower()
        
        score = 0
        matched_keywords = []
        
        for keyword in city_keywords:
            keyword_lower = keyword.lower()
            # 标题匹配权重更高
            if keyword_lower in title:
                score += 3
                matched_keywords.append(keyword)
            # 摘要匹配权重较低
            if keyword_lower in summary:
                score += 1
                if keyword not in matched_keywords:
                    matched_keywords.append(keyword)
        
        # 根据分数确定相关级别
        if score >= 6:
            level = '高度相关'
        elif score >= 3:
            level = '相关'
        elif score >= 1:
            level = '一般相关'
        else:
            level = '一般'
        
        return {
            'score': score,
            'level': level,
            'matched_keywords': matched_keywords
        }

    def filter_news_by_city(self, news_list: List[Dict], city: str) -> List[Dict]:
        """
        根据城市筛选相关新闻（已废弃，使用get_news的city参数）
        """
        # 为每条新闻计算相关程度
        for news in news_list:
            relevance_info = self._calculate_relevance(news, city)
            news['relevance_score'] = relevance_info['score']
            news['relevance_level'] = relevance_info['level']
        
        # 按相关程度排序
        news_list.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # 返回前5条相关新闻，如果没有相关新闻则返回前3条
        relevant_news = [news for news in news_list if news['relevance_score'] > 0]
        if relevant_news:
            return relevant_news[:5]
        else:
            return news_list[:3]

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
        
        # 为每条新闻计算相关程度
        for news in news_list:
            relevance_info = self._calculate_relevance(news, city)
            news['relevance_score'] = relevance_info['score']
            news['relevance_level'] = relevance_info['level']
        
        # 按相关程度排序
        news_list.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        relevant_news = [news for news in news_list if news['relevance_score'] > 0]
        
        return {
            'relevant_count': len(relevant_news),
            'total_count': len(news_list),
            'relevance_rate': len(relevant_news) / len(news_list) if news_list else 0,
            'relevant_news': news_list[:5]  # 返回排序后的前5条
        }

    def _get_mock_news(self, limit: int = 10, city: str = None) -> List[Dict]:
        """
        获取模拟新闻数据，支持相关程度计算
        """
        mock_news = [
            {
                'title': '人工智能技术发展迅速，ChatGPT引领AI革命',
                'url': 'https://news.sina.com.cn/tech/2024/01/15/ai-development.html',
                'summary': '人工智能技术在全球范围内快速发展，ChatGPT等大语言模型引领AI革命，推动各行业数字化转型。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 10:30:00',
                'category': '科技',
                'relevance_score': 0,
                'relevance_level': '一般'
            },
            {
                'title': '新能源汽车销量持续增长，绿色出行成为趋势',
                'url': 'https://news.sina.com.cn/auto/2024/01/15/ev-sales-growth.html',
                'summary': '新能源汽车市场持续火爆，销量大幅增长，绿色出行理念深入人心，推动汽车产业转型升级。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 09:15:00',
                'category': '汽车',
                'relevance_score': 0,
                'relevance_level': '一般'
            },
            {
                'title': '北京科技创新中心建设加速推进',
                'url': 'https://news.sina.com.cn/tech/2024/01/15/beijing-innovation.html',
                'summary': '北京作为全国科技创新中心，正在加速推进各项创新项目，吸引全球顶尖人才和科技企业。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 08:45:00',
                'category': '科技',
                'relevance_score': 0,
                'relevance_level': '一般'
            },
            {
                'title': '上海自贸区深化改革，营商环境持续优化',
                'url': 'https://news.sina.com.cn/finance/2024/01/15/shanghai-ftz.html',
                'summary': '上海自贸区深化改革措施不断，营商环境持续优化，吸引更多外资企业投资兴业。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 08:20:00',
                'category': '财经',
                'relevance_score': 0,
                'relevance_level': '一般'
            },
            {
                'title': '广州数字经济蓬勃发展，智慧城市建设提速',
                'url': 'https://news.sina.com.cn/tech/2024/01/15/guangzhou-digital.html',
                'summary': '广州数字经济蓬勃发展，智慧城市建设全面提速，为城市发展注入新动能。',
                'source': '新浪新闻',
                'publish_time': '2024-01-15 07:55:00',
                'category': '科技',
                'relevance_score': 0,
                'relevance_level': '一般'
            }
        ]
        
        # 如果指定了城市，计算相关程度并排序
        if city:
            for news in mock_news:
                relevance_info = self._calculate_relevance(news, city)
                news['relevance_score'] = relevance_info['score']
                news['relevance_level'] = relevance_info['level']
            
            mock_news.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return mock_news[:limit] 