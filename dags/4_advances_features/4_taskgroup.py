from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

# Default DAG arguments
default_args = {
    'owner': 'Willis',
    'start_date': datetime(2023, 8, 1),  # The date when the DAG starts
}

# Define the DAG
dag = DAG(
    'taskgroup_dag',             # DAG ID
    default_args=default_args,     # Default arguments for the DAG
    description='taskgroup',
    tags=['Data Engineering courses',"Advanced"],
    catchup=False,      # If set to True, Airflow will execute all instances between the DAG's start_date and the current day. Setting to False means skipping missed instances.
    schedule='@daily'  # Schedule interval (run at midnight every day)
)


# Define tasks using BashOperator
task1 = BashOperator(
    task_id='task1',                      # Task ID
    bash_command='echo "Task 1"',         # Bash command to be executed
    dag=dag                               # Assign the task to the DAG
)

# Using the TaskGroup context manager.
with TaskGroup("grouped_tasks", dag=dag) as tg: 
    task2 = BashOperator(
        task_id='task2',
        bash_command='echo "Task 2"',
        dag=dag   
    )

    task3 = BashOperator(
        task_id='task3',
        bash_command='echo "Task 3"',
        dag=dag
    )

    task4 = BashOperator(
        task_id='task4',
        bash_command='echo "Task 4"',
        dag=dag
    )

    task2 >> task4
    task3 >> task4

task5 = BashOperator(
    task_id='Create_txt_file',
    bash_command='echo "Ceci est un fichier test" > /opt/airflow/dags/4_advances_features/sample_bis.txt',  # Create a txt file with text
    dag=dag
)

# Define the task dependencies
task1 >> tg >> task5