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
from models import User


# Class for the login form
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        [validators.Length(min=6), validators.InputRequired()],
    )
    password = PasswordField(
        "Password",
        [validators.InputRequired()],
    )
    submit = SubmitField("Login")


# Class for the sign up form which inherits the login class
class SignUpForm(FlaskForm):
    email = StringField("Email", [validators.InputRequired()])
    username = StringField(
        "Username",
        [validators.Length(min=6), validators.InputRequired()],
    )
    password = PasswordField(
        "Password",
        [validators.InputRequired()],
    )
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                message="Username already exists. Please choose another username."
            )


class commentForm(FlaskForm):
    comment = StringField("What do you think?", [validators.InputRequired()])
    post_id = HiddenField(name="post_id")
    submit3 = SubmitField("Send")


class likeForm(FlaskForm):
    post_id = HiddenField()
    submitLike = SubmitField("Like")


class imageForm(FlaskForm):
    upload = FileField("Upload Picture")
    submit = SubmitField("Upload file")


class postForm(FlaskForm):
    title = StringField(
        "Post title:", render_kw={"placeholder": "Tell us about what you're wearing?"}
    )
    submit = SubmitField("Upload post")


# class editCommentForm(FlaskForm):
#     submitEdit = SubmitField('Edit Comment')
#     post_id = HiddenField()
#     edit = StringField([validators.InputRequired()])
