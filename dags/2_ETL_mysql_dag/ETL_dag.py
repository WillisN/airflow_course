from datetime import datetime, date
import csv
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook

def transform_data():
    today = date.today()
    final = [] # Create an empty list to store the final data

    count_nintendo_games = 0 # Initialize a counter to keep track of the number of Nintendo games

    # Open the CSV file for reading
    with open('/opt/airflow/dags/2_ETL_mysql_dag/staging/extract_videosgames_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            publisher_column = row[5]

            # Check if the game's publisher is 'Nintendo'
            if publisher_column == 'Nintendo':
                name_column = row[1].upper()    # Convert the game name to uppercase
                platform_column = row[2]        # Extract the platform column
                year_game = row[3]            # Extract the year column
                genre_column = row[4]           # Extract the genre column
                transform_date = today.strftime('%Y-%m-%d') # Format today's date as 'YYYY-MM-DD'

                # Create a tuple containing the relevant data for the current Nintendo game
                end = count_nintendo_games, name_column, platform_column, year_game, genre_column, transform_date                    
                final.append(end) # Append the tuple to the final list    
                count_nintendo_games += 1 # Increment the count of Nintendo games


    # Define the header for the CSV file
    header = ['count_nintendo_games', 'name_column', 'platform_column', 'year_game', 'genre_column', 'transform_date']
    # Open the new CSV file for writing
    with open('/opt/airflow/dags/2_ETL_mysql_dag/staging/transform_nintendo_games.csv', 'w', newline='') as output_file:
        # Create a CSV writer object
        writer = csv.writer(output_file)
        writer.writerow(header) # Write the header to the CSV file
        writer.writerows(final) # Write each Nintendo game's data to a row in the CSV file


def load_data():
    csv_file_path = '/opt/airflow/dags/2_ETL_mysql_dag/staging/transform_nintendo_games.csv'

    # Establish a connection to the MySQL database using the MySQL hook
    mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')

    # Open the transformed CSV file for reading
    with open(csv_file_path, 'r') as csv_file:
        # Skip the header line
        next(csv_file)

        # Read each line from the CSV and insert it into the list
        for record in csv.reader(csv_file):
            count_nintendo_games = record[0]
            name_column = record[1]
            platform_column = record[2]
            year_game = record[3]
            genre_column = record[4]
            transform_date = record[5]

            # Define the MySQL query to insert data into the table
            insert_query = '''
                INSERT INTO nintendo_games (GameCount, Name, Platform, Year, Genre, Date)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            record_line = (count_nintendo_games, name_column, platform_column, year_game, genre_column, transform_date)

            # Execute the MySQL query to insert data into the table
            mysql_hook.run(insert_query, parameters=record_line)

# Define default arguments for the DAG
default_args = {
    'owner': 'Willis',        # Owner of the DAG
    'retries': 0,                  # Number of retries in case of failure (disabled)
    'start_date': datetime(2023, 7, 1),  # Start date of the DAG
    'is_paused_upon_creation': True  # This will pause the DAG upon creation
}

# Define the DAG
dag = DAG(
    'ETL_analytics_video_games',             # DAG ID
    default_args=default_args,     # Default arguments for the DAG
    description='Analytics ETL',
    tags=['Data Engineering courses',"Intermediate"],
    catchup=False,              # Do not backfill past runs when DAG is created
    schedule='@daily'  # Schedule interval (run at midnight every day)
)


# E - Extract
extract_data_from_source = BashOperator(
    task_id='extract_data_from_source',
    bash_command='curl -Lb "cookies.txt" "https://raw.githubusercontent.com/WillisN/airflow_course/main/sources/vgsales.csv" -o /opt/airflow/dags/2_ETL_mysql_dag/staging/extract_videosgames_data.csv',
    dag=dag
)

# T - Transform
transform_data_from_source = PythonOperator(
    task_id='transform_data_from_source',
    python_callable=transform_data,
    dag=dag
)

# L - Load
load_data_to_mysql = PythonOperator(
    task_id='load_data_to_mysql',
    python_callable=load_data,
    dag=dag
)

extract_data_from_source >> transform_data_from_source >> load_data_to_mysql
