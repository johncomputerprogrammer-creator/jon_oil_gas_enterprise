from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for flash messages
app.config['SECRET_KEY'] = 'my_secret_key'

# Initialize database
db = SQLAlchemy(app)

# Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"

# Route for homepage
@app.route("/")
def home():
    return render_template("index.html")

# Contact route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            message = request.form["message"]

            # Save to database
            new_message = Contact(name=name, email=email, message=message)
            db.session.add(new_message)
            db.session.commit()

            # Success message
            flash("Your message has been sent successfully!", "success")
            return redirect(url_for("contact"))

        except Exception as e:
            # If there's an error, show an error message
            flash(f"Something went wrong: {e}", "error")
            return redirect(url_for("contact"))

    return render_template("contact.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
