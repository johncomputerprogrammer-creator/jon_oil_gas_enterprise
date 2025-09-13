import sqlite3
import os

# Get base directory (where create_tables.py is)
BASE_DIR = os.path.dirname(__file__)

# Create db folder path
DB_FOLDER = os.path.join(BASE_DIR, "db")

# Create db folder if it doesn't exist
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)
    print("✅ 'db' folder created successfully!")

# Set full database path
DB_PATH = os.path.join(DB_FOLDER, "jon_oil_gas.db")

# Connect to database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ---------------------- CREATE TABLES ----------------------

# Users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password_hash TEXT,
    is_affiliate INTEGER DEFAULT 0,
    affiliate_code TEXT
)
''')

# Products table
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    price_kobo INTEGER NOT NULL,
    stock INTEGER DEFAULT 0,
    image TEXT
)
''')

# Orders table
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total_kobo INTEGER,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paystack_reference TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Order items table
c.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price_kobo INTEGER,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

# Transactions table
c.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    reference TEXT,
    amount_kobo INTEGER,
    status TEXT,
    gateway_response TEXT,
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES orders(id)
)
''')

# Affiliates table
c.execute('''
CREATE TABLE IF NOT EXISTS affiliates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    affiliate_code TEXT UNIQUE,
    commission_percent REAL DEFAULT 5.0,
    balance_kobo INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Affiliate clicks
c.execute('''
CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    affiliate_id INTEGER,
    product_id INTEGER,
    ip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(affiliate_id) REFERENCES affiliates(id)
)
''')

# Subscriptions table
c.execute('''
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plan_name TEXT,
    paystack_subscription_code TEXT,
    status TEXT,
    started_at TIMESTAMP,
    next_billing_date TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()

print(f"✅ Database & tables created successfully at: {DB_PATH}")
