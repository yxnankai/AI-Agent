@echo off
chcp 65001 >nul
echo Creating Desktop Shortcut
echo ========================

echo.
echo Getting current directory...
set "current_dir=%CD%"
echo Current directory: %current_dir%

echo.
echo Getting desktop path...
set "desktop=%USERPROFILE%\Desktop"
echo Desktop path: %desktop%

echo.
echo Creating launcher shortcut...
set "shortcut=%desktop%\AI智能体.bat"

(
echo @echo off
echo chcp 65001 ^>nul
echo title AI智能体
echo.
echo echo 🚀 AI智能体启动中...
echo echo ========================
echo echo.
echo cd /d "%current_dir%"
echo.
echo echo 📦 检查Python环境...
echo python --version ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo ❌ Python未安装或不在PATH中
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo ✅ Python环境正常
echo echo.
echo echo 🔍 检查Ollama服务...
echo ollama --version ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo ⚠️ Ollama未安装，请先安装Ollama
echo     echo 运行 install_ollama.bat 安装Ollama
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo ✅ Ollama已安装
echo echo.
echo echo 🌐 启动Web服务器...
echo echo 📱 访问地址: http://localhost:5000
echo echo 🛑 按 Ctrl+C 停止服务
echo echo.
echo echo 🎯 正在打开浏览器...
echo timeout /t 2 ^>nul
echo start http://localhost:5000
echo echo.
echo echo 🚀 启动AI智能体应用...
echo python run.py
echo echo.
echo pause
) > "%shortcut%"

echo ✅ Desktop shortcut created: %shortcut%

echo.
echo 🎉 Shortcut creation completed!
echo Now you can:
echo 1. Double-click "AI智能体.bat" on desktop to start the app
echo 2. Or run simple_launcher.bat directly
echo.

echo 📝 Notes:
echo - Make sure Python is installed and added to PATH
echo - Make sure Ollama is installed and running
echo - First run may need to install dependencies
echo.

pause 