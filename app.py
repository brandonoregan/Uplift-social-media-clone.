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
from functions import updateLikes


# create an object of the Flask class
app = Flask(__name__)

#
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

# Set the path to the upload directory within the 'static' folder -- change comment
path = os.getcwd()
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the 'static' directory relative to the current script
UPLOAD_FOLDER = os.path.join(current_dir, "static", "img")

# Now, 'static_dir' contains the absolute path to the 'static' directory
print(UPLOAD_FOLDER)
print("@@@@@@@@@@")

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
        # Is it better to have seperate varibles or have them directly in user object?
        # Process form data and update databse
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed_pw)

        db.session.add(user)
        db.session.commit()

        flash("User added successfullly!")

        # Log in the user and redirect to the specified page
        login_user(user)
        return redirect(url_for("render_home"))

    # If form validation fails, re-
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
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("render_home"))
            else:
                flash("Incorrect username or password.")
        else:
            flash("Username does not exist.")
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

    # Collect all instances from associated tables
    all_users = User.query.all()
    all_posts = Post.query.order_by(Post.id.desc()).all()
    all_comments = Comment.query.all()

    # query the database for particular responses
    recent_comments = Comment.query.order_by(desc(Comment.timestamp)).all()
    recent_comments_reversed = list(reversed(recent_comments))
    image = Image.query.filter_by(id=current_user.pic_id).first()
    most_recent_image = db.session.query(Image).order_by(desc(Image.id)).first()
    comment_user_mapping = {}
    now = datetime.utcnow()

    # Sets a key:value pair holding, connecting comment to user
    for comment in recent_comments:
        # user = User.query.get(comment.user_id) same as line below but the old way
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
        image=image,
        dp_form=dp_form,
        post_form=post_form,
        most_recent_image=most_recent_image,
        all_users=all_users,
        Image=Image,
        delete_form=delete_form,
        now=now,
    )


@app.route("/home/post", methods=["POST"])
def upload_post():
    """Handle form submission for POST request"""
    post_form = postForm()

    user_id = current_user.id
    content = post_form.title.data
    img_tup = db.session.query(Image.id).order_by(Image.id.desc()).first()
    pic_id = img_tup[0]

    # create instance of model
    post = Post(user_id=user_id, content=content, pic_id=pic_id)

    # add post to db
    db.session.add(post)
    db.session.commit()

    # Update database, change most recent image draft == False.
    most_recent_image = db.session.query(Image).order_by(desc(Image.id)).first()
    most_recent_image.draft = False
    db.session.commit()

    post_form.title.data = ""

    return redirect(url_for("render_home"))


# This decorater activate the associated function when the specified route is accessed.
@app.route("/home/delete", methods=["POST"])
@login_required
def delete_comment():
    newDeleteForm = deleteForm()

    if request.method == "POST" and newDeleteForm.validate_on_submit():
        comment = Comment.query.get(comment_id)

        if comment and comment.user_id == current_user.id:
            db.session.delete(comment)
            db.session.commit()

            return redirect(url_for("render_home"))


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

    return redirect(url_for("render_home"))


@app.route("/home/like", methods=["POST"])
@login_required
def post_like():
    newLikeForm = likeForm()

    # Example of how to refactor code, function is in functions.py
    if newLikeForm.validate_on_submit():
        updateLikes(current_user, request, Post, Like, db)

    return redirect(url_for("render_home"))


@app.route("/home/image", methods=["POST"])
@login_required
def upload_post_img():
    # Get uploaded image data

    user_id = current_user.id
    file = request.files["upload"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    mimetype = file.mimetype
    draft = True

    # Save the uploaded image to the server
    file.save(filepath)

    # Check if file exists
    if not file:
        flash("No file uploaded")

    # Create Image instance and add to db
    img = Image(
        filepath=filepath,
        mimetype=mimetype,
        name=filename,
        user_id=user_id,
        draft=draft,
    )

    db.session.add(img)
    db.session.commit()

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

    image = Image.query.filter_by(id=current_user.pic_id).first()
    username = current_user.username

    filtered_posts = Post.query.filter_by(user_id=current_user.id).all()

    # usersPost is equal to each post in all post where the current user.id == allpost.userid

    return render_template(
        "profile.html",
        dp_form=dp_form,
        username=username,
        image=image,
        filtered_posts=filtered_posts,
        Image=Image,
    )


@app.route("/profile/picture", methods=["POST"])
@login_required
def post_dp():
    # Get uploaded image data

    user_id = current_user.id
    file = request.files["upload"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    mimetype = file.mimetype

    # Save the uploaded image to the server
    file.save(filepath)

    # Check if file exists
    if not file:
        flash("No file uploaded")

    # Create Image instance and add to db
    img = Image(
        filepath=filepath,
        mimetype=mimetype,
        name=filename,
        user_id=user_id,
    )
    db.session.add(img)
    db.session.commit()

    # update associated tables
    image_id = img.id

    user_id = current_user.id
    user = db.session.get(User, user_id)
    user.pic_id = image_id
    db.session.commit()

    return redirect(
        url_for(
            "render_profile",
        )
    )


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
