from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


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
