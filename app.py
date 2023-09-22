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
from forms import (
    SignUpForm,
    LoginForm,
    commentForm,
    likeForm,
    imageForm,
    postForm,
    deleteForm,
)
from config import Config
from models import db, Post, Like, Comment, Image
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import desc
import os
from werkzeug.utils import secure_filename
from functions import (
    updateLikes,
    signUpUser,
    resetFormPost,
    addPost,
    loginUser,
    deleteComment,
    addComment,
    uploadImage,
    updateProfileImage,
)


# create an object of the Flask class
app = Flask(__name__)

# configure prepooling on datavase connections
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

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

# Set the path to the upload directory within the 'static' folder
path = os.getcwd()

# configure content length
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the 'static' directory relative to the current script
UPLOAD_FOLDER = os.path.join(current_dir, "static", "img")

# configure uploade folder
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


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

    return render_template("index.html", form=form)


@app.route("/", methods=["POST"])
def signup():
    """Handle form submission for POST request"""
    form = SignUpForm()

    if form.validate_on_submit():
        # add new user to database
        signUpUser(form, bcrypt, User, db, flash, login_user)

        # redirect user to approriate page
        return redirect(url_for("render_home"))

    # If form validation fails, render the appropriate page
    return render_template("index.html", form=form)


@app.route("/login")
def render_login():
    """Render specified page for GET request"""
    form = LoginForm()
    return render_template("login.html", form=form)


# This decorater activates the associated function when the specified route is accessed.
@app.route("/login", methods=["POST"])
def login():
    """Handle form submission for POST request"""

    form = LoginForm()

    if form.validate_on_submit():
        # Check user credentials and login user
        loginUser(User, form, bcrypt, login_user, redirect, url_for, flash)

    return render_template("login.html", form=form)


@app.route("/home", methods=["GET"])
def render_home():
    """Render specified page for GET request"""

    # Generate wtforms
    newComForm = commentForm()
    newLikeForm = likeForm()
    dp_form = imageForm()
    post_form = postForm()
    delete_form = deleteForm()

    # Storing database queries in variables
    all_users = User.query.all()
    all_posts = Post.query.order_by(Post.id.desc()).all()
    all_comments = Comment.query.all()
    all_images = Image.query.all()
    recent_comments = Comment.query.order_by(desc(Comment.timestamp)).all()
    recent_comments_reversed = list(reversed(recent_comments))
    user_dp = Image.query.filter_by(id=current_user.pic_id).first()
    most_recent_image = db.session.query(Image).order_by(desc(Image.id)).first()

    # Dictionary to store user with the comments they made
    comment_user_mapping = {}

    # Store current user time in variable
    now = datetime.utcnow()

    # Sets a key:value pair holding, connecting comment to user
    for comment in recent_comments:
        user = db.session.get(User, comment.user_id)
        comment_user_mapping[comment] = user

    return render_template(
        "home.html",
        newComForm=newComForm,
        all_posts=all_posts,
        newLikeForm=newLikeForm,
        all_comments=all_comments,
        recent_comments_reversed=recent_comments_reversed,
        comment_user_mapping=comment_user_mapping,
        user_dp=user_dp,
        dp_form=dp_form,
        post_form=post_form,
        most_recent_image=most_recent_image,
        all_users=all_users,
        Image=Image,
        delete_form=delete_form,
        now=now,
        all_images=all_images,
    )


@app.route("/home/post", methods=["POST"])
def upload_post():
    """Handle form submission for POST request"""

    # Genereate wtforms
    post_form = postForm()

    # Add post to db
    addPost(db, Image, Post, current_user, post_form, desc)

    # Reset post form to default
    resetFormPost(Image, db, desc, post_form)

    return redirect(url_for("render_home"))


# This decorater activate the associated function when the specified route is accessed.
@app.route("/home/delete", methods=["POST"])
@login_required
def delete_comment():
    """Handle form submission for POST request"""

    # Delete comment from UI and db
    deleteComment(request, db, Comment, current_user)

    return redirect(url_for("render_home"))


@app.route("/home/comment", methods=["POST"])
@login_required
def post_comment():
    """Handle form submission for POST request"""

    newComForm = commentForm()

    if request.method == "POST" and newComForm.validate_on_submit():
        # Add comment to UI post and db
        addComment(datetime, Comment, current_user, request, newComForm, db, desc)

    return redirect(url_for("render_home"))


@app.route("/home/like", methods=["POST"])
@login_required
def post_like():
    """Handle form submission for POST request"""

    newLikeForm = likeForm()

    if newLikeForm.validate_on_submit():
        # Increment like count on UI and db
        updateLikes(current_user, request, Post, Like, db)

    return redirect(url_for("render_home"))


@app.route("/home/image", methods=["POST"])
@login_required
def upload_post_img():
    """Handle form submission for POST request"""

    # Uploads image to db
    uploadImage(request, secure_filename, app, os, flash, Image, current_user, db)

    return redirect(
        url_for(
            "render_home",
        )
    )


# This decorater activate the associated function when the specified route is accessed.
@app.route("/profile")
@login_required
def render_profile():
    """Render specified page for GET request"""
    dp_form = imageForm()

    # Find users display picture
    user_dp = Image.query.filter_by(id=current_user.pic_id).first()

    # Find all post that are generate from the current user
    filtered_posts = Post.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "profile.html",
        dp_form=dp_form,
        username=current_user.username,
        user_dp=user_dp,
        filtered_posts=filtered_posts,
        Image=Image,
    )


@app.route("/profile/picture", methods=["POST"])
@login_required
def post_dp():
    """Handle form submission for POST request"""

    # Update profile image on UI and DB
    updateProfileImage(
        request, secure_filename, app, os, flash, Image, current_user, db, User
    )

    return redirect(
        url_for(
            "render_profile",
        )
    )


# This decorator will redirect the user, activating the login function
@app.route("/logout")
@login_required
def logout():
    """Render specified page for GET request"""
    logout_user()
    return redirect(url_for("login"))


# Create all db tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
