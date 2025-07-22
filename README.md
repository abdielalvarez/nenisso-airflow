# Nenisso Airflow

Apache Airflow implementation for migrating n8n workflows to Airflow DAGs.

## Structure

### DAGs by Service
- `mercadolibre/` - MercadoLibre API workflows
- `aliexpress/` - AliExpress data processing workflows  
- `openai/` - OpenAI and AI service workflows
- `gcp/` - Google Cloud Platform workflows
- `postgresql/` - Database operations workflows
- `orchestration/` - Master orchestrator workflows
- `communication/` - Bot and notification workflows

### Plugins
- `operators/` - Custom operators for each service
- `sensors/` - Custom sensors for triggers
- `hooks/` - Service connection hooks

### Include
- `workflows_logic/` - Business logic from n8n workflows
- `configs/` - Configuration files
- `migration/` - Tools for n8n to Airflow migration

## Migration from n8n

This structure mirrors the existing n8n workflows in `/n8n/workflows/` and provides a systematic way to migrate each workflow to Airflow DAGs.