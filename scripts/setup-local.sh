#!/bin/bash

# DevOps Demo 本地环境设置脚本
# 用于快速设置本地开发环境

set -e  # 遇到错误时退出

echo "🚀 DevOps Demo 本地环境设置开始..."

# 检查必需工具
echo "📋 检查必需工具..."

check_tool() {
    if command -v $1 &> /dev/null; then
        echo "✅ $1 已安装"
    else
        echo "❌ $1 未安装，请先安装 $1"
        exit 1
    fi
}

check_tool python3
check_tool docker
check_tool git

# 检查Python版本
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo "✅ Python版本 $PYTHON_VERSION 符合要求"
else
    echo "❌ Python版本 $PYTHON_VERSION 不符合要求，需要 $REQUIRED_VERSION 或更高版本"
    exit 1
fi

# 创建Python虚拟环境
echo "🐍 创建Python虚拟环境..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ 虚拟环境创建成功"
else
    echo "ℹ️ 虚拟环境已存在"
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source .venv/bin/activate
echo "✅ 虚拟环境已激活"

# 升级pip
echo "📦 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📚 安装Python依赖..."
pip install -r requirements.txt
echo "✅ 依赖安装完成"

# 运行测试
echo "🧪 运行测试..."
pytest tests/ -v
echo "✅ 测试通过"

# 启动应用（后台）
echo "🌐 启动FastAPI应用..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
APP_PID=$!
echo "✅ 应用已启动，PID: $APP_PID"

# 等待应用启动
echo "⏳ 等待应用启动..."
sleep 5

# 测试应用
echo "🔍 测试应用端点..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 健康检查通过"
    echo "🎉 应用运行正常！"
    echo ""
    echo "📝 可用端点："
    echo "   - API文档: http://localhost:8000/docs"
    echo "   - 健康检查: http://localhost:8000/health"
    echo "   - API首页: http://localhost:8000/"
    echo ""
    echo "🛑 停止应用: kill $APP_PID"
else
    echo "❌ 健康检查失败"
    kill $APP_PID
    exit 1
fi

echo ""
echo "🎯 下一步："
echo "1. 查看API文档: http://localhost:8000/docs"
echo "2. 阅读部署指南: docs/DEPLOYMENT_GUIDE.md"
echo "3. 设置Azure DevOps环境"
echo ""
echo "🏁 本地环境设置完成！"