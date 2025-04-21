from flask import Blueprint, render_template, request, redirect, session, url_for

auth = Blueprint("auth", __name__)

# Sample user
USER_CREDENTIALS = {
    "admin": "password123"
}

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if USER_CREDENTIALS.get(username) == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
