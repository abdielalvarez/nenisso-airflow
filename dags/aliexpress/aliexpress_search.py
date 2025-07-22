# AliExpress Search DAG
# Migrated from: SEARCH_BY_KEYWORD_* workflows

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'nenisso',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def search_by_keyword(**context):
    """
    Search AliExpress items by keyword
    Migrated from SEARCH_BY_KEYWORD workflows
    """
    print("Searching AliExpress by keyword...")
    return "search_completed"

def store_item_search(**context):
    """
    Search items within specific AliExpress stores
    Migrated from STORE_ITEM_SEARCH workflow
    """
    print("Searching store items...")
    return "store_search_completed"

dag = DAG(
    'aliexpress_search',
    default_args=default_args,
    description='Search AliExpress items and stores',
    schedule_interval='@daily',
    catchup=False
)

keyword_search = PythonOperator(
    task_id='search_by_keyword',
    python_callable=search_by_keyword,
    dag=dag
)

store_search = PythonOperator(
    task_id='store_item_search',
    python_callable=store_item_search,
    dag=dag
)

keyword_search >> store_search