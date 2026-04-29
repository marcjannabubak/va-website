from flask import Flask, render_template, request, redirect, url_for, session
from database import ArchiveItem, add_timeline_event, get_all_timeline_events, init_db, check_admin,  get_admin_by_username, add_post, get_all_posts
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
    posts =get_all_posts()
    return render_template("home.html", posts=posts)


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
        posts = get_all_posts()
        return render_template("home.html", error="Invalid username or password", posts=posts)


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

    return render_template("addPost.html")


@app.route("/add_archive_item", methods=["GET", "POST"])
@admin_required
def add_archive_item():
    if request.method == "POST":
        year = int(request.form["year"])
        author = request.form["author"]
        name = request.form["name"]
        pdf_file = request.files["pdf_file"]
        pdfName = pdf_file.filename
        pdfData = pdf_file.read()

        admin = get_admin_by_username(session["admin"])
        IDadmin = admin["IDadmin"]

        item = ArchiveItem(year, author, name, pdfName, pdfData, IDadmin)
        item.upload()

        return redirect(url_for("home"))

    return render_template("addArchiveItem.html")

@app.route("/add_timeline_event", methods=["GET", "POST"])
@admin_required
def add_timeline_event_page():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        add_timeline_event(title, description, date)
        return redirect(url_for("home"))

    return render_template("addTimelineEvent.html")

@app.route("/timeline")
def timeline():
    events = get_all_timeline_events()
    return render_template("timeline.html", events=events)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5002)