@echo off
chcp 65001 >nul
echo 🚀 AI智能体打包工具 - 修复版
echo =================================

echo.
echo 📦 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
)

echo.
echo 📦 检查pip...
python -m pip --version
if errorlevel 1 (
    echo ❌ pip不可用
    pause
    exit /b 1
)

echo.
echo 📦 安装PyInstaller...
python -m pip install pyinstaller
if errorlevel 1 (
    echo ❌ PyInstaller安装失败
    echo 尝试使用国内镜像源...
    python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller
    if errorlevel 1 (
        echo ❌ 安装失败，请检查网络连接
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller安装成功

echo.
echo 🧹 清理旧文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo 🔨 开始打包...
python -m PyInstaller --onefile --console --name "AI智能体" --add-data "templates;templates" --add-data "services;services" --add-data "config.py;." --add-data "app.py;." --add-data "run.py;." --hidden-import flask --hidden-import requests --hidden-import ollama --hidden-import beautifulsoup4 --hidden-import lxml --hidden-import feedparser --hidden-import python-dotenv app_launcher.py

if errorlevel 1 (
    echo ❌ 打包失败
    echo.
    echo 🔧 尝试简化打包...
    python -m PyInstaller --onefile --console --name "AI智能体" app_launcher.py
    if errorlevel 1 (
        echo ❌ 简化打包也失败
        pause
        exit /b 1
    )
)

echo.
echo ✅ 打包完成！
echo 📁 可执行文件位置: dist\AI智能体.exe
echo.

echo 🎯 创建桌面快捷方式...
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\AI智能体.bat"

echo @echo off > "%shortcut%"
echo cd /d "%CD%\dist" >> "%shortcut%"
echo "AI智能体.exe" >> "%shortcut%"
echo pause >> "%shortcut%"

echo ✅ 桌面快捷方式已创建: %shortcut%
echo.

echo 🎉 打包完成！现在您可以：
echo 1. 双击桌面上的"AI智能体.bat"启动应用
echo 2. 或直接运行 dist\AI智能体.exe
echo.

pause 