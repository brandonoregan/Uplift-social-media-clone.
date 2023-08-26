from flask import Flask, render_template, url_for, redirect
from forms import SignUpForm, LoginForm

# Create an instance of the Flask class
app = Flask(__name__)

# Create secrkey key
app.config["SECRET_KEY"] = "secret"


# This decorater will render the associated template when the specified route is accessed.
@app.route("/", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    return render_template("index.html", form=form)


# This decorater will render the associated template when the specified route is accessed.
@app.route("/login")
def render_login():
    form = LoginForm()
    return render_template("login.html", form=form)


# This decorater will render the associated template when the specified route is accessed.
@app.route("/home")
def render_home():
    return render_template("home.html")


# This decorater will render the associated template when the specified route is accessed.
@app.route("/profile")
def render_profile():
    return render_template("profile.html")


# This decorator will redirect the user, activating the render_login function
@app.route("/logout")
def logout():
    return redirect(url_for("render_login"))


if __name__ == "__main__":
    app.run(debug=True)
