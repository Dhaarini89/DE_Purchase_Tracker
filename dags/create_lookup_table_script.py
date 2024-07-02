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
def create_lookup_table():
 #Creating lookup Table
 sql = f"""
    CREATE TABLE IF NOT EXISTS lookup_category (
    item_name VARCHAR(255) NOT NULL,
    item_category VARCHAR(50));

    """ 
 cur.execute(sql)
 conn.commit()
 # Define categories for each item
 item_to_category = {
    "Laptop": "Electronics",
    "Smartphone": "Electronics",
    "Headphones": "Electronics",
    "Tablet": "Electronics",
    "Office Chair": "Furniture",
    "Monitor": "Electronics",
    "Keyboard": "Electronics",
    "Mouse": "Electronics",
    "Printer": "Electronics",
    "Webcam": "Electronics",
    "Desk Lamp": "Furniture",
    "External Hard Drive": "Electronics",
    "Router": "Electronics",
    "Smartwatch": "Electronics",
    "Bluetooth Speaker": "Electronics",
    "Coffee Maker": "Kitchen Appliances",
    "Electric Kettle": "Kitchen Appliances",
    "Blender": "Kitchen Appliances",
    "Microwave Oven": "Kitchen Appliances",
    "Toaster": "Kitchen Appliances",
    "Vacuum Cleaner": "Home Appliances",
    "Washing Machine": "Home Appliances",
    "Refrigerator": "Home Appliances",
    "Dishwasher": "Home Appliances",
    "Electric Shaver": "Personal Care",
    "Hair Dryer": "Personal Care",
    "Air Conditioner": "Home Appliances",
    "Heater": "Home Appliances",
    "Fan": "Home Appliances",
    "Table": "Furniture",
    "Chair": "Furniture",
    "Bookshelf": "Furniture",
    "Bed": "Furniture",
    "Wardrobe": "Furniture"
 }

 # Generate INSERT script
 insert_script = "INSERT INTO lookup_category (item_name, item_category) VALUES\n"
 values = []
 for item_name, category in item_to_category.items():
    values.append(f"('{item_name}', '{category}')")
 insert_script += ",\n".join(values) + ";"
  
 cur.execute(insert_script)
 conn.commit() 
 cur.close()
 conn.close()
 
if __name__ == "__main__":
  create_lookup_table()
