@echo off
chcp 65001 >nul
echo 🚀 Ollama安装工具
echo ========================

echo.
echo 📦 检查Ollama是否已安装...
ollama --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Ollama已安装
    echo.
    echo 🎯 启动Ollama服务...
    start "" ollama serve
    echo ✅ Ollama服务已启动
    echo.
    echo 📝 提示：Ollama服务会在后台运行
    echo 您可以通过 http://localhost:11434 访问Ollama API
    pause
    exit /b 0
)

echo ❌ Ollama未安装
echo.
echo 📥 正在下载Ollama安装程序...
echo 请访问: https://ollama.ai/download
echo 下载Windows版本的Ollama安装程序
echo.
echo 🔧 安装步骤：
echo 1. 下载并运行Ollama安装程序
echo 2. 按照安装向导完成安装
echo 3. 安装完成后重新运行此脚本
echo.
echo 💡 或者您也可以使用以下命令安装：
echo winget install Ollama.Ollama
echo.

set /p choice="是否使用winget安装Ollama? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🔧 使用winget安装Ollama...
    winget install Ollama.Ollama
    if errorlevel 1 (
        echo ❌ 安装失败，请手动下载安装
    ) else (
        echo ✅ 安装完成
        echo.
        echo 🎯 启动Ollama服务...
        start "" ollama serve
        echo ✅ Ollama服务已启动
    )
) else (
    echo.
    echo 📝 请手动下载安装Ollama
    echo 下载地址: https://ollama.ai/download
)

echo.
echo 📚 安装完成后，您可以：
echo 1. 运行 "ollama pull qwen:latest" 下载模型
echo 2. 运行 "ollama list" 查看已安装的模型
echo 3. 启动AI智能体应用
echo.

pause 