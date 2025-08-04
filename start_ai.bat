@echo off
chcp 65001 >nul
title AI智能体启动器

echo 🚀 AI智能体启动器
echo ========================
echo.

echo 📦 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境正常

echo.
echo 📦 检查依赖...
python -c "import flask, requests, ollama" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少依赖，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖检查通过

echo.
echo 🔍 检查Ollama服务...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Ollama未安装
    echo 请先运行 install_ollama.bat 安装Ollama
    echo.
    set /p choice="是否继续启动应用? (y/n): "
    if /i not "%choice%"=="y" (
        exit /b 1
    )
) else (
    echo ✅ Ollama已安装
)

echo.
echo 🌐 启动Web服务器...
echo 📱 访问地址: http://localhost:5000
echo 🛑 按 Ctrl+C 停止服务
echo.

echo 🎯 正在打开浏览器...
timeout /t 2 >nul
start http://localhost:5000

echo.
echo 🚀 启动AI智能体应用...
python run.py

pause 