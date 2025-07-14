# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
  
  # 配置远程状态存储（可选）
  backend "azurerm" {
    # 这些值将通过pipeline变量设置
    # resource_group_name  = "terraform-state-rg"
    # storage_account_name = "terraformstateXXXXX"
    # container_name      = "tfstate"
    # key                 = "devops-demo.terraform.tfstate"
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# 获取当前Azure配置信息
data "azurerm_client_config" "current" {}

# 创建资源组
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location

  tags = var.common_tags
}

# 创建App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${var.app_name}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  os_type            = "Linux"
  sku_name           = var.app_service_sku

  tags = var.common_tags
}

# 创建App Service
resource "azurerm_linux_web_app" "main" {
  name                = var.app_name
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_service_plan.main.location
  service_plan_id    = azurerm_service_plan.main.id

  site_config {
    always_on = var.app_service_sku != "F1" ? true : false
    
    application_stack {
      docker_image     = var.docker_image_name
      docker_image_tag = var.docker_image_tag
    }

    health_check_path = "/health"
    
    # CORS配置
    cors {
      allowed_origins = ["*"]
    }
  }

  app_settings = {
    "ENVIRONMENT"                    = var.environment
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"     = var.docker_registry_url
    "DOCKER_REGISTRY_SERVER_USERNAME" = var.docker_registry_username
    "DOCKER_REGISTRY_SERVER_PASSWORD" = var.docker_registry_password
  }

  logs {
    detailed_error_messages = true
    failed_request_tracing  = true
    
    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 35
      }
    }
  }

  tags = var.common_tags
}

# 创建Application Insights（可选）
resource "azurerm_application_insights" "main" {
  name                = "${var.app_name}-insights"
  location           = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type   = "web"

  tags = var.common_tags
}

# 配置App Service的Application Insights
resource "azurerm_linux_web_app_slot" "staging" {
  count           = var.create_staging_slot ? 1 : 0
  name            = "staging"
  app_service_id  = azurerm_linux_web_app.main.id

  site_config {
    always_on = var.app_service_sku != "F1" ? true : false
    
    application_stack {
      docker_image     = var.docker_image_name
      docker_image_tag = var.docker_image_tag
    }

    health_check_path = "/health"
  }

  app_settings = {
    "ENVIRONMENT"                    = "staging"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"     = var.docker_registry_url
    "DOCKER_REGISTRY_SERVER_USERNAME" = var.docker_registry_username
    "DOCKER_REGISTRY_SERVER_PASSWORD" = var.docker_registry_password
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.main.instrumentation_key
  }

  tags = var.common_tags
}