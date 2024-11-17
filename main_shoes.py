import sqlite3
from table_data import *
import os

# Connect to SQLite database (or create it if it doesn't exist)
dir_path = 'SQL_Analyst'
db_path = os.path.join(dir_path, 'shoes.db')
conn = sqlite3.connect(db_path)
create_table = False

cursor = conn.cursor()

# Create the Shoes table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Shoes (
    Id CHAR(10) PRIMARY KEY,
    Brand CHAR(10) NOT NULL,
    Type CHAR(250) NOT NULL,
    Color CHAR(250) NOT NULL,
    Price DECIMAL(8, 2) NOT NULL,
    Desc VARCHAR(750) NULL
);
""")

conn.commit()

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

# Commit changes
conn.commit()

# Function to insert data into the Shoes table
def insert_shoe(table, id, brand, type_, color, price, desc=None):
    cursor.execute("""
    INSERT INTO Shoes (Id, Brand, Type, Color, Price, Desc)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (id, brand, type_, color, price, desc))
    conn.commit()

# Function to insert data into the Shoes table
def insert_to_table(table, id, brand, type_, color, price, desc=None):
    # Using parameterized query to prevent SQL injection
    query = f"INSERT INTO {table} (Id, Brand, Type, Color, Price, Desc) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (id, brand, type_, color, price, desc))
    conn.commit()

# Function to retrieve all shoes from the table
def get_all_shoes(order_col='', order_type='ASC'):
    if not order_col:
        cursor.execute("SELECT * FROM Shoes")
    else:
        cursor.execute(f"SELECT * FROM Shoes ORDER BY {order_col} {order_type}")

    return cursor.fetchall()

# Function to find a shoe by brand
def get_shoes_by_brand(brand):
    cursor.execute("SELECT * FROM Shoes WHERE Brand = ?", (brand,))
    return cursor.fetchall()

# Function to find a shoe by brands
def get_shoes_by_brands(brand_list):
    # Create the correct number of placeholders based on the length of brand_list
    placeholders = ', '.join(['?'] * len(brand_list))
    query = f"SELECT * FROM Shoes WHERE Brand IN ({placeholders})"
    cursor.execute(query, brand_list)
    return cursor.fetchall()

# Function to find a shoe by brand
def get_shoes_by_brand_wildcard(brand):
    cursor.execute("SELECT * FROM Shoes WHERE Brand like ?", (brand,))
    return cursor.fetchall()

# Function to find a shoe by price
def get_shoes_by_price(low_price, high_price):
    cursor.execute("SELECT * FROM Shoes WHERE Price BETWEEN ? AND ?", (low_price, high_price,))
    return cursor.fetchall()


# Function to find a shoe price squared alias
def get_shoes_using_operator_alias():
    cursor.execute("SELECT Color, Brand, Price, Price * Price as SquarePrice FROM Shoes")
    return cursor.fetchall()

# Function to find aggregate shoe price - ignores nulls
def get_shoes_using_operator_alias():
    # cursor.execute("SELECT SUM(Price) as avg_price FROM Shoes")
    # cursor.execute("SELECT AVG(Price) as avg_price FROM Shoes")
    cursor.execute("SELECT COUNT(DISTINCT Price) as avg_price FROM Shoes WHERE Price BETWEEN 75 AND 85")
    return cursor.fetchall()

# Function to find a brand with more than 2 items
def get_shoes_grouped():
    query = """
    SELECT 
    Brand
    ,Count (*) as num_items
    FROM Shoes
    GROUP BY Brand
    HAVING COUNT (*) >= 1
    ORDER BY num_items ASC
    """
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == '__main__':
    # Example: Inserting a sample shoe record
    # List of shoe data to be inserted
    
    # Inserting each shoe into the Shoes table
    if create_table:
        for shoe in shoes_data:
            insert_to_table('Shoes', *shoe)
        
    # Fetch and print all shoes
    fetched_shoes = get_all_shoes() 
    # fetched_shoes = get_all_shoes(order_col='Desc', order_type='ASC') 

    # fetched_shoes = get_shoes_by_brand('Vance')
    # fetched_shoes = get_shoes_by_brand('Vancde')
    # fetched_shoes = get_shoes_by_brands(['Vance', 'Nike', 'Adidas'])

    # fetched_shoes = get_shoes_by_price(low_price=80, high_price=86)
    # fetched_shoes = get_shoes_by_brand_wildcard('N%')
    
    # fetched_shoes = get_shoes_using_operator_alias()
    # fetched_shoes = get_shoes_grouped()


    for shoe in fetched_shoes:
        print(shoe)

    # Close the connection when done (usually at the end of the program)
    conn.close()
