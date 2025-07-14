output "resource_group_name" {
  description = "资源组名称"
  value       = azurerm_resource_group.main.name
}

output "app_service_name" {
  description = "App Service名称"
  value       = azurerm_linux_web_app.main.name
}

output "app_service_url" {
  description = "App Service的URL"
  value       = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "app_service_id" {
  description = "App Service的资源ID"
  value       = azurerm_linux_web_app.main.id
}

output "staging_slot_url" {
  description = "Staging槽的URL"
  value       = var.create_staging_slot ? "https://${azurerm_linux_web_app.main.default_hostname}-staging.azurewebsites.net" : null
}

output "application_insights_instrumentation_key" {
  description = "Application Insights的instrumentation key"
  value       = azurerm_application_insights.main.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Application Insights的连接字符串"
  value       = azurerm_application_insights.main.connection_string
  sensitive   = true
}