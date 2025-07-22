# Example GCP DAG
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def gcp_task():
    print("Google Cloud Platform task example")

dag = DAG('gcp_example', start_date=datetime(2025, 1, 1))
task = PythonOperator(task_id='gcp_task', python_callable=gcp_task, dag=dag)