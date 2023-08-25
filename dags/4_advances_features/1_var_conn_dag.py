from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable

default_args = {
    'owner': 'Willis',
    'start_date': datetime(2023, 1, 1),    
}

dag = DAG(
    'variables_connections_dag',
    default_args=default_args,
    description='A simple DAG that uses Variables and Connections',
    tags=['Data Engineering courses',"Advanced"],
    catchup = False,              # Do not backfill past runs when DAG is created
    schedule='@daily',
)

# Define a Variable that can be used across tasks in this DAG
example_variable = Variable.get("variable_test_airflow")

# Define a Connection that represents the database connection to be used
# This assumes you have already created a connection in Airflow with the ID "my_database_conn"
database_connection_id = "postgresql_connection"

# Task 1: Print the value of the example_variable
def print_variable():
    print(f"Example Variable Value: {example_variable}")

task_print_variable = PythonOperator(
    task_id='print_variable',
    python_callable=print_variable,
    dag=dag,
)

# Task 2: Use the database connection to run a SQL query
task_execute_query = BashOperator(
    task_id='execute_query',
    bash_command=f'airflow connections get {database_connection_id}',
    dag=dag,
)

# Define the task order
task_print_variable >> task_execute_query
