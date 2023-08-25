from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Define default arguments for the DAG
default_args = {
    'owner': 'Willis',        # Owner of the DAG
    'depends_on_past': False,      # DAG does not depend on past runs of tasks
    'email_on_failure': False,     # Disable email notifications on failure
    'email_on_retry': False,       # Disable email notifications on retry
    'retries': 0,                  # Number of retries in case of failure (disabled)
    'start_date': datetime(2023, 8, 1),  # Start date of the DAG
    
}

# Define the DAG
dag = DAG(
    'your_first_dag',             # DAG ID
    default_args=default_args,     # Default arguments for the DAG
    description='Training DAG',
    tags=['Data Engineering courses',"Beginner"],
    catchup=False,              # Do not backfill past runs when DAG is created
    schedule='0 0 * * *'  # Schedule interval (run at midnight every day)
)

# Define tasks using BashOperator
task1 = BashOperator(
    task_id='task1',                      # Task ID
    bash_command='echo "Task 1"',         # Bash command to be executed
    dag=dag                               # Assign the task to the DAG
)

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

task5 = BashOperator(
    task_id='Create_txt_file',
    bash_command='echo "Ceci est un fichier test" > /opt/airflow/ddags/1_first_dag/sample.txt',  # Create a txt file with text
    dag=dag
)

# Define the task dependencies
task1 >> task2         # task1 depends on task2
task1 >> task3         # task1 depends on task3
task2 >> task4         # task2 depends on task4
task3 >> task4         # task3 depends on task4
task4 >> task5         # task4 depends on task5