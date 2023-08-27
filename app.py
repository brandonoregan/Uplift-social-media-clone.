from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from forms import SignUpForm, LoginForm
from config import Config
from models import db, Post, Like, Comment
from flask_bcrypt import Bcrypt



# create an object of the Flask class
app = Flask(__name__)

# load config settings from config.py
app.config.from_object(Config)

# initialize the SQLAlchemy instance with the app
db.init_app(app)

# crate object of LoginManager class
login_manager = LoginManager()

# configure object for login
login_manager.init_app(app)

# redirect users to login page when trying to access restricted pages
login_manager.login_view = 'render_login'

from models import User

# this function instructs flask_login how to retireve user from db 
@login_manager.user_loader
def load_user(user_id):
    if user_id == 'None':
        return None
    return User.query.get(int(user_id))


# create an object from the Bcrypt class
bcrypt = Bcrypt(app)


# This decorater activate the associated function when the specified route is accessed.
@app.route("/", methods=["GET", "POST"])
def signup():
    """Identify request method, "post" updates database with associated data, "get" will render associated form"""
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_pw)
        # Should this login user go before db commit or after?
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("render_home"))
    return render_template("index.html", form=form)


# This decorater activate the associated function when the specified route is accessed.
@app.route("/login", methods=["GET", "POST"])
def render_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('render_profile'))
    return render_template("login.html", form=form)


# This decorater activate the associated function when the specified route is accessed.
@app.route("/home", methods=["GET", "POST"])
@login_required
def render_home():
    return render_template("home.html")


# This decorater activate the associated function when the specified route is accessed.
@app.route("/profile", methods=["GET", "POST"])
@login_required
def render_profile():
    return render_template("profile.html")


# This decorator will redirect the user, activating the render_login function
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("render_login"))


# Create all db tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
