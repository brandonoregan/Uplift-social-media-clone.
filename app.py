from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    flash,
    get_flashed_messages,
)
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
    UserMixin,
)
from forms import SignUpForm, LoginForm, commentForm, likeForm, editCommentForm
from config import Config
from models import db, Post, Like, Comment
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import desc
import os
from werkzeug.utils import secure_filename
from functions import updateLikes


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
login_manager.login_view = "login"

from models import User


# this function instructs flask_login how to retireve user from db
@login_manager.user_loader
def load_user(user_id):
    if user_id == "None":
        return None
    user = db.session.get(User, int(user_id))
    # return User.query.get(int(user_id))
    return user


# inject variables for all templates
@app.context_processor
def inject_variable():
    return dict(user=current_user)


# create an object from the Bcrypt class
bcrypt = Bcrypt(app)


@app.route("/")
def render_signup():
    """Render specified page for GET request"""
    form = SignUpForm()
    return render_template('index.html', form=form)


@app.route("/", methods=["POST"])
def signup():
    """Handle form submission for POST request"""
    form = SignUpForm()
    if form.validate_on_submit():
        # Is it better to have seperate varibles or have them directly in user object?
        # Process form data and update databse
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        # Log in the user and redirect to the specified page
        login_user(user)
        return redirect(url_for("home"))
    
    # If form validation fails, re-
    return render_template("index.html", form=form)


@app.route("/login")
def render_login():
    """Render specified page for GET request"""
    form = LoginForm()
    return render_template('login.html', form=form)


# This decorater activates the associated function when the specified route is accessed.
@app.route("/login", methods=["POST"])
def login():
    """Handle form submission for POST request"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Incorrect username or password.")
        else:
            flash("Username does not exist.")
    return render_template("login.html", form=form)


@app.route("/home")
def render_home():
    """Render specified page for GET request"""
    newComForm = commentForm()
    newLikeForm = likeForm()
    all_posts = Post.query.all()
    all_comments = Comment.query.all()
    recent_comments = Comment.query.order_by(desc(Comment.timestamp)).limit(3).all()
    recent_comments_reversed = list(reversed(recent_comments))
    comment_user_mapping = {}
    
    # Sets a key:value pair holding, connecting comment to user
    for comment in recent_comments:
        user = User.query.get(comment.user_id)
        comment_user_mapping[comment] = user

    return render_template(
        "home.html",
        newComForm=newComForm,
        all_posts=all_posts,
        newLikeForm=newLikeForm,
        all_comments=all_comments,
        recent_comments_reversed=recent_comments_reversed,
        comment_user_mapping=comment_user_mapping
    )





# This decorater activate the associated function when the specified route is accessed.
@app.route("/home/comment", methods=["POST"])
@login_required
def post_comment():

    newComForm = commentForm()

    if request.method == "POST" and newComForm.validate_on_submit():
        user_id = current_user.id
        post_id = request.form.get("post_id")
        content = newComForm.comment.data
        timestamp = datetime.utcnow()
        comment = Comment(
            user_id=user_id, post_id=post_id, content=content, timestamp=timestamp
        )
        db.session.add(comment)
        db.session.commit()
        newComForm.comment.data = ""
    else:  # remove later, keep around for now for debugging
        print("ERROR ERROR ERROR ERROR")
        for field, errors in newComForm.errors.items():
            print(f"Field: {field}, Errors: {errors}")

    return redirect(url_for('render_home'))

# This decorater activate the associated function when the specified route is accessed.
@app.route("/home/like", methods=["POST"])
@login_required
def post_like():
    
    newLikeForm = likeForm()

    # Example of how to refactor code, function is in functions.py
    if newLikeForm.validate_on_submit():
        updateLikes(current_user, request, Post, Like, db)

    return redirect(url_for('render_home'))


# This decorater activate the associated function when the specified route is accessed.
@app.route("/profile")
@login_required
def render_profile():
    return render_template("profile.html")


# This decorator will redirect the user, activating the login function
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Create all db tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
