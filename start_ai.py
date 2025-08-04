#!/usr/bin/env python3
"""
AI智能体启动器 - Python版本
避免批处理文件编码问题
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def check_python():
    """检查Python环境"""
    print("📦 检查Python环境...")
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    except Exception as e:
        print(f"❌ Python环境检查失败: {e}")
        return False

def check_dependencies():
    """检查依赖"""
    print("\n📦 检查依赖...")
    required_modules = ['flask', 'requests', 'ollama']
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} 已安装")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} 未安装")
    
    if missing_modules:
        print(f"\n🔧 正在安装缺失的依赖: {', '.join(missing_modules)}")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
            print("✅ 依赖安装完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖安装失败: {e}")
            return False
    
    return True

def check_ollama():
    """检查Ollama服务"""
    print("\n🔍 检查Ollama服务...")
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama未安装")
            return False
    except FileNotFoundError:
        print("❌ Ollama未安装")
        return False

def start_ollama_service():
    """启动Ollama服务"""
    print("\n🚀 启动Ollama服务...")
    try:
        # 检查Ollama是否已在运行
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama服务已运行")
            return True
        else:
            print("⚠️ Ollama服务未运行，请手动启动: ollama serve")
            return False
    except Exception as e:
        print(f"❌ Ollama服务检查失败: {e}")
        return False

def open_browser():
    """打开浏览器"""
    print("\n🎯 正在打开浏览器...")
    try:
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
        print("✅ 浏览器已打开")
        return True
    except Exception as e:
        print(f"❌ 打开浏览器失败: {e}")
        return False

def start_flask_app():
    """启动Flask应用"""
    print("\n🌐 启动Web服务器...")
    print("📱 访问地址: http://localhost:5000")
    print("🛑 按 Ctrl+C 停止服务")
    print()
    
    try:
        # 启动Flask应用
        subprocess.run([sys.executable, 'run.py'])
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")
    except Exception as e:
        print(f"❌ 启动Flask应用失败: {e}")

def create_desktop_shortcut():
    """创建桌面快捷方式"""
    try:
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "AI智能体.bat"
        
        # 获取当前脚本路径
        current_dir = Path(__file__).parent.absolute()
        
        # 创建批处理文件内容
        batch_content = f'''@echo off
chcp 65001 >nul
title AI智能体
cd /d "{current_dir}"
python start_ai.py
pause
'''
        
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ 桌面快捷方式已创建: {shortcut_path}")
        return True
    except Exception as e:
        print(f"❌ 创建快捷方式失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 AI智能体启动器")
    print("=" * 50)
    
    # 检查Python环境
    if not check_python():
        input("按回车键退出...")
        return
    
    # 检查依赖
    if not check_dependencies():
        input("按回车键退出...")
        return
    
    # 检查Ollama
    ollama_installed = check_ollama()
    if not ollama_installed:
        print("\n⚠️ Ollama未安装")
        print("请先运行 install_ollama.bat 安装Ollama")
        choice = input("是否继续启动应用? (y/n): ").lower()
        if choice != 'y':
            return
    
    # 启动Ollama服务
    if ollama_installed:
        start_ollama_service()
    
    # 创建桌面快捷方式
    create_desktop_shortcut()
    
    # 在新线程中打开浏览器
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # 启动Flask应用
    start_flask_app()

if __name__ == '__main__':
    main() 