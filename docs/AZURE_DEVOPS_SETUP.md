# Azure DevOps 预设置指导

在开始使用CI/CD Pipeline之前，你需要在Azure DevOps中完成以下预设置。这个指导将帮你一步步完成所有必要的配置。

## 🏗️ 设置概览

```
Azure DevOps 设置流程
├── 1. 组织和项目创建
├── 2. 代码仓库设置
├── 3. Service Connections配置
├── 4. Variable Groups创建
├── 5. Environments环境设置
├── 6. 权限和安全配置
└── 7. Pipeline准备
```

## 📋 前置条件

### 必需账户和权限
- **Azure订阅** - 有效的Azure订阅
- **Azure DevOps账户** - Microsoft账户或工作/学校账户
- **权限** - Azure订阅的Contributor权限
- **权限** - Azure DevOps组织的Project Administrator权限

### 必需工具
- **Azure CLI** - 用于命令行操作
- **Web浏览器** - 用于Azure DevOps界面操作

## 🚀 第一步：创建Azure DevOps组织和项目

### 1.1 创建Azure DevOps组织

1. **访问Azure DevOps**
   ```
   https://dev.azure.com/
   ```

2. **创建新组织**
   - 点击"Create new organization"
   - 选择数据存储位置（建议选择距离最近的区域）
   - 输入组织名称（例如：`your-company-devops`）
   - 完成验证流程

3. **验证组织创建**
   - 确认组织URL：`https://dev.azure.com/{your-organization}`
   - 确认可以正常访问

### 1.2 创建项目

1. **在组织中创建项目**
   - 点击"Create project"
   - **项目名称**：`devops-demo`
   - **描述**：`DevOps CI/CD 演示项目`
   - **可见性**：Private（推荐）或Public
   - **版本控制**：Git
   - **工作项流程**：Agile

2. **项目设置验证**
   ```
   项目URL: https://dev.azure.com/{organization}/devops-demo
   ```

## 📁 第二步：代码仓库设置

### 2.1 导入或创建代码仓库

**选项A：从现有仓库导入**
1. 进入 Repos → Files
2. 点击"Import a repository"
3. 输入源仓库URL
4. 完成导入

**选项B：直接在Azure Repos创建**
1. 进入 Repos → Files
2. 使用Web界面上传项目文件
3. 或使用Git命令推送代码：

```bash
# 克隆空仓库
git clone https://dev.azure.com/{organization}/devops-demo/_git/devops-demo

# 添加项目文件
cd devops-demo
# 复制所有项目文件到此目录

# 推送到Azure Repos
git add .
git commit -m "Initial project setup"
git push origin main
```

### 2.2 分支策略设置

1. **进入分支策略设置**
   - Repos → Branches
   - 点击main分支的"..."菜单
   - 选择"Branch policies"

2. **配置分支保护策略**
   ```yaml
   分支策略建议：
   ✅ Require a minimum number of reviewers: 1
   ✅ Check for linked work items
   ✅ Check for comment resolution
   ✅ Limit merge types: Squash merge
   ✅ Build validation (稍后配置Pipeline后启用)
   ```

## 🔗 第三步：Service Connections配置

Service Connections是连接外部服务的关键配置。你需要配置以下连接：

### 3.1 Azure Resource Manager Service Connection

1. **进入Service Connections设置**
   ```
   Project Settings → Service connections → Create service connection
   ```

2. **选择连接类型**
   - 选择"Azure Resource Manager"
   - 选择"Service principal (automatic)"

3. **配置Azure连接**
   - **订阅**：选择你的Azure订阅
   - **资源组**：留空（表示全订阅权限）
   - **Service connection name**：`azure-service-connection`
   - **描述**：`Azure Resource Manager connection for DevOps Demo`
   - **安全设置**：
     - ✅ Grant access permission to all pipelines

4. **验证连接**
   - 保存后点击"Verify"确认连接正常

### 3.2 Docker Registry Service Connection

**选项A：Azure Container Registry (推荐)**

1. **创建Azure Container Registry**
   ```bash
   # 使用Azure CLI创建ACR
   az acr create \
     --resource-group devops-demo-rg \
     --name devopsdemoregistry$(date +%s) \
     --sku Basic \
     --admin-enabled
   
   # 获取登录凭据
   az acr credential show --name devopsdemoregistry$(date +%s)
   ```

2. **配置ACR Service Connection**
   - 选择"Docker Registry"
   - **Registry type**：Azure Container Registry
   - **Azure subscription**：选择你的订阅
   - **Azure container registry**：选择创建的ACR
   - **Service connection name**：`docker-registry-connection`

**选项B：Docker Hub**

1. **配置Docker Hub连接**
   - 选择"Docker Registry"
   - **Registry type**：Docker Hub
   - **Docker ID**：你的Docker Hub用户名
   - **Password**：你的Docker Hub密码或访问令牌
   - **Service connection name**：`docker-registry-connection`

### 3.3 验证Service Connections

