import os
import sqlite3

# Create database folder if missing
BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "jon_oil_gas.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# Connect to the correct database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop old products table if it exists
cursor.execute("DROP TABLE IF EXISTS products")

# Create products table
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        image TEXT NOT NULL
    )
""")

# Insert fresh products
products = [
    ("Cooking Gas 12kg", 12000, "High-quality cooking gas cylinder.", "gas12.jpg"),
    ("Engine Oil 5L", 8000, "Premium engine oil for all vehicles.", "engineoil5l.jpg"),
    ("Diesel 50L", 35000, "Diesel fuel for generators and engines.", "diesel50l.jpg"),
    ("Gas Burner", 4500, "Durable gas burner for home cooking.", "gasburner.jpg"),
    ("Generator 3.5KVA", 95000, "Powerful generator for home and office.", "generator3_5kva.jpg")
]

cursor.executemany(
    "INSERT INTO products (name, price, description, image) VALUES (?, ?, ?, ?)",
    products
)

conn.commit()
conn.close()

print("✅ Fresh database created successfully!")
