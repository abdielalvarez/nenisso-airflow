# Example PostgreSQL DAG
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def postgres_task():
    print("PostgreSQL task example")

dag = DAG('postgres_example', start_date=datetime(2025, 1, 1))
task = PythonOperator(task_id='postgres_task', python_callable=postgres_task, dag=dag)