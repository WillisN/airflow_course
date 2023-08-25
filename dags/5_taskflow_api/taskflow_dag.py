from airflow import DAG
from airflow.decorators import task, dag
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'Willis',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'start_date': datetime(2023, 8, 1),
}

@dag(dag_id='taskflow_dag',
     default_args=default_args,
     description='taskflow DAG',
     tags=['Data Engineering courses', "Advanced"],
     catchup=False,
     schedule='0 0 * * *'
     )
def taskflow_dag():

    # First task: simply prints and returns a message
    @task()
    def execute_task1():
        print("print - Task 1")
        return "Output of Task 1"

    # Second task: simply prints and returns another message
    @task()
    def execute_task2():
        print("print - Task 2")
        return "Output of Task 2"

    # Third task: just another print and return
    @task()
    def execute_task3():
        print("print - Task 3")
        return "Output of Task 3"

    # Fourth task: takes the outputs from task2 and task3, prints them, and returns a message
    @task()
    def execute_task4(input_from_task2, input_from_task3):
        print(f"print - Task 4, Inputs: {input_from_task2}, {input_from_task3}")
        return "Output of Task 4"

    # Final task: takes the output from task4 and writes it into a text file
    @task()
    def create_txt_file(input_from_task4):
        with open('/opt/airflow/dags/5_taskflow_api/sample_taskflow.txt', 'w') as file:
            file.write(f"Ceci est un fichier test. Input: {input_from_task4}")

    # Initiate tasks
    task1_output = execute_task1()
    task2_output = execute_task2()
    task3_output = execute_task3()
    task4_output = execute_task4(task2_output, task3_output)
    create_txt = create_txt_file(task4_output)

    # Define the task dependencies:
    # task1_output runs before task2_output and task3_output
    # Both task2_output and task3_output run before task4_output
    # task4_output runs before create_txt_file
    task1_output >> [task2_output, task3_output]
    [task2_output, task3_output] >> task4_output
    task4_output >> create_txt

# Instantiate the DAG
dag_instance = taskflow_dag()
