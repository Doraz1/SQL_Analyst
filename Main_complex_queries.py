import sqlite3
from table_data import *
import os

# Connect to SQLite database (or create it if it doesn't exist)
dir_path = 'SQL_Analyst'
shoes_db_path = os.path.join(dir_path, 'shoes.db')
orders_db_path = os.path.join(dir_path, 'orders.db')
conn_shoes = sqlite3.connect(shoes_db_path)
conn_orders = sqlite3.connect(orders_db_path)

cursor_shoes = conn_shoes.cursor()
cursor_orders = conn_orders.cursor()

def get_orders_of_adidas_shoes_1():
    # Query to get Adidas shoe IDs from shoes.db
    cursor_shoes.execute("""
                         SELECT Id 
                         FROM shoes 
                         WHERE brand = 'Adidas'
                         """
                         )

    adidas_shoes_ids_raw = cursor_shoes.fetchall()

    # adidas_shoe_ids = [row[0] for row in ]
    # If there are no Adidas shoes, return an empty list
    if not adidas_shoes_ids_raw:
        return []
    adidas_shoes_ids = [item[0] for item in adidas_shoes_ids_raw]

    print(adidas_shoes_ids)
    # Use the shoe IDs to query orders of Adidas shoes in orders.db
    placeholder = ', '.join('?' for _ in adidas_shoes_ids)  # For safe parameterization
    query = f"SELECT * FROM orders WHERE ShoeId IN ({placeholder})"
    cursor_orders.execute(query, adidas_shoes_ids)
    return cursor_orders.fetchall()

def get_orders_of_adidas_shoes_2():
     # Query to get Adidas shoe IDs from shoes.db
    cursor_shoes.execute("""
                         SELECT OrderId, ShoeID, Quantity, OrderDate
                         FROM orders
                         WHERE Brand IN 
                         (SELECT Id 
                         FROM shoes 
                         WHERE brand = 'Adidas') 
                         
                         """
                         )
# Example usage
adidas_orders = get_orders_of_adidas_shoes_1() # SQLite approach instead of nested
for order in adidas_orders:
    print(order)

# Close connections
conn_shoes.close()
conn_orders.close()

