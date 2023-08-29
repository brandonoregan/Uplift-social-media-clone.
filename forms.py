from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, HiddenField
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
    submit = SubmitField("Sign up")


# Class for the sign up form which inherits the login class
class SignUpForm(LoginForm):
    email = StringField("Email", [validators.InputRequired()])

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                message="Username already exists. Please choose another username."
            )


class commentForm(FlaskForm):
    comment = StringField("What do you think?", [validators.InputRequired()])
    post_id = HiddenField()
    submit3 = SubmitField('Send')
