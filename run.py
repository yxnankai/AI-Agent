#!/usr/bin/env python3
"""
AI智能体应用启动脚本
"""

import os
import sys
from app import app
from services.ollama_service import OllamaService

def check_ollama():
    """检查Ollama服务是否可用"""
    try:
        ollama_service = OllamaService()
        if ollama_service.test_connection():
            print("✅ Ollama服务连接正常")
            return True
        else:
            print("❌ Ollama服务连接失败")
            return False
    except Exception as e:
        print(f"❌ Ollama服务检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 启动AI智能体应用...")
    
    # 检查Ollama服务
    print("🔍 检查Ollama服务...")
    ollama_available = check_ollama()
    
    if not ollama_available:
        print("⚠️  警告: Ollama服务不可用，将使用备用汇总方案")
        print("💡 提示: 请确保Ollama已安装并运行在 http://localhost:11434")
        print("💡 安装指南: https://ollama.ai/")
    
    # 启动Flask应用
    print("🌐 启动Web服务器...")
    print("📱 访问地址: http://localhost:5000")
    print("🛑 按 Ctrl+C 停止服务")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 