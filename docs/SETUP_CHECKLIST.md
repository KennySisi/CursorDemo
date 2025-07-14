# Azure DevOps 设置快速检查清单

使用这个清单确保你已完成所有必要的Azure DevOps配置。

## 🎯 设置优先级

```
高优先级 (必须完成)
├── ✅ Azure订阅和权限
├── ✅ Service Principal创建
├── ✅ Azure DevOps组织和项目
├── ✅ Service Connections
├── ✅ Variable Groups
├── ✅ Environments
└── ✅ Pipeline创建

中优先级 (建议完成)
├── ☑️ 分支策略
├── ☑️ 审批流程
├── ☑️ 权限细化
└── ☑️ 监控设置

低优先级 (可选)
├── ⭕ 部署时间窗口
├── ⭕ 高级安全设置
└── ⭕ 自定义Agent
```

## 📋 必需信息收集

在开始设置之前，准备以下信息：

### Azure信息
- [ ] **Azure订阅ID**: `_________________________________`
- [ ] **Azure租户ID**: `_________________________________`
- [ ] **资源组名称**: `terraform-state-rg`
- [ ] **存储账户名称**: `terraformstate[timestamp]`

### Azure DevOps信息
- [ ] **组织名称**: `_________________________________`
- [ ] **项目名称**: `devops-demo`
- [ ] **仓库URL**: `_________________________________`

### 应用配置
- [ ] **应用名称** (全局唯一): `devops-demo-app-[timestamp]`
- [ ] **Docker Registry类型**: [ ] ACR [ ] Docker Hub
- [ ] **Registry名称**: `_________________________________`

## 🔧 第一步：Azure资源准备

### 1.1 Azure CLI登录
```bash
# 执行命令并确认结果
az login
az account show --query "id" -o tsv
```
- [ ] **订阅ID记录**: `_________________________________`

### 1.2 创建Service Principal
```bash
az ad sp create-for-rbac \
  --name "devops-demo-terraform" \
  --role="Contributor" \
  --scopes="/subscriptions/{your-subscription-id}"
```
**记录输出信息**:
- [ ] **appId** (ARM_CLIENT_ID): `_________________________________`
- [ ] **password** (ARM_CLIENT_SECRET): `_________________________________`
- [ ] **tenant** (ARM_TENANT_ID): `_________________________________`

### 1.3 创建Terraform状态存储
```bash
# 创建资源组
az group create --name terraform-state-rg --location "East Asia"

# 创建存储账户
STORAGE_ACCOUNT_NAME="terraformstate$(date +%s)"
az storage account create \
  --name $STORAGE_ACCOUNT_NAME \
  --resource-group terraform-state-rg \
  --location "East Asia" \
  --sku Standard_LRS

# 创建容器
az storage container create --name tfstate --account-name $STORAGE_ACCOUNT_NAME
```
- [ ] **存储账户名称记录**: `_________________________________`

### 1.4 创建Container Registry (如果使用ACR)
```bash
ACR_NAME="devopsdemoregistry$(date +%s)"
az acr create \
  --resource-group terraform-state-rg \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled

# 获取凭据
az acr credential show --name $ACR_NAME
```
- [ ] **ACR名称**: `_________________________________`
- [ ] **ACR用户名**: `_________________________________`
- [ ] **ACR密码**: `_________________________________`

## 🏗️ 第二步：Azure DevOps基础设置

### 2.1 组织和项目创建
访问: `https://dev.azure.com/`

- [ ] **组织已创建**: `https://dev.azure.com/{your-org}`
- [ ] **项目已创建**: 名称为`devops-demo`
- [ ] **Git仓库可访问**: 可以clone和push代码

### 2.2 代码仓库设置
- [ ] **项目文件已上传**: 所有Pipeline文件都在仓库中
- [ ] **分支结构正确**: 有main分支
- [ ] **分支策略已设置**: 配置了基本的保护规则

## 🔗 第三步：Service Connections

### 3.1 Azure Resource Manager
`Project Settings → Service connections → Create service connection`

- [ ] **连接类型**: Azure Resource Manager
- [ ] **名称**: `azure-service-connection`
- [ ] **订阅**: 已选择正确的Azure订阅
- [ ] **权限**: Grant access to all pipelines ✅
- [ ] **验证**: 连接测试通过 ✅

### 3.2 Docker Registry
- [ ] **连接类型**: Docker Registry
- [ ] **名称**: `docker-registry-connection`
- [ ] **Registry类型**: [ ] ACR [ ] Docker Hub
- [ ] **凭据**: 已正确配置
- [ ] **权限**: Grant access to all pipelines ✅
- [ ] **验证**: 连接测试通过 ✅

## 📦 第四步：Variable Groups

### 4.1 terraform-variables Group
`Pipelines → Library → Variable groups`

**Group名称**: `terraform-variables`

**必需变量**:
- [ ] **ARM_CLIENT_ID**: `[Service Principal appId]` 
- [ ] **ARM_CLIENT_SECRET**: `[Service Principal password]` 🔒 Secret
- [ ] **ARM_SUBSCRIPTION_ID**: `[Azure Subscription ID]`
- [ ] **ARM_TENANT_ID**: `[Azure Tenant ID]`
- [ ] **TF_VAR_app_name**: `devops-demo-app-[timestamp]` (全局唯一)
- [ ] **TF_VAR_location**: `East Asia`
- [ ] **TF_VAR_environment**: `prod`
- [ ] **TF_VAR_app_service_sku**: `B1`
- [ ] **backendResourceGroup**: `terraform-state-rg`
- [ ] **backendStorageAccount**: `[存储账户名称]`
- [ ] **backendContainerName**: `tfstate`

