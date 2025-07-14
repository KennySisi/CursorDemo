variable "resource_group_name" {
  description = "Azure资源组名称"
  type        = string
  default     = "devops-demo-rg"
}

variable "location" {
  description = "Azure区域位置"
  type        = string
  default     = "East Asia"
}

variable "app_name" {
  description = "应用程序名称"
  type        = string
  default     = "devops-demo-app"
}

variable "environment" {
  description = "环境名称 (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "app_service_sku" {
  description = "App Service的SKU"
  type        = string
  default     = "B1"  # Basic tier, 适合demo使用
  
  validation {
    condition = contains([
      "F1",   # Free
      "D1",   # Shared
      "B1", "B2", "B3",  # Basic
      "S1", "S2", "S3",  # Standard
      "P1v2", "P2v2", "P3v2",  # Premium V2
      "P1v3", "P2v3", "P3v3"   # Premium V3
    ], var.app_service_sku)
    error_message = "app_service_sku必须是有效的Azure App Service SKU."
  }
}

variable "docker_image_name" {
  description = "Docker镜像名称"
  type        = string
  default     = "devops-demo-api"
}

variable "docker_image_tag" {
  description = "Docker镜像标签"
  type        = string
  default     = "latest"
}

variable "docker_registry_url" {
  description = "Docker注册表URL"
  type        = string
  default     = "https://index.docker.io/v1/"
}

variable "docker_registry_username" {
  description = "Docker注册表用户名"
  type        = string
  sensitive   = true
  default     = ""
}

variable "docker_registry_password" {
  description = "Docker注册表密码"
  type        = string
  sensitive   = true
  default     = ""
}

variable "create_staging_slot" {
  description = "是否创建staging部署槽"
  type        = bool
  default     = true
}

variable "common_tags" {
  description = "应用于所有资源的通用标签"
  type        = map(string)
  default = {
    Project     = "DevOps-Demo"
    Environment = "Production"
    ManagedBy   = "Terraform"
    Owner       = "DevOps-Team"
  }
}