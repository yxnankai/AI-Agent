from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from services.weather_service import WeatherService
from services.news_service import NewsService
from services.ollama_service import OllamaService

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 初始化服务
weather_service = WeatherService()
news_service = NewsService()
ollama_service = OllamaService()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/cities')
def get_cities():
    """获取支持的城市列表"""
    try:
        cities = weather_service.get_supported_cities()
        return jsonify({
            'success': True,
            'data': cities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/weather')
def get_weather():
    """获取天气信息API"""
    try:
        city = request.args.get('city', '北京')
        weather_data = weather_service.get_weather(city)
        return jsonify({
            'success': True,
            'data': weather_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news')
def get_news():
    """获取新闻信息API"""
    try:
        news_data = news_service.get_news()
        return jsonify({
            'success': True,
            'data': news_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/summary')
def get_summary():
    """获取AI汇总报告"""
    try:
        city = request.args.get('city', '北京')
        
        # 获取天气信息
        weather_data = weather_service.get_weather(city)
        
        # 获取新闻信息
        news_data = news_service.get_news(10)
        
        # 生成AI汇总，传递城市信息进行地域相关性分析
        summary = ollama_service.generate_summary(weather_data, news_data, city)
        
        return jsonify({
            'success': True,
            'data': {
                'summary': summary,
                'weather': weather_data,
                'news': news_data,
                'city': city
            }
        })
        
    except Exception as e:
        print(f"生成汇总报告时出错: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/models')
def get_models():
    """获取可用的Ollama模型列表"""
    try:
        models = ollama_service.get_available_models()
        return jsonify({
            'success': True,
            'data': models
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/set-model', methods=['POST'])
def set_model():
    """设置使用的模型"""
    try:
        data = request.get_json()
        model_name = data.get('model_name')
        
        if not model_name:
            return jsonify({
                'success': False,
                'error': '模型名称不能为空'
            }), 400
        
        success = ollama_service.set_model(model_name)
        
        return jsonify({
            'success': success,
            'message': f'模型已设置为: {model_name}' if success else '模型设置失败'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/current-model')
def get_current_model():
    """获取当前使用的模型"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'model_name': ollama_service.model_name
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 