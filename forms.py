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
    username = StringField(
        "Username",
        [validators.Length(min=6), validators.InputRequired()],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password", [validators.InputRequired()], render_kw={"placeholder": "Password"}
    )
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


class commentForm(FlaskForm):
    comment = StringField("What do you think?", [validators.InputRequired()])
    post_id = HiddenField(name="post_id")
    submit3 = SubmitField("Send", id="submitButton")


class deleteForm(FlaskForm):
    comment_id = HiddenField(name="comment_id")
    submit = SubmitField("Delete", id="submitButton")


class likeForm(FlaskForm):
    post_id = HiddenField()
    submitLike = SubmitField("Like", id="submitButton")


class imageForm(FlaskForm):
    upload = FileField("Upload Picture", validators=[FileRequired()])
    submit = SubmitField("Upload file", id="submitButton")


class postForm(FlaskForm):
    title = StringField(
        "Post title:", render_kw={"placeholder": "Tell us about what you're wearing?"}
    )
    submit = SubmitField("Upload post", validators=[FileRequired()], id="submitButton")


# class editCommentForm(FlaskForm):
#     submitEdit = SubmitField('Edit Comment')
#     post_id = HiddenField()
#     edit = StringField([validators.InputRequired()])
