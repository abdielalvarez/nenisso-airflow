# CLAUDE.md

This file provides comprehensive guidance to Claude Code when working with the nenisso-airflow project.

## Project Overview

**nenisso-airflow** is an Apache Airflow implementation for migrating complex n8n workflows to production-grade data orchestration. The project maintains the business logic from the original n8n-server while leveraging Airflow's superior scheduling, monitoring, and scalability.

### Migration Context

This project migrates from a sophisticated n8n ecosystem that handles:
- **E-commerce operations** (MercadoLibre, AliExpress integration)
- **AI-powered content generation** (OpenAI, video generation)
- **Multi-modal bot interactions** (Telegram, WhatsApp)
- **Cloud data processing** (GCS, Google Drive, PostgreSQL)
- **Vector database operations** (Qdrant, embeddings)

## Architecture Principles

### 1. DAG Organization Strategy
```
dags/
├── service_name/           # Group by external service
│   ├── __init__.py
│   ├── dag_name.py        # Individual DAG files
│   └── example.py         # Template for new DAGs
```

### 2. Migration Patterns
- **1 n8n workflow** → **1 Airflow DAG**
- **n8n node** → **Airflow Task**
- **n8n credential** → **Airflow Connection**
- **n8n webhook** → **Airflow Sensor**
- **n8n sub-workflow** → **TaskGroup or SubDAG**

### 3. Code Organization
```
include/
├── workflows_logic/        # Business logic from n8n
├── configs/               # Configuration management
└── migration/             # n8n→Airflow conversion tools

plugins/
├── operators/             # Custom operators per service
├── hooks/                # Service-specific connections
└── sensors/              # Custom trigger sensors

services/
└── aliexpress.py          # Complete AliExpress API integration
```

## Development Commands

### Core Airflow Commands
```bash
# Initialize Airflow database
airflow db init

# Create admin user
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Start Airflow scheduler
airflow scheduler

# Start Airflow webserver
airflow webserver --port 8080

# Test specific DAG
airflow dags test dag_id execution_date

# Run specific task
airflow tasks test dag_id task_id execution_date
```

### Development Workflow
```bash
# Lint Python code
ruff check .
ruff format .

# Type checking
mypy dags/ include/ plugins/

# Run tests
pytest tests/ -v

# Validate all DAGs
python -m pytest tests/test_dag_validation.py
```

### DAG Development Commands
```bash
# List all DAGs
airflow dags list

# Check DAG for errors
airflow dags check dag_id

# Show DAG structure
airflow dags show dag_id

# Trigger DAG manually
airflow dags trigger dag_id
```

## Coding Standards

### DAG Structure Template
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

# Import business logic from include/
from include.workflows_logic.service_logic import process_function

default_args = {
    'owner': 'nenisso',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'service_workflow_name',
    default_args=default_args,
    description='Migrated from n8n workflow: ORIGINAL_NAME_ID.json',
    schedule_interval='@daily',  # Use n8n's original schedule
    catchup=False,
    max_active_runs=1,
    tags=['service-name', 'migrated-from-n8n']
)

# Tasks follow n8n node structure
start = DummyOperator(task_id='start', dag=dag)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_function,
    dag=dag
)

end = DummyOperator(task_id='end', dag=dag)

# Dependencies mirror n8n connections
start >> process_task >> end
```

### Business Logic Organization
```python
# include/workflows_logic/service_name_logic.py
"""
Business logic migrated from n8n workflow: ORIGINAL_NAME_ID.json
Original workflow path: n8n-server/n8n/workflows/ORIGINAL_NAME_ID.json
"""

def migrated_function(**context):
    """
    Migrated from n8n node: NodeName
    Original node type: n8n-nodes-base.nodeType
    """
    # Preserve original business logic
    pass
```

### Custom Operators Pattern
```python
# plugins/operators/service_operator.py
from airflow.models import BaseOperator
from airflow.hooks.base_hook import BaseHook

