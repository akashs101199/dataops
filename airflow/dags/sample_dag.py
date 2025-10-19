from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import random, time

def do_work():
    time.sleep(random.randint(1, 5))

def maybe_fail():
    if random.random() < 0.3:
        raise RuntimeError("Intentional failure for demo")

with DAG(
    dag_id="demo_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=timedelta(minutes=2),
    catchup=False,
    default_args={"owner": "demo"},
    tags=["demo"],
) as dag:
    t1 = PythonOperator(task_id="extract", python_callable=do_work)
    t2 = PythonOperator(task_id="transform", python_callable=maybe_fail)
    t3 = PythonOperator(task_id="load", python_callable=do_work)

    t1 >> t2 >> t3
