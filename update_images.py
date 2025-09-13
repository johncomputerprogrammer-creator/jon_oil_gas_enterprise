import sqlite3
import os

# Path to your database
DB_PATH = os.path.join(os.getcwd(), "db", "jon_oil_gas.db")

# Connect to the database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Make sure 'image' column exists
try:
    c.execute("ALTER TABLE products ADD COLUMN image TEXT;")
except sqlite3.OperationalError:
    # Column already exists
    pass

# Update products with image filenames
updates = [
    ("gas12.jpg", "Cooking Gas 12kg"),
    ("engineoil5l.jpg", "Engine Oil 5L"),
    ("diesel50l.jpg", "Diesel 50L"),
    ("gasburner.jpg", "Gas Burner"),
    ("generator3_5kva.jpg", "Generator 3.5KVA"),
]

for img, name in updates:
    c.execute("UPDATE products SET image=? WHERE name=?", (img, name))

conn.commit()
conn.close()

print("✅ Products table updated with correct image filenames!")
