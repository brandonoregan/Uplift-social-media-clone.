from flask import Flask, render_template, url_for, redirect

# Create an instance of the Flask class
app = Flask(__name__)


# Routes for index.html
# This decorater will render the associated template when the specified route is accessed.
@app.route("/")
def index():
    return render_template("index.html")


# This decorater will render the associated template when the specified route is accessed.
# @app.route("/", methods=['POST'])
# def index():
#     return render_template("index.html")


# Routes for register.html
# This decorater will render the associated template when the specified route is accessed.
@app.route("/signup")
def render_signup():
    return render_template("signup.html")


# Routes for login.html
# This decorater will render the associated template when the specified route is accessed.
@app.route("/login")
def render_login():
    return render_template("login.html")


# Routes for home.html
# This decorater will render the associated template when the specified route is accessed.
@app.route("/home")
def render_home():
    return render_template("home.html")


# Routes for profile.html
# This decorater will render the associated template when the specified route is accessed.
@app.route("/profile")
def render_profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
      return redirect(url_for("render_login"))


if __name__ == "__main__":
    app.run(debug=True)
