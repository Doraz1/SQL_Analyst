import sqlite3
from datetime import datetime
import random
from table_data import *
import os

# Connect to the SQLite database
dir_path = 'SQL_Analyst'
db_path = os.path.join(dir_path, 'orders.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
create_table = False

# Create the Orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    OrderId CHAR(10) PRIMARY KEY,
    ShoeId CHAR(10) NOT NULL,
    Quantity INTEGER NOT NULL,
    OrderDate TEXT NOT NULL,
    Freight DECIMAL(6, 2) NOT NULL,
    TotalPrice DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ShoeId) REFERENCES Shoes(Id)
);
""")

conn.commit()

# Function to insert an order into the Orders table
def insert_order(order_id, shoe_id, quantity, order_date, freight, total_price):
    cursor.execute("""
    INSERT INTO Orders (OrderId, ShoeId, Quantity, OrderDate, Freight, TotalPrice)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, shoe_id, quantity, order_date, freight, total_price))
    conn.commit()


# Function to retrieve all orders from the table
def get_all_orders():
    cursor.execute("SELECT * FROM Orders")
    return cursor.fetchall()

if __name__ == '__main__':
    # Insert example orders
    shoe_ids = [shoe[0] for shoe in shoes_data]  # Extract all shoe IDs from shoes_data
    if create_table:
        for i in range(1, 21):
            order_id = f"O{i:04}"  # Generates order IDs like O0001, O0002, etc.
            shoe_id = random.choice(shoe_ids)  # Randomly select a shoe ID
            quantity = random.randint(1, 5)  # Random quantity between 1 and 5
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time
            freight = round(random.uniform(5.0, 20.0), 2)  # Random freight cost between $5 and $20
            # Calculate total price as (price of shoe * quantity) + freight
            shoe_price = next(shoe[4] for shoe in shoes_data if shoe[0] == shoe_id)
            total_price = round((shoe_price * quantity) + freight, 2)

            # Insert the order into the Orders table
            insert_order(order_id, shoe_id, quantity, order_date, freight, total_price)


    orders = get_all_orders()
    for order in orders:
        print(order)

    # Close the connection
    conn.close()