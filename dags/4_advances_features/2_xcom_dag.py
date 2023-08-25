# Import necessary modules from the Airflow library.
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Default arguments for the DAG. These are common configurations that apply to the DAG and its tasks.
default_args = {
    'owner': 'Willis',                          # Owner of the DAG
    'start_date': datetime(2023, 7, 1),          # Start date for the DAG
}

# Instantiate a DAG. This represents a collection of tasks that run on a schedule.
dag = DAG(
    'xcom_example_dag',                          # Unique identifier for the DAG
    default_args=default_args,                   # Apply the default arguments
    description='An example DAG demonstrating XCom usage',   # Description of the DAG's purpose
    tags=['Data Engineering courses',"Advanced"],
    schedule='@daily',                  # How often to run the DAG. '@daily' means once a day.
    catchup=False                                # If set to True, Airflow will execute all instances between the DAG's start_date and the current day. Setting to False means skipping missed instances.
)

# Python function that pushes a value into XCom.
def push_xcom_value(**kwargs):
    value_to_push = "This is the pushed value!"
    kwargs['ti'].xcom_push(key='sample_key', value=value_to_push)  # Using the xcom_push method to push a value to XCom

# Define a task in the DAG using the PythonOperator, which will run the above function.
push_task = PythonOperator(
    task_id='push_task',                        # Unique identifier for this task
    python_callable=push_xcom_value,            # Python function to be executed by this task
    provide_context=True,                       # This ensures the function gets the necessary keyword arguments like 'ti'
    dag=dag                                     # Link this task to the previously defined DAG
)

# Python function that pulls a value from XCom and then prints it.
def pull_xcom_value(**kwargs):
    ti = kwargs['ti']                           # Extract the task instance from the provided kwargs
    pulled_value = ti.xcom_pull(task_ids='push_task', key='sample_key')  # Use xcom_pull to retrieve the value from XCom
    print(f"Pulled Value from XCom: {pulled_value}")

# Another task using the PythonOperator to run the above function.
pull_task = PythonOperator(
    task_id='pull_task',
    python_callable=pull_xcom_value,
    provide_context=True,
    dag=dag
)

# Setting the order in which the tasks will execute.
# push_task will execute first, followed by pull_task, and finally bash_task.
push_task >> pull_task
