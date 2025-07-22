# Example OpenAI DAG
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def openai_task():
    print("OpenAI task example")

dag = DAG('openai_example', start_date=datetime(2025, 1, 1))
task = PythonOperator(task_id='openai_task', python_callable=openai_task, dag=dag)