确认以下连接已正确创建：
- ✅ `azure-service-connection` (Azure Resource Manager)
- ✅ `docker-registry-connection` (Docker Registry)

## 📦 第四步：Variable Groups创建

Variable Groups用于管理Pipeline中的变量和密钥。

### 4.1 创建 terraform-variables Group

1. **进入Variable Groups**
   ```
   Pipelines → Library → Variable groups → + Variable group
   ```

2. **基本设置**
   - **Variable group name**：`terraform-variables`
   - **描述**：`Terraform deployment variables`

3. **添加变量**
   ```yaml
   # Azure认证变量
   ARM_CLIENT_ID: "your-service-principal-app-id"
   ARM_CLIENT_SECRET: "your-service-principal-password" # 设为Secret
   ARM_SUBSCRIPTION_ID: "your-azure-subscription-id"
   ARM_TENANT_ID: "your-azure-tenant-id"
   
   # Terraform变量
   TF_VAR_app_name: "devops-demo-app-20240115" # 必须全局唯一
   TF_VAR_location: "East Asia"
   TF_VAR_environment: "prod"
   TF_VAR_app_service_sku: "B1"
   
   # Terraform后端配置
   backendResourceGroup: "terraform-state-rg"
   backendStorageAccount: "terraformstate20240115" # 替换为实际存储账户名
   backendContainerName: "tfstate"
   ```

4. **安全设置**
   - 将`ARM_CLIENT_SECRET`标记为Secret（点击变量右侧的锁图标）
   - ✅ Allow access to all pipelines

### 4.2 创建 application-variables Group

1. **创建新Variable Group**
   - **Variable group name**：`application-variables`
   - **描述**：`Application deployment variables`

2. **添加变量**
   ```yaml
   # 应用配置
   webAppName: "devops-demo-app-20240115" # 与TF_VAR_app_name相同
   imageRepository: "devops-demo-api"
   
   # Docker Registry配置（如果使用ACR）
   dockerRegistryUrl: "devopsdemoregistry20240115.azurecr.io"
   dockerRegistryUsername: "devopsdemoregistry20240115"
   dockerRegistryPassword: "your-acr-password" # 设为Secret
   
   # 或者Docker Hub配置
   # dockerRegistryUrl: "docker.io"
   # dockerRegistryUsername: "your-dockerhub-username"
   # dockerRegistryPassword: "your-dockerhub-password" # 设为Secret
   ```

3. **安全设置**
   - 将`dockerRegistryPassword`标记为Secret
   - ✅ Allow access to all pipelines

## 🌍 第五步：Environments设置

Environments用于管理不同的部署环境和审批流程。

### 5.1 创建 staging Environment

1. **进入Environments设置**
   ```
   Pipelines → Environments → Create environment
   ```

2. **配置staging环境**
   - **Name**：`staging`
   - **描述**：`Staging environment for testing`
   - **Resource**：None

3. **配置审批和检查**
   - 进入Environment → Approvals and checks
   - 可以选择添加：
     - **Pre-deployment approvals**：无（自动部署）
     - **Branch control**：仅允许develop分支部署

### 5.2 创建 production Environment

1. **配置production环境**
   - **Name**：`production`
   - **描述**：`Production environment`
   - **Resource**：None

2. **配置审批策略**
   - 进入Environment → Approvals and checks
   - 添加"Approvals"：
     - **Approvers**：添加你的账户或团队
     - **Advanced**：
       - ✅ Allow approvers to approve their own runs
       - **Timeout**：30 minutes
       - **Instructions**：请仔细检查变更内容后再批准部署

3. **可选：配置部署时间窗口**
   - 添加"Business hours"检查：
     - 设置允许部署的时间窗口
     - 例如：工作日 9:00-18:00

### 5.3 创建 production-destroy Environment

1. **配置销毁环境**
   - **Name**：`production-destroy`
   - **描述**：`Environment for infrastructure destruction - requires multiple approvals`

2. **配置严格审批**
   - 添加多个审批者
   - 设置更长的超时时间
   - 添加详细的审批说明

## 🔐 第六步：权限和安全配置

### 6.1 项目权限设置

1. **管理项目权限**
   ```
   Project Settings → Permissions
   ```

2. **关键权限验证**
   ```yaml
   Build Administrators:
   ✅ Edit build pipeline
   ✅ Queue builds
   ✅ Manage build qualities
   
   Release Administrators:
   ✅ Edit release pipeline
   ✅ Manage releases
   ✅ Manage deployment
   
   Project Administrators:
   ✅ Edit project-level information
   ✅ Manage service connections
   ✅ Manage variable groups
   ```

### 6.2 Service Connection权限

1. **验证Service Connection权限**
   - 进入每个Service Connection的Security设置
   - 确认Pipeline Service Account有使用权限
   - 确认User permissions正确设置

### 6.3 Agent Pool配置

1. **检查Agent Pool**
   ```
   Project Settings → Agent pools
   ```

