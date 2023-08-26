from flask import Flask, render_template, url_for, redirect, request
from forms import SignUpForm, LoginForm
from config import Config
from models import db, User, Post, Like, Comment


# create an instance of the Flask class
app = Flask(__name__)

# load config settings from config.py
app.config.from_object(Config)

# initialize the SQLAlchemy instance with the app
db.init_app(app)

# This decorater will render the associated template when the specified route is accessed.
@app.route("/", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if request.method == "POST":
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('render_home'))
    return render_template("index.html", form=form)


# This decorater will render the associated template when the specified route is accessed.
@app.route("/login", methods=["GET", "POST"])
def render_login():
    form = LoginForm()
    return render_template("login.html", form=form)


# This decorater will render the associated template when the specified route is accessed.
@app.route("/home", methods=["GET", "POST"])
def render_home():
    return render_template("home.html")


# This decorater will render the associated template when the specified route is accessed.
@app.route("/profile", methods=["GET", "POST"])
def render_profile():
    return render_template("profile.html")


# This decorator will redirect the user, activating the render_login function
@app.route("/logout")
def logout():
    return redirect(url_for("render_login"))


# Create all db tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
