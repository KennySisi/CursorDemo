# DevOps Demo Makefile
# 简化常用开发操作

.PHONY: help install test lint format run docker-build docker-run clean

# 默认目标
help:
	@echo "DevOps Demo - 可用命令:"
	@echo ""
	@echo "  install      安装依赖"
	@echo "  test         运行测试"
	@echo "  test-cov     运行测试并生成覆盖率报告"
	@echo "  lint         代码质量检查"
	@echo "  format       代码格式化"
	@echo "  run          启动应用"
	@echo "  docker-build 构建Docker镜像"
	@echo "  docker-run   运行Docker容器"
	@echo "  docker-up    使用docker-compose启动"
	@echo "  smoke-test   运行烟雾测试"
	@echo "  clean        清理临时文件"
	@echo "  setup        设置开发环境"

# 设置开发环境
setup:
	@echo "🚀 设置开发环境..."
	python3 -m venv .venv
	@echo "请运行: source .venv/bin/activate (Linux/Mac) 或 .venv\\Scripts\\activate (Windows)"
	@echo "然后运行: make install"

# 安装依赖
install:
	@echo "📦 安装依赖..."
	pip install --upgrade pip
	pip install -r requirements.txt

# 运行测试
test:
	@echo "🧪 运行测试..."
	pytest tests/ -v

# 运行测试并生成覆盖率报告
test-cov:
	@echo "🧪 运行测试并生成覆盖率报告..."
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

# 代码质量检查
lint:
	@echo "🔍 代码质量检查..."
	black --check app/ tests/
	flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503
	mypy app/ --ignore-missing-imports

# 代码格式化
format:
	@echo "✨ 代码格式化..."
	black app/ tests/

# 启动应用
run:
	@echo "🌐 启动应用..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 构建Docker镜像
docker-build:
	@echo "🐳 构建Docker镜像..."
	docker build -t devops-demo-api .

# 运行Docker容器
docker-run: docker-build
	@echo "🐳 运行Docker容器..."
	docker run -p 8000:8000 devops-demo-api

# 使用docker-compose启动
docker-up:
	@echo "🐳 使用docker-compose启动..."
	docker-compose up --build

# 烟雾测试
smoke-test:
	@echo "🚀 运行烟雾测试..."
	python tests/smoke_tests.py http://localhost:8000

# 清理临时文件
clean:
	@echo "🧹 清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage

# 开发工作流
dev: install format lint test run

# CI工作流（模拟）
ci: install lint test test-cov docker-build

# 完整验证
verify: ci smoke-test