from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, check_admin

app = Flask(__name__)
app.secret_key = "va-secret-key"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    admin = check_admin(username, password)

    if admin:
        session["admin"] = admin["username"]
        session["role"] = admin["role"]
        return redirect(url_for("home"))
    else:
        return render_template("home.html", error="Invalid username or password")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    session.pop("role", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5002)