import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2


# Database connection parameters
dbname = "postgres"
user = "airflow"
password = "airflow"
host = "postgres"

# Connect to the database
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cur = conn.cursor()


def try_execute_sql(sql: str,msg:str):
    try:
        cur.execute(sql)
        conn.commit()
        print(f"Executed {msg} creation successfully")
    except Exception as e:
        print(f"Couldn't execute {msg} creation due to exception: {e}")
        conn.rollback()


def create_tables():
    #Bronze table Creation
    create_bronze_table_sql = f"""
    CREATE TABLE IF NOT EXISTS bronze_purchase_load (
    item_name VARCHAR(255) NOT NULL,
    date_of_purchase DATE NOT NULL,
    cost NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    purchased_by VARCHAR(255) NOT NULL,
    payment_method VARCHAR(50) NOT NULL );

    """
    msg="Bronze table"
    try_execute_sql(create_bronze_table_sql,msg)

    #Silvertable Creation
    create_silver_table_sql = f"""
    CREATE TABLE IF NOT EXISTS silver_purchase_load (
    item_name VARCHAR(255) NOT NULL,
    date_of_purchase DATE NOT NULL,
    cost NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    purchased_by VARCHAR(255) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    purchased_category VARCHAR(50) );

    """
    msg="Silver table"
    try_execute_sql(create_silver_table_sql,msg)

    #Gold table Creation
    create_gold_table_sql = f"""
    CREATE TABLE IF NOT EXISTS gold_purchase_load (
    year_month VARCHAR(6) NOT NULL,
    total_cost NUMERIC(10, 2) NOT NULL,
    total_quantity INTEGER NOT NULL );

    """
    msg="Gold table"
    try_execute_sql(create_gold_table_sql,msg)

    cur.close()
    conn.close()


if __name__ == "__main__":
    create_tables()
