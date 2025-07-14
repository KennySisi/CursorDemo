# DevOps CI/CD 演示项目部署指南

这是一个完整的DevOps CI/CD演示项目，展示了如何使用Azure DevOps、Terraform、Docker等现代技术栈构建自动化的软件交付流水线。

## 🎯 项目架构

```
DevOps Demo Project
├── 应用层 (FastAPI + Python)
├── 容器化 (Docker)
├── 基础设施 (Terraform + Azure)
├── CI/CD (Azure DevOps Pipelines)
└── 监控 (Application Insights)
```

## 📋 前置条件

### 1. Azure 账户和订阅
- 有效的Azure订阅
- 具有足够权限创建资源的账户

### 2. Azure DevOps 组织和项目
- Azure DevOps组织
- 已创建的项目

### 3. 本地开发环境
```bash
# 必需工具
- Python 3.11+
- Docker Desktop
- Git
- Azure CLI
- Terraform CLI
- Visual Studio Code (推荐)
```

## 🚀 第一阶段：本地开发环境搭建

### 步骤1：克隆并设置项目

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd devops-demo

# 2. 创建Python虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行本地测试
pytest tests/

# 5. 启动本地服务
uvicorn app.main:app --reload
```

### 步骤2：验证本地环境

```bash
# 访问API文档
curl http://localhost:8000/docs

# 测试健康检查
curl http://localhost:8000/health

# 运行完整测试套件
pytest tests/ -v --cov=app
```

### 步骤3：Docker本地测试

```bash
# 构建Docker镜像
docker build -t devops-demo-api .

# 运行容器
docker run -p 8000:8000 devops-demo-api

# 或使用docker-compose
docker-compose up --build
```

## 🏗️ 第二阶段：Azure基础设施准备

### 步骤1：Azure CLI登录

```bash
# 登录Azure
az login

# 设置默认订阅
az account set --subscription "your-subscription-id"

# 验证登录状态
az account show
```

### 步骤2：创建Service Principal

```bash
# 创建用于Terraform的Service Principal
az ad sp create-for-rbac \
  --name "terraform-devops-demo" \
  --role="Contributor" \
  --scopes="/subscriptions/{subscription-id}"

# 记录输出信息：
# - appId (客户端ID)
# - password (客户端密钥)
# - tenant (租户ID)
```

### 步骤3：创建Terraform状态存储

```bash
# 创建资源组
az group create \
  --name terraform-state-rg \
  --location "East Asia"

# 创建存储账户
az storage account create \
  --name terraformstate$(date +%s) \
  --resource-group terraform-state-rg \
  --location "East Asia" \
  --sku Standard_LRS \
  --encryption-services blob

# 创建容器
az storage container create \
  --name tfstate \
  --account-name terraformstate$(date +%s)
```

### 步骤4：配置Terraform变量

```bash
# 复制示例变量文件
cp terraform/terraform.tfvars.example terraform/terraform.tfvars

# 编辑terraform.tfvars文件，填入实际值
# 注意：app_name必须全局唯一
```

## 🔧 第三阶段：Azure DevOps配置

### 步骤1：创建Service Connections

在Azure DevOps项目中：

1. **Azure Service Connection**
   - 进入 Project Settings → Service connections
   - 选择 "Azure Resource Manager"
   - 使用前面创建的Service Principal信息
   - 命名为 "azure-service-connection"

2. **Docker Registry Connection**
   - 选择 "Docker Registry"
   - 配置您的容器注册表（Azure ACR或Docker Hub）
   - 命名为 "docker-registry-connection"

### 步骤2：创建Variable Groups

1. **terraform-variables** 组：
```yaml
Variables:
  - TF_VAR_app_name: "your-unique-app-name"
  - TF_VAR_location: "East Asia"
  - TF_VAR_environment: "prod"
  - ARM_CLIENT_ID: "service-principal-app-id"
  - ARM_CLIENT_SECRET: "service-principal-password" (设为secret)
  - ARM_SUBSCRIPTION_ID: "your-subscription-id"
  - ARM_TENANT_ID: "your-tenant-id"
```

2. **application-variables** 组：
```yaml
Variables:
  - webAppName: "your-unique-app-name"
  - imageRepository: "devops-demo-api"
  - dockerRegistryUrl: "your-registry-url"