**权限设置**:
- [ ] **Allow access to all pipelines**: ✅

### 4.2 application-variables Group
**Group名称**: `application-variables`

**必需变量**:
- [ ] **webAppName**: `[与TF_VAR_app_name相同]`
- [ ] **imageRepository**: `devops-demo-api`

**ACR配置** (如果使用ACR):
- [ ] **dockerRegistryUrl**: `[ACR名称].azurecr.io`
- [ ] **dockerRegistryUsername**: `[ACR用户名]`
- [ ] **dockerRegistryPassword**: `[ACR密码]` 🔒 Secret

**Docker Hub配置** (如果使用Docker Hub):
- [ ] **dockerRegistryUrl**: `docker.io`
- [ ] **dockerRegistryUsername**: `[Docker Hub用户名]`
- [ ] **dockerRegistryPassword**: `[Docker Hub密码]` 🔒 Secret

**权限设置**:
- [ ] **Allow access to all pipelines**: ✅

## 🌍 第五步：Environments

### 5.1 staging Environment
`Pipelines → Environments → Create environment`

- [ ] **Name**: `staging`
- [ ] **Description**: `Staging environment for testing`
- [ ] **Resource**: None
- [ ] **Approvals**: 无需审批 (自动部署)

### 5.2 production Environment
- [ ] **Name**: `production`
- [ ] **Description**: `Production environment`
- [ ] **Resource**: None

**审批设置**:
- [ ] **Approvals**: 已添加审批者
- [ ] **Timeout**: 30 minutes
- [ ] **Instructions**: 已设置审批说明

### 5.3 production-destroy Environment
- [ ] **Name**: `production-destroy`
- [ ] **Description**: `Environment for infrastructure destruction`
- [ ] **Approvals**: 已配置严格审批

## 📝 第六步：Pipeline创建

### 6.1 Infrastructure Pipeline
`Pipelines → Pipelines → Create Pipeline`

- [ ] **Source**: Azure Repos Git
- [ ] **Repository**: devops-demo
- [ ] **YAML file**: `/azure-pipelines-infrastructure.yml`
- [ ] **Name**: `Infrastructure Pipeline`
- [ ] **Status**: 已保存但未运行

### 6.2 Application Pipeline
- [ ] **Source**: Azure Repos Git
- [ ] **Repository**: devops-demo
- [ ] **YAML file**: `/azure-pipelines-application.yml`
- [ ] **Name**: `Application Pipeline`
- [ ] **Status**: 已保存但未运行

## ✅ 最终验证清单

### 关键配置验证
- [ ] **所有Service Connections都显示绿色对勾** ✅
- [ ] **所有Variable Groups都可访问** ✅
- [ ] **所有Environments都已创建** ✅
- [ ] **Pipeline文件存在于仓库中** ✅
- [ ] **敏感变量都标记为Secret** 🔒

### 权限验证
- [ ] **Service Connections允许Pipeline访问** ✅
- [ ] **Variable Groups允许Pipeline访问** ✅
- [ ] **Environments配置了正确的审批流程** ✅

### Azure资源验证
在Azure Portal中确认:
- [ ] **terraform-state-rg资源组存在** ✅
- [ ] **存储账户存在且可访问** ✅
- [ ] **Service Principal有Contributor权限** ✅
- [ ] **ACR存在且可访问** (如果使用) ✅

## 🚀 准备就绪检查

如果所有上述项目都已完成，你可以开始运行Pipeline：

### 首次部署顺序
1. **Infrastructure Pipeline**:
   ```
   Pipelines → Infrastructure Pipeline → Run pipeline
   ```

2. **验证基础设施部署**:
   - 检查Terraform plan
   - 批准apply步骤
   - 确认Azure资源创建成功

3. **Application Pipeline**:
   ```
   推送代码到main分支或手动触发
   ```

4. **验证应用部署**:
   - 检查CI阶段通过
   - 确认Docker镜像构建成功
   - 验证生产环境部署

## ⚠️ 故障排除快速参考

### 常见错误和解决方案

**Service Connection错误**:
```
Error: Could not find service connection 'azure-service-connection'
Solution: 检查名称拼写，确认Pipeline有访问权限
```

**Variable Group错误**:
```
Error: Variable group 'terraform-variables' not found
Solution: 确认Variable Group名称正确，检查Pipeline权限
```

**Azure权限错误**:
```
Error: Insufficient privileges to complete the operation
Solution: 确认Service Principal有Contributor权限
```

**Terraform状态错误**:
```
Error: Error loading state: storage account not found
Solution: 确认存储账户名称正确，检查网络访问
```

## 📞 需要帮助?

如果遇到问题：

1. **检查清单**: 确保所有必需项目都已完成 ✅
2. **查看日志**: Pipeline执行日志通常有详细错误信息
3. **验证权限**: 确认所有权限都正确配置
4. **测试连接**: 手动测试Service Connections

---

**完成状态**: ___/69 项已完成

完成所有检查项目后，你的Azure DevOps环境就完全准备好了！🎉