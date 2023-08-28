from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'Willis',
    'start_date': datetime(2023, 1, 1),  # The date when the DAG starts
    
}

dag = DAG(
    'jinja_dag',             # DAG ID
    default_args=default_args,     # Default arguments for the DAG
    description='A DAG with Jinja templating in SQL context',
    tags=['Data Engineering courses','Advanced'],
    catchup= False,              # Do not backfill past runs when DAG is created
    schedule='0 0 * * *'  # Schedule interval (run at midnight every day)
)


# Task 1: Create final destination table if it doesn't exist
create_table_task = PostgresOperator(
    task_id='clean_destination_postgresql',
    postgres_conn_id='postgresql_connection',
    dag=dag,
    sql="""
    CREATE TABLE IF NOT EXISTS daily_sales (
        rank_game int, 
        name_game varchar(132), 
        platform varchar(4), 
        year_game varchar(4), 
        genre_game varchar(12), 
        publisher varchar(38), 
        NA_Sales decimal(4, 2), 
        EU_Sales decimal(4, 2), 
        JP_Sales decimal(4, 2), 
        Other_Sales decimal(4, 2), 
        Global_Sales decimal(4, 2), 
        load_date date
        );
    """
    )

# Task 2: Delete data with Jinja
delete_data_task = PostgresOperator(
    task_id='idempotent_insert_task',
    postgres_conn_id='postgresql_connection',
    sql="""
    DELETE FROM daily_sales 
    WHERE load_date between {{ yesterday_ds }} and {{ ds }};
    """,
)


# Task 3: Ensuring idempotent data loading and Incremental insert with Jinja

"""
{{ ds }}: The execution date as YYYY-MM-DD.
{{ ds_nodash }}: The execution date as YYYYMMDD.
{{ tomorrow_ds }}: The day after the execution date as YYYY-MM-DD.
{{ yesterday_ds }}: The day before the execution date as YYYY-MM-DD.
"""

incremental_insert_task = PostgresOperator(
    task_id='incremental_insert_task',
    postgres_conn_id='postgresql_connection',
    sql="""
    INSERT INTO daily_sales
    SELECT * FROM public.sales
    WHERE load_date between {{ yesterday_ds }} and {{ ds }};
    """,
)


# Setting task dependencies
create_table_task >> delete_data_task >> incremental_insert_task 
