@echo off
REM DevOps Demo Windows本地环境设置脚本

echo 🚀 DevOps Demo 本地环境设置开始...

REM 检查Python
echo 📋 检查Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装，请先安装Python 3.11+
    exit /b 1
) else (
    echo ✅ Python已安装
)

REM 检查Docker
echo 📋 检查Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker未安装，请先安装Docker Desktop
    exit /b 1
) else (
    echo ✅ Docker已安装
)

REM 创建虚拟环境
echo 🐍 创建Python虚拟环境...
if not exist ".venv" (
    python -m venv .venv
    echo ✅ 虚拟环境创建成功
) else (
    echo ℹ️ 虚拟环境已存在
)

REM 激活虚拟环境
echo 🔄 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 升级pip
echo 📦 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 📚 安装Python依赖...
pip install -r requirements.txt
echo ✅ 依赖安装完成

REM 运行测试
echo 🧪 运行测试...
pytest tests/ -v
if %errorlevel% neq 0 (
    echo ❌ 测试失败
    exit /b 1
)
echo ✅ 测试通过

REM 启动应用
echo 🌐 启动FastAPI应用...
start /b uvicorn app.main:app --host 0.0.0.0 --port 8000

REM 等待应用启动
echo ⏳ 等待应用启动...
timeout /t 5 /nobreak > nul

REM 测试应用
echo 🔍 测试应用端点...
curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 健康检查通过
    echo 🎉 应用运行正常！
    echo.
    echo 📝 可用端点：
    echo    - API文档: http://localhost:8000/docs
    echo    - 健康检查: http://localhost:8000/health
    echo    - API首页: http://localhost:8000/
    echo.
) else (
    echo ❌ 健康检查失败
    exit /b 1
)

echo 🎯 下一步：
echo 1. 查看API文档: http://localhost:8000/docs
echo 2. 阅读部署指南: docs\DEPLOYMENT_GUIDE.md
echo 3. 设置Azure DevOps环境
echo.
echo 🏁 本地环境设置完成！
pause