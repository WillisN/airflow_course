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

    sql = """
        INSERT INTO target_table_{{ ds_nodash }}
        SELECT * FROM source_table
        WHERE date_column = '{{ ds }}';
    """

    copy_task = PostgresOperator(
        task_id='copy_task',
        postgres_conn_id='my_postgres_conn',
        sql=sql,
    )