class ServiceOperator(BaseOperator):
    """
    Custom operator for Service API integration
    Migrated from n8n nodes of type: service-node-type
    """
    
    def __init__(self, service_conn_id: str, **kwargs):
        super().__init__(**kwargs)
        self.service_conn_id = service_conn_id
    
    def execute(self, context):
        # Implementation following n8n node logic
        pass
```

## Configuration Management

### Airflow Variables (for n8n global variables)
```python
from airflow.models import Variable

# Migrate n8n global variables to Airflow Variables
API_BASE_URL = Variable.get("api_base_url", default_var="https://api.example.com")
BATCH_SIZE = Variable.get("batch_size", default_var=100)
```

### Airflow Connections (for n8n credentials)
```python
from airflow.hooks.base_hook import BaseHook

# Migrate n8n credentials to Airflow Connections
def get_service_connection():
    conn = BaseHook.get_connection("service_conn_id")
    return {
        'api_key': conn.password,
        'base_url': conn.host,
        'extra_params': conn.extra_dejson
    }
```

### Environment-Specific Settings
```python
# include/configs/airflow_config.py
import os
from airflow.configuration import conf

# Environment detection
ENVIRONMENT = os.getenv('AIRFLOW_ENV', 'development')
IS_PRODUCTION = ENVIRONMENT == 'production'

# Resource allocation based on environment
DEFAULT_POOL_SIZE = 5 if IS_PRODUCTION else 2
MAX_ACTIVE_TASKS = 16 if IS_PRODUCTION else 8
```

## Migration Guidelines

### 1. Pre-Migration Analysis
Before migrating any n8n workflow:
1. **Study original workflow JSON** in `n8n-server/n8n/workflows/`
2. **Identify node types** and their Airflow equivalents
3. **Map credentials** to Airflow Connections
4. **Analyze dependencies** and data flow
5. **Review error handling** patterns

### 2. Migration Process
1. **Create DAG file** in appropriate `dags/service/` directory
2. **Extract business logic** to `include/workflows_logic/`
3. **Create custom operators** if needed in `plugins/operators/`
4. **Set up connections** via Airflow UI or environment variables
5. **Add comprehensive tests** in `tests/`
6. **Document migration** in DAG docstring

### 3. Testing Strategy
```python
# tests/dags/test_service_workflow.py
import pytest
from datetime import datetime
from airflow.models import DagBag

def test_dag_loads():
    """Test that DAG loads without errors"""
    dag_bag = DagBag(dag_folder='dags/', include_examples=False)
    assert 'service_workflow_name' in dag_bag.dags
    assert len(dag_bag.import_errors) == 0

def test_dag_structure():
    """Test DAG structure matches n8n workflow"""
    dag_bag = DagBag(dag_folder='dags/', include_examples=False)
    dag = dag_bag.get_dag('service_workflow_name')
    
    # Verify task count matches n8n nodes
    assert len(dag.tasks) == expected_task_count
    
    # Verify dependencies match n8n connections
    task_dependencies = dag.get_task_dependencies()
    # Add specific dependency assertions
```

## Error Handling Patterns

### 1. Retry Configuration
```python
# Mirror n8n's error handling settings
default_args = {
    'retries': 3,  # Based on n8n workflow settings
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30)
}
```

### 2. Error Logging
```python
def error_callback(context):
    """Custom error callback for critical workflows"""
    task_instance = context['task_instance']
    dag_id = context['dag'].dag_id
    
    # Log to same systems as n8n workflows
    print(f"Task {task_instance.task_id} failed in DAG {dag_id}")
    
    # Integrate with existing error reporting
    # (preserve n8n error notification patterns)
```

## Performance Optimization

### 1. Resource Allocation
```python
# DAG-level resource configuration
dag = DAG(
    'resource_intensive_dag',
    max_active_runs=1,          # Prevent resource conflicts
    max_active_tasks_per_dag=4, # Limit concurrent tasks
    pool='heavy_computation_pool'  # Use dedicated resource pool
)
```

### 2. Task Grouping for Parallel Processing
```python
from airflow.utils.task_group import TaskGroup

