from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from project.controller import read_data, check_threshold, send_message


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def get_tasks(dag_schedule):
    read = PythonOperator(
        task_id='read_users_info',
        python_callable=read_data,
        op_kwargs={'group_by': dag_schedule}
    )
     
    check = PythonOperator(
        task_id = 'Check_threshold',
        python_callable=check_threshold,
        op_kwargs={'group': dag_schedule}
    )

    send = PythonOperator(
        task_id = "send_notification",
        python_callable=send_message,
        op_kwargs={'group': dag_schedule}
    )

    return read, check, send


with DAG(
    dag_id='notifier_mins10',
    default_args=default_args,
    schedule_interval='*/10 * * * *'
) as dag:    
    read, check, send = get_tasks('mins10')
    read >> check >> send



with DAG(
    dag_id='notifier_hourly',
    default_args=default_args,
    schedule_interval='@hourly'
) as dag:    
    read, check, send = get_tasks('hourly')
    read >> check >> send


with DAG(
    dag_id='notifier_daily',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:    
    read, check, send = get_tasks('daily')
    read >> check >> send


with DAG(
    dag_id='notifier_weekly',
    default_args=default_args,
    schedule_interval='@weekly'
) as dag:    
    read, check, send = get_tasks('weekly')
    read >> check >> send