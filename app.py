import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "super_secret_key"

# -------------------
# DATABASE CONNECTION
# -------------------
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "db", "jon_oil_gas.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------
# HOME PAGE
# -------------------
@app.route("/")
def home():
    return redirect(url_for("products"))

# -------------------
# PRODUCTS PAGE
# -------------------
@app.route("/products")
def products():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, price, description, image FROM products")
    products = c.fetchall()
    conn.close()
    return render_template("products.html", products=products)

# -------------------
# REGISTER PAGE
# -------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
            conn.close()
            flash("Registration successful! You can now login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already exists!", "danger")
    return render_template("register.html")

# -------------------
# LOGIN PAGE
# -------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password_hash=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["name"]
            flash("Login successful!", "success")
            return redirect(url_for("products"))
        else:
            flash("Invalid email or password!", "danger")
    return render_template("login.html")

# -------------------
# LOGOUT
# -------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out!", "info")
    return redirect(url_for("home"))

# -------------------
# PAYMENT PAGE
# -------------------
@app.route("/payment")
def payment():
    return render_template("payment.html")

# -------------------
# CONTACT PAGE
# -------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")

# -------------------
# START SERVER
# -------------------
if __name__ == "__main__":
    if not os.path.exists("db"):
        os.makedirs("db")
    app.run(debug=True)
