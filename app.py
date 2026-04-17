from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, check_admin,  get_admin_by_username, add_post, get_all_posts
from functools import wraps


app = Flask(__name__)
app.secret_key = "va-secret-key"
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function

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

@app.route("/edit")
@admin_required
def edit():
    return render_template("edit.html")


@app.route("/add_post", methods=["GET", "POST"])
@admin_required
def add_post_page():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date = request.form["date"]

        admin = get_admin_by_username(session["admin"])

        IDboard = 1
        IDadmin = admin["IDadmin"]

        add_post(title, content, date, IDboard, IDadmin)
        return redirect(url_for("home"))

    return render_template("add_post.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5002)