import datetime as dt
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2023, 8, 5),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('jinja_sql_dag',
         default_args=default_args,
         description='A DAG with Jinja templating in SQL context',
         schedule_interval=dt.timedelta(days=1),
         catchup=False,
         ) as dag:


    # Task 1: Create final destination table if it doesn't exist
    create_table_task = PostgresOperator(
        task_id='clean_destination_postgresql',
        sql="""
        CREATE TABLE IF NOT EXISTS final_destination (
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
    """,
        postgres_conn_id='postgresql_connection',
        dag=dag
        )

    # Task 2: Incremental insert with Jinja
    """
    {{ ds }}: The execution date as YYYY-MM-DD.
    {{ ds_nodash }}: The execution date as YYYYMMDD.
    {{ tomorrow_ds }}: The day after the execution date as YYYY-MM-DD.
    {{ yesterday_ds }}: The day before the execution date as YYYY-MM-DD.
    """

    incremental_insert = """
        INSERT INTO final_destination
        SELECT * FROM public.sales
        WHERE load_date between {{ yesterday_ds }} and {{ ds }};
    """

    incremental_insert_task = PostgresOperator(
        task_id='incremental_insert_task',
        postgres_conn_id='postgresql_connection',
        sql=incremental_insert,
    )

    # Task 3: Ensuring idempotent data loading
    # Assuming that rank_game and load_date make the record unique
    idempotent_insert = """
        DELETE FROM final_destination WHERE load_date = '{{ ds }}';
        INSERT INTO final_destination
        SELECT * FROM public.sales WHERE load_date = '{{ ds }}';
    """

    idempotent_insert_task = PostgresOperator(
        task_id='idempotent_insert_task',
        postgres_conn_id='postgresql_connection',
        sql=idempotent_insert,
    )

    # Setting task dependencies
    create_table_task >> incremental_insert_task >> idempotent_insert_task
