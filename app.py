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
    return User.query.get(int(user_id))


# inject variables for all templates
@app.context_processor
def inject_variable():
    return dict(user=current_user)


# create an object from the Bcrypt class
bcrypt = Bcrypt(app)


# This decorater activates the associated function when the specified route is accessed.
@app.route("/", methods=["GET", "POST"])
def signup():
    """Identify request method, "post" updates database with associated data, "get" will render associated form"""
    form = SignUpForm()
    if form.validate_on_submit():
        # Is it better to have seperate varibles or have them directly in user object?
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed_pw)
        # Should this login user go before db commit or after?
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("home"))
    return render_template("index.html", form=form)


# This decorater activates the associated function when the specified route is accessed.
@app.route("/login", methods=["GET", "POST"])
def login():
    """Identify request method, 'Post': varifies information against database. 'Get': renders associated template"""
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


# This decorater activate the associated function when the specified route is accessed.
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    newComForm = commentForm()
    newLikeForm = likeForm()
    editComment = editCommentForm()
    all_posts = Post.query.all()
    all_comments = Comment.query.all()

    if newComForm.validate_on_submit():
        user_id = current_user.id
        post_id = request.form.get("post_id")
        content = newComForm.comment.data
        timestamp = datetime.utcnow()
        comment = Comment(
            user_id=user_id, post_id=post_id, content=content, timestamp=timestamp
        )
        db.session.add(comment)
        db.session.commit()
    else:  # remove later, keep around for now for debugging
        print("ERROR ERROR ERROR ERROR")
        for field, errors in newComForm.errors.items():
            print(f"Field: {field}, Errors: {errors}")

    if editComment.validate_on_submit():
        post_id = request.form.get("post_id")
        edit = editComment.edit.data
        comment = Comment.query.filter_by(id=post_id).first()


        if comment:
            comment.content = edit
            db.session.commit()


    if newLikeForm.validate_on_submit():
        user_id = current_user.id
        post_id = request.form.get("post_id")

        post = Post.query.filter_by(id=post_id).first()
        if post:
            post.likes = post.likes + 1
            db.session.flush()
            db.session.refresh(post)
            db.session.commit()

        like = Like(user_id=user_id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return render_template(
        "home.html",
        newComForm=newComForm,
        all_posts=all_posts,
        newLikeForm=newLikeForm,
        all_comments=all_comments,
        editComment=editComment
    )


# "url_for(""static"", filename=""img/fashion-1.jpg"")"


# This decorater activate the associated function when the specified route is accessed.
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
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