with TaskGroup('parallel_processing') as tg:
    # Group related tasks that can run in parallel
    # (similar to n8n parallel branches)
    for i in range(batch_count):
        task = PythonOperator(
            task_id=f'process_batch_{i}',
            python_callable=process_batch_function,
            op_args=[i]
        )
```

## Integration Points

### 1. Database Connections
- **PostgreSQL**: Shared with original n8n-server database
- **Connection ID**: Use `postgres_default` or create service-specific connections
- **Schema**: Maintain compatibility with existing table structures

### 2. External APIs
- **MercadoLibre**: Migrate OAuth2 credentials and refresh token logic
- **OpenAI**: Use existing API keys through Airflow Connections
- **Google Cloud**: Maintain service account authentication patterns
- **RapidAPI**: Preserve API key management and rate limiting

### 3. File Storage
- **Google Cloud Storage**: Use existing bucket structure and naming conventions
- **Local file processing**: Maintain compatibility with n8n file handling patterns

## Documentation Requirements

### 1. DAG Documentation
Each DAG must include:
- **Original n8n workflow reference**: File name and ID
- **Business purpose**: What the workflow accomplishes
- **Migration notes**: Changes made during conversion
- **Dependencies**: External services and connections required
- **Monitoring**: Key metrics and alerting points

### 2. Operator Documentation
Custom operators must document:
- **n8n node equivalent**: Original node type being replaced
- **Parameter mapping**: n8n parameters → Airflow parameters
- **Error handling**: How errors are managed vs. n8n
- **Testing approach**: Unit and integration test patterns

## Security Considerations

### 1. Secrets Management
- **Never hardcode** API keys or passwords in DAG files
- **Use Airflow Connections** for all external service credentials
- **Environment variables** for non-sensitive configuration only
- **Airflow Variables** for encrypted sensitive data

### 2. Access Control
- **DAG-level permissions** for different service teams
- **Connection-level security** for API credentials
- **Audit logging** for sensitive operations

## Common Migration Patterns

### 1. HTTP Requests (n8n HTTP node → Airflow)
```python
from airflow.providers.http.operators.http import SimpleHttpOperator

# n8n HTTP node becomes SimpleHttpOperator
http_task = SimpleHttpOperator(
    task_id='api_request',
    http_conn_id='service_connection',
    endpoint='/api/endpoint',
    method='POST',
    headers={'Content-Type': 'application/json'},
    data=json.dumps(payload)
)
```

### 2. Conditional Logic (n8n IF node → Airflow)
```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    # Migrate n8n IF node logic
    condition = evaluate_condition(context)
    return 'true_branch' if condition else 'false_branch'

branch_task = BranchPythonOperator(
    task_id='conditional_logic',
    python_callable=choose_branch
)
```

### 3. Data Transformation (n8n Code node → Airflow)
```python
def transform_data(**context):
    """
    Migrated from n8n Code node
    Original JavaScript logic converted to Python
    """
    # Preserve original transformation logic
    raw_data = context['task_instance'].xcom_pull(task_ids='extract_task')
    transformed = process_data(raw_data)  # Business logic preserved
    return transformed

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data
)
```

## Monitoring and Alerting

### 1. DAG Monitoring
- **SLA monitoring**: Set based on n8n workflow performance
- **Task duration alerting**: Identify performance degradation
- **Success/failure rates**: Maintain service level agreements

### 2. Business Logic Monitoring
- **Data quality checks**: Preserve n8n workflow validations
- **API response monitoring**: Track external service health
- **Volume alerting**: Monitor data processing volumes

## Development Workflow

### 1. New DAG Creation
1. **Identify source workflow**: Reference original n8n workflow JSON
2. **Create DAG skeleton**: Use template structure above
3. **Migrate business logic**: Extract to `include/workflows_logic/`
4. **Add tests**: Unit tests for logic, integration tests for DAG
5. **Validate locally**: Test DAG parsing and execution
6. **Document migration**: Update this CLAUDE.md if needed

### 2. Testing Approach
```bash
# Validate DAG syntax
python dags/service/workflow_name.py

# Test DAG loading
airflow dags check workflow_name

