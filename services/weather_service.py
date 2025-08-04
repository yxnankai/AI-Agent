import requests
import json
from datetime import datetime
import re

class WeatherService:
    def __init__(self):
        # 使用免费的天气API
        self.base_url = "http://wttr.in"
        
        # 中国主要城市列表
        self.chinese_cities = {
            '北京': 'Beijing',
            '上海': 'Shanghai',
            '广州': 'Guangzhou',
            '深圳': 'Shenzhen',
            '杭州': 'Hangzhou',
            '南京': 'Nanjing',
            '武汉': 'Wuhan',
            '成都': 'Chengdu',
            '重庆': 'Chongqing',
            '西安': 'Xian',
            '天津': 'Tianjin',
            '青岛': 'Qingdao',
            '大连': 'Dalian',
            '厦门': 'Xiamen',
            '苏州': 'Suzhou',
            '无锡': 'Wuxi',
            '宁波': 'Ningbo',
            '长沙': 'Changsha',
            '郑州': 'Zhengzhou',
            '济南': 'Jinan',
            '福州': 'Fuzhou',
            '合肥': 'Hefei',
            '南昌': 'Nanchang',
            '太原': 'Taiyuan',
            '石家庄': 'Shijiazhuang',
            '哈尔滨': 'Harbin',
            '长春': 'Changchun',
            '沈阳': 'Shenyang',
            '呼和浩特': 'Hohhot',
            '银川': 'Yinchuan',
            '兰州': 'Lanzhou',
            '西宁': 'Xining',
            '乌鲁木齐': 'Urumqi',
            '拉萨': 'Lhasa',
            '昆明': 'Kunming',
            '贵阳': 'Guiyang',
            '南宁': 'Nanning',
            '海口': 'Haikou',
            '三亚': 'Sanya',
            '珠海': 'Zhuhai',
            '佛山': 'Foshan',
            '东莞': 'Dongguan',
            '中山': 'Zhongshan',
            '惠州': 'Huizhou',
            '江门': 'Jiangmen',
            '肇庆': 'Zhaoqing',
            '清远': 'Qingyuan',
            '韶关': 'Shaoguan',
            '河源': 'Heyuan',
            '梅州': 'Meizhou',
            '汕尾': 'Shanwei',
            '揭阳': 'Jieyang',
            '潮州': 'Chaozhou',
            '汕头': 'Shantou',
            '湛江': 'Zhanjiang',
            '茂名': 'Maoming',
            '阳江': 'Yangjiang',
            '云浮': 'Yunfu',
            '徐州': 'Xuzhou',
            '常州': 'Changzhou',
            '南通': 'Nantong',
            '扬州': 'Yangzhou',
            '镇江': 'Zhenjiang',
            '泰州': 'Taizhou',
            '盐城': 'Yancheng',
            '连云港': 'Lianyungang',
            '宿迁': 'Suqian',
            '淮安': 'Huaian',
            '金华': 'Jinhua',
            '温州': 'Wenzhou',
            '嘉兴': 'Jiaxing',
            '湖州': 'Huzhou',
            '绍兴': 'Shaoxing',
            '台州': 'Taizhou',
            '丽水': 'Lishui',
            '衢州': 'Quzhou',
            '舟山': 'Zhoushan',
            '泉州': 'Quanzhou',
            '漳州': 'Zhangzhou',
            '莆田': 'Putian',
            '三明': 'Sanming',
            '南平': 'Nanping',
            '龙岩': 'Longyan',
            '宁德': 'Ningde',
            '芜湖': 'Wuhu',
            '蚌埠': 'Bengbu',
            '淮南': 'Huainan',
            '马鞍山': 'Maanshan',
            '淮北': 'Huaibei',
            '铜陵': 'Tongling',
            '安庆': 'Anqing',
            '黄山': 'Huangshan',
            '滁州': 'Chuzhou',
            '阜阳': 'Fuyang',
            '宿州': 'Suzhou',
            '六安': 'Luan',
            '亳州': 'Bozhou',
            '池州': 'Chizhou',
            '宣城': 'Xuancheng',
            '景德镇': 'Jingdezhen',
            '萍乡': 'Pingxiang',
            '九江': 'Jiujiang',
            '新余': 'Xinyu',
            '鹰潭': 'Yingtan',
            '赣州': 'Ganzhou',
            '吉安': 'Jian',
            '宜春': 'Yichun',
            '抚州': 'Fuzhou',
            '上饶': 'Shangrao',
            '大同': 'Datong',
            '阳泉': 'Yangquan',
            '长治': 'Changzhi',
            '晋城': 'Jincheng',
            '朔州': 'Shuozhou',
            '晋中': 'Jinzhong',
            '运城': 'Yuncheng',
            '忻州': 'Xinzhou',
            '临汾': 'Linfen',
            '吕梁': 'Luliang',
            '包头': 'Baotou',
            '乌海': 'Wuhai',
            '赤峰': 'Chifeng',
            '通辽': 'Tongliao',
            '鄂尔多斯': 'Ordos',
            '呼伦贝尔': 'Hulunbuir',
            '巴彦淖尔': 'Bayannur',
            '乌兰察布': 'Ulanqab',
            '兴安盟': 'Xinganmeng',
            '锡林郭勒': 'Xilingol',
            '阿拉善': 'Alxa',
            '鞍山': 'Anshan',
            '抚顺': 'Fushun',
            '本溪': 'Benxi',
            '丹东': 'Dandong',
            '锦州': 'Jinzhou',
            '营口': 'Yingkou',
            '阜新': 'Fuxin',
            '辽阳': 'Liaoyang',
            '盘锦': 'Panjin',
            '铁岭': 'Tieling',
            '朝阳': 'Chaoyang',
            '葫芦岛': 'Huludao',
            '吉林市': 'Jilin',
            '四平': 'Siping',
            '辽源': 'Liaoyuan',
            '通化': 'Tonghua',
            '白山': 'Baishan',
            '松原': 'Songyuan',
            '白城': 'Baicheng',
            '延边': 'Yanbian',
            '齐齐哈尔': 'Qiqihar',
            '鸡西': 'Jixi',
            '鹤岗': 'Hegang',
            '双鸭山': 'Shuangyashan',
            '大庆': 'Daqing',
            '伊春': 'Yichun',
            '佳木斯': 'Jiamusi',
            '七台河': 'Qitaihe',
            '牡丹江': 'Mudanjiang',
            '黑河': 'Heihe',
            '绥化': 'Suihua',
            '大兴安岭': 'Daxinganling'
        }
        
    def get_weather(self, city="北京"):
        """
        获取指定城市的天气信息
        """
        try:
            # 处理城市名称
            processed_city = self._process_city_name(city)
            
            # 使用wttr.in API获取天气信息
            url = f"{self.base_url}/{processed_city}?format=j1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            weather_data = response.json()
            
            # 解析天气数据
            current_condition = weather_data['current_condition'][0]
            
            # 安全获取天气描述 - 修复显示问题
            weather_desc = '多云'  # 默认值
            try:
                # 优先使用中文描述
                if 'lang_zh' in current_condition and len(current_condition['lang_zh']) > 0:
                    lang_zh_item = current_condition['lang_zh'][0]
                    if isinstance(lang_zh_item, dict) and 'value' in lang_zh_item:
                        weather_desc = str(lang_zh_item['value'])
                    else:
                        weather_desc = str(lang_zh_item)
                # 备选英文描述
                elif 'weatherDesc' in current_condition and len(current_condition['weatherDesc']) > 0:
                    weather_desc_item = current_condition['weatherDesc'][0]
                    if isinstance(weather_desc_item, dict) and 'value' in weather_desc_item:
                        weather_desc = str(weather_desc_item['value'])
                    else:
                        weather_desc = str(weather_desc_item)
                # 备选天气图标描述
                elif 'weatherIconUrl' in current_condition and len(current_condition['weatherIconUrl']) > 0:
                    # 从图标URL提取天气描述
                    icon_url_item = current_condition['weatherIconUrl'][0]
                    if isinstance(icon_url_item, dict) and 'value' in icon_url_item:
                        icon_url = str(icon_url_item['value'])
                    else:
                        icon_url = str(icon_url_item)
                    
                    if 'sunny' in icon_url.lower():
                        weather_desc = '晴天'
                    elif 'cloudy' in icon_url.lower():
                        weather_desc = '多云'
                    elif 'rainy' in icon_url.lower():
                        weather_desc = '雨天'
                    elif 'snowy' in icon_url.lower():
                        weather_desc = '雪天'
                    else:
                        weather_desc = '多云'
            except Exception as e:
                print(f"解析天气描述时出错: {e}")
                weather_desc = '多云'
            
            # 确保所有字段都是字符串类型
            weather_info = {
                'city': str(city),
                'temperature': str(current_condition['temp_C']),
                'feels_like': str(current_condition['FeelsLikeC']),
                'humidity': str(current_condition['humidity']),
                'description': str(weather_desc),
                'wind_speed': str(current_condition['windspeedKmph']),
                'wind_direction': str(current_condition['winddir16Point']),
                'visibility': str(current_condition['visibility']),
                'pressure': str(current_condition['pressure']),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return weather_info
            
        except requests.RequestException as e:
            # 如果API调用失败，返回模拟数据
            return self._get_mock_weather(city)
        except Exception as e:
            print(f"获取天气信息时出错: {e}")
            return self._get_mock_weather(city)
    
    def _process_city_name(self, city):
        """
        处理城市名称，支持中文城市名转换为英文
        """
        # 移除可能的"省"、"市"等后缀
        city = re.sub(r'[省市自治区特别行政区]$', '', city.strip())
        
        # 检查是否在中文城市列表中
        if city in self.chinese_cities:
            return self.chinese_cities[city]
        
        # 如果不在列表中，直接返回原名称（API可能支持）
        return city
    
    def get_supported_cities(self):
        """
        获取支持的城市列表
        """
        return list(self.chinese_cities.keys())
    
    def _get_mock_weather(self, city):
        """返回模拟天气数据"""
        return {
            'city': city,
            'temperature': '22',
            'feels_like': '24',
            'humidity': '65',
            'description': '多云',
            'wind_speed': '15',
            'wind_direction': '东北',
            'visibility': '10',
            'pressure': '1013',
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'note': '模拟数据'
        } 