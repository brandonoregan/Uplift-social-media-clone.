from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        [
            validators.Length(
                min=6
            ), 
            validators.InputRequired()
        ],
    )
    password = PasswordField("Password")
    submit = SubmitField("Sign up")


class SignUpForm(LoginForm):
    email = StringField(
        "Email", 
        [
            validators.InputRequired()
        ]
    )