```

### 步骤3：创建Environments

1. **staging** 环境
   - 无需特殊审批
   - 自动部署

2. **production** 环境
   - 设置审批者
   - 配置部署时间窗口

3. **production-destroy** 环境
   - 需要多重审批
   - 仅用于销毁基础设施

### 步骤4：创建Pipelines

1. **基础设施Pipeline**
   - 创建新pipeline
   - 选择 "azure-pipelines-infrastructure.yml"
   - 配置触发器和变量

2. **应用程序Pipeline**
   - 创建新pipeline
   - 选择 "azure-pipelines-application.yml"
   - 配置触发器和变量

## 🚀 第四阶段：执行部署

### 步骤1：部署基础设施

```bash
# 手动触发基础设施pipeline
# 或推送terraform文件夹的更改来自动触发

# 验证Terraform计划
# 在main分支上审批并应用
```

### 步骤2：部署应用程序

```bash
# 推送代码到main分支触发CI/CD
git add .
git commit -m "feat: initial deployment"
git push origin main

# 监控pipeline执行
# 检查各个阶段的状态
```

### 步骤3：验证部署

```bash
# 获取应用URL（从Terraform输出）
az webapp show \
  --name your-app-name \
  --resource-group your-resource-group \
  --query defaultHostName

# 测试应用
curl https://your-app-name.azurewebsites.net/health

# 运行端到端测试
python tests/smoke_tests.py https://your-app-name.azurewebsites.net
```

## 🔄 日常运维流程

### 功能开发流程

1. **创建功能分支**
```bash
git checkout -b feature/new-feature
```

2. **开发和测试**
```bash
# 编写代码
# 运行本地测试
pytest tests/
```

3. **提交PR到develop**
```bash
git push origin feature/new-feature
# 创建PR到develop分支
```

4. **自动部署到staging**
```bash
# PR合并到develop后自动部署到staging
# 运行staging环境测试
```

5. **发布到生产**
```bash
# 创建PR从develop到main
# 合并后自动部署到生产环境
```

### 基础设施变更流程

1. **修改Terraform文件**
2. **创建PR并审查**
3. **合并后自动执行Terraform plan**
4. **在生产环境中审批apply**

### 回滚流程

1. **应用回滚**
```bash
# 通过Azure Portal回滚到之前的部署
# 或重新运行之前成功的pipeline
```

2. **基础设施回滚**
```bash
# 恢复Terraform文件到之前版本
# 重新运行infrastructure pipeline
```

## 📊 监控和日志

### Application Insights

- 自动收集应用性能数据
- 查看请求追踪和错误日志
- 设置警报规则

### Azure Monitor

- 监控基础设施健康状态
- 设置资源使用率警报
- 配置自动扩缩容

### 日志查看

```bash
# 查看应用日志
az webapp log tail \
  --name your-app-name \
  --resource-group your-resource-group

# 下载日志文件
az webapp log download \
  --name your-app-name \
  --resource-group your-resource-group
```

## 🔒 安全考虑

### 1. 密钥管理
- 使用Azure Key Vault存储敏感信息
- 在pipeline中使用secret变量
- 定期轮换密钥

### 2. 网络安全
- 配置网络安全组规则
- 使用HTTPS和SSL证书
- 实施最小权限原则

### 3. 镜像安全
- 定期扫描Docker镜像漏洞
- 使用受信任的基础镜像
- 及时更新依赖包

## 🎯 性能优化

### 1. 应用优化
- 启用API缓存
- 优化数据库查询
- 使用CDN加速静态资源

### 2. 基础设施优化
- 配置自动扩缩容
- 使用Azure Front Door
- 优化App Service计划

## 🔧 故障排除

### 常见问题

1. **Pipeline失败**
   - 检查service connection配置
   - 验证variable group变量
   - 查看详细错误日志

2. **Terraform错误**
   - 检查Azure权限
   - 验证状态文件锁定
   - 确认资源名称唯一性

3. **应用启动失败**
   - 检查Docker镜像构建
   - 验证环境变量配置
   - 查看应用日志

### 调试命令

```bash
# 检查应用状态
az webapp show --name your-app-name --resource-group your-rg

# 重启应用
az webapp restart --name your-app-name --resource-group your-rg

# 查看容器日志
az webapp log tail --name your-app-name --resource-group your-rg

# 测试网络连接
az webapp ssh --name your-app-name --resource-group your-rg
```

## 📚 进一步学习

### 推荐资源
- [Azure DevOps文档](https://docs.microsoft.com/azure/devops/)
- [Terraform Azure文档](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Docker最佳实践](https://docs.docker.com/develop/dev-best-practices/)

### 扩展功能
- 添加数据库持久化
- 实施蓝绿部署
- 集成自动化测试
- 添加性能监控
- 实现多环境管理

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request
5. 通过代码审查
6. 合并到主分支

---

**注意**: 这是一个演示项目，在生产环境中使用时请确保遵循您组织的安全策略和最佳实践。