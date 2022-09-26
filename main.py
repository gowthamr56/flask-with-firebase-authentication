from unicodedata import name
from flask import Flask, render_template, request, flash, redirect, url_for, session
from firebase import signup, signin, auth

app = Flask(__name__)

@app.route("/home", methods=["GET", "POST"])
def home():
    if "user" in session:
        if request.method == "POST":
            return redirect(url_for("logout"))
        return render_template("home.html")
    else:
        return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            message, category = signin(email, password)
            session["user"] = email
            if category == "success":
                if message == "email not verified":
                    flash("Check your e-mail to done a e-mail verification")
                    return redirect(url_for("home"))
                return redirect(url_for("home"))                
            else:
                flash(message)
        else:
            flash("Please, enter e-mail and password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 != password2:
            flash("Both password should be same", category="error")
        else:
            message, category = signup(email, password1)
            if category == "success":
                return render_template("verify_email.html")
            else:
                flash(message)

    return render_template("sign_up.html")

@app.route("/verify")
def verify_email():
    return render_template("verify_email.html")

if __name__ == "__main__":
    app.secret_key = "this_key_is_secret"
    app.run(debug=True)