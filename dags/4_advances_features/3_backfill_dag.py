from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Default DAG arguments
default_args = {
    'owner': 'Willis',
    'start_date': datetime(2023, 8, 1),  # The date when the DAG starts
}

# Define the DAG
dag = DAG(
    'catchup_and_backfill_dag',             # DAG ID
    default_args=default_args,     # Default arguments for the DAG
    description='catchup and backfill',
    tags=['Data Engineering courses',"Advanced"],
    catchup = True,              
    schedule='@daily'  # Schedule interval (run at midnight every day)
)

# Function to print a message
def print_message(message):
    print(message)

# Task to print a message for each execution
print_message_task = PythonOperator(
    task_id='print_message',
    python_callable=print_message,
    op_args=['Hello, this is a backfill example!'],
    dag=dag
)