# Run task locally
airflow tasks test workflow_name task_name 2025-01-01

# Full DAG test
airflow dags test workflow_name 2025-01-01
```

## File Naming Conventions

### 1. DAG Files
- **Pattern**: `service_workflow_purpose.py`
- **Examples**: `ml_token_management.py`, `openai_category_predictor.py`
- **Avoid**: Generic names like `dag.py` or `workflow.py`

### 2. Business Logic Files
- **Pattern**: `service_name_logic.py`
- **Location**: `include/workflows_logic/`
- **Documentation**: Include original n8n workflow reference

### 3. Test Files
- **Pattern**: `test_service_workflow.py`
- **Location**: `tests/dags/`
- **Coverage**: Test both DAG structure and business logic

Remember: This project preserves complex business logic while gaining Airflow's orchestration capabilities. Always reference the original n8n workflows in `n8n-server/n8n/workflows/` when implementing new features or debugging issues.

## AliExpress Service Integration

### Overview
The AliExpress service (`services/aliexpress.py`) provides complete integration with the AliExpress DataHub RapidAPI. It implements all 10 endpoints found in the original n8n workflows with proper error handling, logging, and validation.

### Implementation Details

**Service Class Location**: `services/aliexpress.py`  
**Configuration**: Uses `include/configs/env_config.py` for environment variables  
**API Key**: Configured via `RAPIDAPI_ALIEXPRESS_KEY` environment variable

### Available Endpoints

1. **item_search_5** - Product search by keyword
2. **item_detail_3** - Detailed product information
3. **category_list_1** - AliExpress categories list
4. **item_desc_2** - Detailed product descriptions
5. **store_item_search_2** - Search items within specific stores
6. **shipping_detail_5** - Shipping information and costs
7. **item_review_2** - Product reviews and ratings
8. **store_categories** - Store-specific categories
9. **store_info** - Store information and ratings
10. **item_sku** - Product variants and SKU details

### Testing Structure

**Test Location**: `tests/executions/`  
**Test Pattern**: `test_aliexpress_[endpoint].py`

```bash
# Run all AliExpress tests
python tests/executions/test_aliexpress_search.py
python tests/executions/test_aliexpress_item_detail.py
python tests/executions/test_aliexpress_categories.py
python tests/executions/test_aliexpress_description.py
python tests/executions/test_aliexpress_store_search.py
python tests/executions/test_aliexpress_shipping.py
python tests/executions/test_aliexpress_reviews.py
python tests/executions/test_aliexpress_store_categories.py
python tests/executions/test_aliexpress_store_info.py
python tests/executions/test_aliexpress_sku.py
```

### Error Handling

The service implements comprehensive error handling:
- **HTTP Status Validation**: Accepts codes 200 (success) and 205 (no results)
- **API Response Validation**: Checks for violations and error conditions
- **Logging**: Full request/response logging for debugging
- **Exception Management**: Proper exception raising with context

### Usage Pattern

```python
from services.aliexpress import AliExpress
from include.configs.env_config import ENV

# Initialize service
api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
api = AliExpress(api_key)

# Search products
results = api.item_search_5(q="iphone", page=1)

# Get product details
details = api.item_detail_3("3256809212376891")
```

### Mock Data Structure

**Mock Location**: `tests/data/aliexpress/`  
**Pattern**: `[endpoint]_response.json`

Mock files contain real API responses for testing and development purposes.

### API Configuration

**Base URL**: `https://aliexpress-datahub.p.rapidapi.com`  
**Headers**: 
- `x-rapidapi-host: aliexpress-datahub.p.rapidapi.com`
- `x-rapidapi-key: [YOUR_API_KEY]`

**Default Parameters**:
- `locale: es_ES` (Spanish)
- `region: MX` (Mexico)  
- `currency: MXN` (Mexican Peso)

### Migration Notes

This service directly replaces the AliExpress functionality from the original n8n workflows:
- Preserves all parameter structures from n8n nodes
- Maintains error handling patterns
- Supports all data transformations used in original workflows
- Ready for integration into Airflow DAGs