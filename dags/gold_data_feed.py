
import psycopg2
import csv
import os

# Database connection parameters
dbname = "postgres"
user = "airflow"
password = "airflow"
host = "postgres"


def gold_data_feed_gen():
     # Connect to the database
     conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
     cur = conn.cursor()
     directory_path = "/opt/airflow/"
      # List files in the directory
     files = os.listdir(directory_path)
     print(files)
     file_nme123="/opt/airflow/tgt/gold_feed.csv"
     cur.execute("SELECT item_category,sum(cost) as cost,sum(quantity) as quantity FROM silver_purchase_load group by item_category")
     rows = cur.fetchall()
     cur.close()
     conn.close()
     if not rows:
        raise ValueError("No data fetched from source")
     with open(file_nme123, 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(["category", "cost", "quantity"])  # Write header
      writer.writerows(rows)

if __name__ == "__main__":
   gold_data_feed_gen()