# Example AliExpress DAG
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def aliexpress_task():
    print("AliExpress task example")

dag = DAG('aliexpress_example', start_date=datetime(2025, 1, 1))
task = PythonOperator(task_id='aliexpress_task', python_callable=aliexpress_task, dag=dag)