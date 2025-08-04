# AI智能体

基于Ollama的智能信息聚合系统，集成天气查询、热点新闻和AI智能汇总功能。

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Ollama (本地大语言模型)
- 网络连接

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd AI-Agent
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **安装Ollama**
```bash
# Windows: 下载安装包
# Linux/Mac: curl -fsSL https://ollama.ai/install.sh | sh
```

4. **下载模型**
```bash
ollama pull qwen:latest
```

5. **启动应用**
```bash
python run.py
```

### 一键启动
```bash
# Windows
start_ai.bat

# 或使用Python启动器
python start_ai.py
```

## 📱 使用说明

1. 打开浏览器访问 `http://localhost:5000`
2. 选择城市或输入城市名称
3. 选择Ollama模型
4. 点击"获取AI汇总"按钮

## 🔧 核心功能

### 天气信息
- 实时天气数据获取
- 支持100+中国主要城市
- 温度、湿度、风速等详细信息

### 热点新闻
- 新浪新闻API实时获取
- 地域相关性智能分析
- 支持20个主要城市关键词匹配
- 新闻标题可点击跳转

### AI智能汇总
- 集成Ollama大语言模型
- 自动模型识别和选择
- 思维链优化，输出简洁直接
- 地域定制化新闻筛选

## 📊 项目结构

```
AI-Agent/
├── app.py                 # Flask主应用
├── run.py                 # 启动脚本
├── config.py              # 配置文件
├── services/              # 服务模块
│   ├── weather_service.py
│   ├── news_service.py
│   └── ollama_service.py
├── templates/             # 前端模板
│   └── index.html
├── test_all.py            # 综合测试脚本
├── test_services.py       # 服务测试
├── test_relevance_analysis.py # 地域相关性测试
├── requirements.txt       # 依赖列表
├── 项目完整说明.md        # 详细功能说明
└── README.md             # 项目说明
```

## 🧪 测试

### 运行综合测试
```bash
python test_all.py
```

### 运行服务测试
```bash
python test_services.py
```

### 运行地域相关性测试
```bash
python test_relevance_analysis.py
```

## 🔍 故障排除

### 常见问题

1. **Ollama连接失败**
```bash
ollama list
ollama serve
```

2. **天气数据异常**
- 检查网络连接
- 验证城市名称

3. **新闻获取失败**
- 检查新浪新闻API状态
- 验证网络连接

## 📈 功能特性

- ✅ 智能地域分析
- ✅ 思维链优化
- ✅ 安全数据解析
- ✅ 一键启动
- ✅ 响应式设计
- ✅ 模块化架构

## 🎯 应用场景

- 个人用户：日常天气查询、新闻浏览
- 商务用户：市场动态监控、地域信息分析
- 开发者：AI应用开发参考

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**AI智能体** - 让信息获取更智能、更便捷！🚀
