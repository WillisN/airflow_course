from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
import random
from datetime import datetime, timedelta

def extract_mysql():
    mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')
    records = mysql_hook.get_records('SELECT * FROM db_videos_games_source.sales')
    return records

def generate_random_timestamp():
    base_date = datetime(2024, 1, 1)
    random_days = random.randint(0, 30)  # Generates random days between 0 and 30
    return base_date + timedelta(days=random_days)

def load_postgres(records):
    logging.getLogger().setLevel(logging.WARNING)
    postgres_hook = PostgresHook(postgres_conn_id='postgresql_connection')
    for record in records:
        # Append random timestamp to each record
        record_with_timestamp = (*record, generate_random_timestamp())
        postgres_hook.run(
            """INSERT INTO sales VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            parameters=record_with_timestamp
        )

if __name__ == "__main__":
    source = extract_mysql()
    load_postgres(source)
