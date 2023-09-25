from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    validators,
    ValidationError,
    HiddenField,
    FileField,
)
from flask_wtf.file import FileRequired
from models import User


# Class for the login form
class LoginForm(FlaskForm):
    # Creates a string field input with specified validators
    username = StringField(
        "Username",
        [validators.Length(min=6), validators.InputRequired()],
        render_kw={"placeholder": "Username"},
    )
    # Creates a password input with specified validators
    password = PasswordField(
        "Password", [validators.InputRequired()], render_kw={"placeholder": "Password"}
    )
    # Creates a submit button
    submit = SubmitField("Login", id="submitButton")


# Class for the sign up form which inherits the login class
class SignUpForm(FlaskForm):
    email = StringField(
        "Email:", [validators.InputRequired()], render_kw={"placeholder": "Email"}
    )
    username = StringField(
        "Username:",
        [validators.Length(min=6), validators.InputRequired()],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password:", [validators.InputRequired()], render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Sign up", id="submitButton")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                message="Username already exists. Please choose another username."
            )

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()

        if existing_user_email:
            raise ValidationError(
                message="Email already exists. Please choose another email."
            )


# Class for new comment form
class commentForm(FlaskForm):
    comment = StringField("What do you think?", [validators.InputRequired()])
    post_id = HiddenField(name="post_id")
    submit3 = SubmitField("Send", id="submitButton")


# Class for delete button form on post
class deleteForm(FlaskForm):
    comment_id = HiddenField("comment_id")
    submit = SubmitField("Delete", id="submitButton")


# Class for like button form on post
class likeForm(FlaskForm):
    post_id = HiddenField()
    submitLike = SubmitField("Like", id="submitButton")


# Class for upload image form
class imageForm(FlaskForm):
    upload = FileField("Upload Picture", validators=[FileRequired()])
    submit = SubmitField("Upload file", id="submitButton")


# Class for creating post on post form
class postForm(FlaskForm):
    title = StringField(
        "Post title:", render_kw={"placeholder": "Tell us about what you're wearing?"}
    )
    submit = SubmitField("Upload post", id="submitButton")
