# Example MercadoLibre DAG
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def ml_task():
    print("MercadoLibre task example")

dag = DAG('ml_example', start_date=datetime(2025, 1, 1))
task = PythonOperator(task_id='ml_task', python_callable=ml_task, dag=dag)