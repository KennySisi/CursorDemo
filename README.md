# DevOps CI/CD 演示项目 🚀

一个完整的DevOps CI/CD演示项目，展示了如何使用现代技术栈构建自动化的软件交付流水线。

[![Build Status](https://dev.azure.com/your-org/devops-demo/_apis/build/status/application-pipeline?branchName=main)](https://dev.azure.com/your-org/devops-demo/_build/latest?definitionId=&branchName=main)
[![Infrastructure](https://dev.azure.com/your-org/devops-demo/_apis/build/status/infrastructure-pipeline?branchName=main)](https://dev.azure.com/your-org/devops-demo/_build/latest?definitionId=&branchName=main)

## 📖 项目概述

这个项目演示了一个完整的DevOps工作流程，包括：

- **应用程序**: 基于Python FastAPI的RESTful API
- **容器化**: Docker镜像构建和管理
- **基础设施即代码**: 使用Terraform管理Azure资源
- **CI/CD流水线**: Azure DevOps自动化部署
- **监控和日志**: Application Insights集成

## 🏗️ 技术栈

### 应用技术
- **Python 3.11** - 编程语言
- **FastAPI** - Web框架
- **Pydantic** - 数据验证
- **Uvicorn** - ASGI服务器
- **Pytest** - 测试框架

### DevOps工具
- **Docker** - 容器化
- **Terraform** - 基础设施即代码
- **Azure DevOps** - CI/CD平台
- **Azure App Service** - 应用托管
- **Application Insights** - 监控和分析

### 代码质量
- **Black** - 代码格式化
- **Flake8** - 代码质量检查
- **MyPy** - 类型检查
- **Pytest-cov** - 代码覆盖率

## 🚀 快速开始

### 本地开发

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd devops-demo

# 2. 设置Python环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行应用
uvicorn app.main:app --reload

# 5. 访问API文档
# http://localhost:8000/docs
```

### Docker运行

```bash
# 构建并运行
docker-compose up --build

# 仅运行应用
docker build -t devops-demo-api .
docker run -p 8000:8000 devops-demo-api
```

## 📊 API端点

### 核心端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | API首页 |
| GET | `/health` | 健康检查 |
| GET | `/docs` | API文档 |

### 用户管理

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/users` | 获取用户列表 |
| POST | `/users` | 创建新用户 |
| GET | `/users/{id}` | 获取指定用户 |
| DELETE | `/users/{id}` | 删除用户 |

### 示例请求

```bash
# 健康检查
curl http://localhost:8000/health

# 创建用户
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "email": "zhangsan@example.com"}'

# 获取用户
curl http://localhost:8000/users/1
```

## 🔄 CI/CD 流程

### 分支策略

```
main (生产环境)
  ↑
develop (测试环境)
  ↑
feature/* (功能分支)
```

### Pipeline架构

#### 应用程序Pipeline
```
触发 → 代码质量检查 → 单元测试 → Docker构建 → 部署Staging → 部署生产
```

#### 基础设施Pipeline
```
触发 → Terraform验证 → Plan → 审批 → Apply → 输出
```

### 自动化流程

1. **功能开发**: `feature/*` → `develop`
   - 自动运行测试
   - 部署到staging环境

2. **生产发布**: `develop` → `main`
   - 全面测试验证
   - 需要手动审批
   - 部署到生产环境

3. **基础设施变更**: 修改`terraform/*`
   - Terraform格式验证
   - Plan阶段预览
   - 生产环境需审批

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_main.py

# 生成覆盖率报告
pytest --cov=app --cov-report=html

# 运行烟雾测试
python tests/smoke_tests.py http://localhost:8000

# 运行生产测试
python tests/production_tests.py https://your-app.azurewebsites.net
```

### 测试类型

- **单元测试**: 测试单个函数和类
- **集成测试**: 测试API端点
- **烟雾测试**: 部署后的基本功能验证
- **生产测试**: 生产环境的完整功能测试

## 🏗️ 基础设施

### Azure资源

- **Resource Group**: 资源组织
- **App Service Plan**: 计算资源
- **App Service**: Web应用托管
- **Application Insights**: 监控和日志
- **Storage Account**: Terraform状态存储

### Terraform模块

```
terraform/
├── main.tf          # 主要资源定义
├── variables.tf     # 变量定义
├── outputs.tf       # 输出定义
└── terraform.tfvars # 变量值（需要创建）
```

## 📈 监控

### Application Insights集成

- 自动收集性能指标
- 请求追踪和依赖监控
- 错误和异常捕获
- 自定义事件和指标

### 健康检查

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "environment": "production"
}
```

## 🔧 配置

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `ENVIRONMENT` | 运行环境 | `development` |
| `PORT` | 服务端口 | `8000` |

### 开发配置

创建 `.env` 文件：

```env
ENVIRONMENT=development
DEBUG=true
```

## 📁 项目结构

```
devops-demo/
├── app/                          # 应用程序代码
│   ├── __init__.py
│   └── main.py                   # FastAPI应用
├── tests/                        # 测试文件
│   ├── __init__.py
│   ├── test_main.py             # 单元测试
│   ├── smoke_tests.py           # 烟雾测试
│   └── production_tests.py      # 生产测试
├── terraform/                    # Terraform配置
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── docs/                         # 项目文档
│   └── DEPLOYMENT_GUIDE.md      # 部署指南
├── azure-pipelines-*.yml        # Azure DevOps Pipeline
├── Dockerfile                    # Docker配置
├── docker-compose.yml           # 本地开发环境
├── requirements.txt             # Python依赖
├── pyproject.toml              # 现代Python配置
├── setup.py                    # Python包配置
└── README.md                   # 项目说明
```

## 🚀 部署指南

详细的部署步骤请参考 [部署指南](docs/DEPLOYMENT_GUIDE.md)。

### 快速部署检查清单

- [ ] Azure订阅和权限
- [ ] Azure DevOps项目
- [ ] Service Connections配置
- [ ] Variable Groups创建
- [ ] Terraform状态存储
- [ ] Pipeline配置
- [ ] 环境设置

## 🤝 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发规范

- 遵循PEP 8代码风格
- 编写测试用例
- 更新文档
- 使用语义化版本

## 📄 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 支持

如果你有任何问题或需要帮助：

1. 查看 [部署指南](docs/DEPLOYMENT_GUIDE.md)
2. 检查 [Issues](https://github.com/your-org/devops-demo/issues)
3. 创建新的 Issue

## 🔗 相关链接

- [Azure DevOps](https://dev.azure.com/)
- [Terraform Registry](https://registry.terraform.io/)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Docker Hub](https://hub.docker.com/)

---

**注意**: 这是一个演示项目，用于学习和教育目的。在生产环境中使用时请确保遵循安全最佳实践。