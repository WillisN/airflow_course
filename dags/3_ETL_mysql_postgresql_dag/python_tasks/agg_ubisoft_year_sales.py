from airflow.providers.postgres.hooks.postgres import PostgresHook


def staging_agg_ubisoft_year_sales():
    postgres_hook = PostgresHook(postgres_conn_id='postgresql_connection')
    postgres_hook.run("""
        DROP TABLE IF EXISTS agg_ubisoft_year_sales;
        CREATE TABLE agg_ubisoft_year_sales AS
        SELECT name_game
                        , year_game
                        , Global_Sales
                        , sum(Global_Sales) OVER (PARTITION BY year_game) AS year_Global_Sales 
                        FROM sales
                        WHERE publisher = 'Ubisoft'
                        ORDER BY year_game DESC
                """)

if __name__ == "__main__": 
    staging_agg_ubisoft_year_sales()