2. **使用Microsoft-hosted agents**
   - 确认"Azure Pipelines"pool可用
   - 验证有足够的并行作业额度
   - 对于免费账户：1个并行作业

## 🔧 第七步：Azure CLI准备工作

在配置Azure DevOps之前，你需要先在Azure中创建一些资源。

### 7.1 创建Service Principal

```bash
# 登录Azure
az login

# 设置默认订阅
az account set --subscription "your-subscription-id"

# 创建Service Principal
az ad sp create-for-rbac \
  --name "devops-demo-terraform" \
  --role="Contributor" \
  --scopes="/subscriptions/{subscription-id}"

# 保存输出信息用于Variable Groups配置
# {
#   "appId": "your-app-id",           # 用作 ARM_CLIENT_ID
#   "displayName": "devops-demo-terraform",
#   "password": "your-password",      # 用作 ARM_CLIENT_SECRET
#   "tenant": "your-tenant-id"        # 用作 ARM_TENANT_ID
# }
```

### 7.2 创建Terraform状态存储

```bash
# 创建资源组
az group create \
  --name terraform-state-rg \
  --location "East Asia"

# 创建存储账户（名称必须全局唯一）
STORAGE_ACCOUNT_NAME="terraformstate$(date +%s)"
az storage account create \
  --name $STORAGE_ACCOUNT_NAME \
  --resource-group terraform-state-rg \
  --location "East Asia" \
  --sku Standard_LRS \
  --encryption-services blob

# 创建容器
az storage container create \
  --name tfstate \
  --account-name $STORAGE_ACCOUNT_NAME

# 记录存储账户名称，用于Variable Groups配置
echo "Storage Account Name: $STORAGE_ACCOUNT_NAME"
```

## 📝 第八步：Pipeline准备

### 8.1 Pipeline文件验证

确认以下Pipeline文件在代码仓库中：
- ✅ `azure-pipelines-infrastructure.yml`
- ✅ `azure-pipelines-application.yml`

### 8.2 创建Pipeline

1. **创建Infrastructure Pipeline**
   ```
   Pipelines → Pipelines → Create Pipeline
   ```
   - 选择"Azure Repos Git"
   - 选择你的仓库
   - 选择"Existing Azure Pipelines YAML file"
   - **Path**：`/azure-pipelines-infrastructure.yml`
   - **Name**：`Infrastructure Pipeline`

2. **创建Application Pipeline**
   - 重复上述步骤
   - **Path**：`/azure-pipelines-application.yml`
   - **Name**：`Application Pipeline`

3. **暂时不要运行Pipeline**
   - 选择"Save"而不是"Save and run"
   - 需要先完成所有配置

## ✅ 配置验证清单

在开始运行Pipeline之前，确认以下项目都已完成：

### Azure DevOps基础设置
- [ ] Azure DevOps组织已创建
- [ ] 项目"devops-demo"已创建
- [ ] 代码仓库已设置并包含所有项目文件
- [ ] 分支策略已配置

### Service Connections
- [ ] `azure-service-connection` (Azure RM) 已创建并验证
- [ ] `docker-registry-connection` (Docker Registry) 已创建并验证

### Variable Groups
- [ ] `terraform-variables` Variable Group已创建
- [ ] `application-variables` Variable Group已创建
- [ ] 所有敏感变量已标记为Secret
- [ ] 所有变量值已正确填入

### Environments
- [ ] `staging` Environment已创建
- [ ] `production` Environment已创建并配置审批
- [ ] `production-destroy` Environment已创建并配置严格审批

### Azure资源
- [ ] Service Principal已创建并记录凭据
- [ ] Terraform状态存储已创建
- [ ] Azure Container Registry已创建（如果使用ACR）

### Pipeline文件
- [ ] `azure-pipelines-infrastructure.yml` 在仓库中
- [ ] `azure-pipelines-application.yml` 在仓库中
- [ ] Pipeline已在Azure DevOps中创建但未运行

## 🚀 下一步

完成所有配置后，你可以：

1. **首先运行Infrastructure Pipeline**
   - 手动触发Infrastructure Pipeline
   - 验证Terraform计划
   - 批准基础设施部署

2. **然后运行Application Pipeline**
   - 推送代码到main分支
   - 观察自动化CI/CD流程
   - 验证应用部署

3. **测试完整流程**
   - 创建feature分支并提交PR
   - 验证自动化测试
   - 测试环境提升流程

## ⚠️ 常见问题

### 权限问题
```
错误：Service connection 'azure-service-connection' could not be found
解决：检查Service Connection名称和权限设置
```

### 变量问题
```
错误：Variable group 'terraform-variables' could not be found
解决：确认Variable Group名称拼写正确，并且允许Pipeline访问
```

### 存储账户问题
```
错误：Storage account 'terraformstate...' not found
解决：确认存储账户已创建且名称正确填入Variable Group
```

---

完成这些设置后，你的Azure DevOps环境就准备好了！可以开始运行CI/CD Pipeline了。