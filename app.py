from flask import Flask, render_template, request, redirect, url_for, session
from database import Admin, ArchiveItem, Board, Post, TimelineEvent, init_db, ArtTerms

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
    posts = Post.get_all_posts()
    return render_template("home.html", posts=posts)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    admin = Admin.check_admin(username, password)

    if admin:
        session["admin"] = admin["username"]
        session["role"] = admin["role"]
        return redirect(url_for("home"))
    
    else:
        posts = Post.get_all_posts()
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

        admin = Admin.get_admin_by_username(session["admin"])

        IDboard = 1
        IDadmin = admin["IDadmin"]

        Post.add_post(title, content, date, IDboard, IDadmin)
        return redirect(url_for("home"))

    return render_template("addPost.html")

@app.route("/edit_post/<int:IDpost>", methods=["GET", "POST"])
@admin_required
def edit_post(IDpost):
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date = request.form["date"]

        Post.edit_post(IDpost, title, content, date)
        return redirect(url_for("home"))

    post = Post.get_post_by_id(IDpost)
    return render_template("editPost.html", post=post)


@app.route("/delete_post/<int:IDpost>", methods=["POST"])
@admin_required
def delete_post(IDpost):
    Post.delete_post(IDpost)
    return redirect(url_for("home"))

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

        admin = Admin.get_admin_by_username(session["admin"])
        IDadmin = admin["IDadmin"]

        item = ArchiveItem(year, author, name, pdfName, pdfData, IDadmin)
        item.upload()

        return redirect(url_for("home"))

    return render_template("addArchiveItem.html")

@app.route("/edit_archive_item/<int:IDarchiveItem>", methods=["GET", "POST"])
@admin_required
def edit_archive_item(IDarchiveItem):
    if request.method == "POST":
        year = int(request.form["year"])
        author = request.form["author"]
        name = request.form["name"]
        pdf_file = request.files["pdf_file"]
        pdfName = pdf_file.filename
        pdfData = pdf_file.read()

        ArchiveItem.edit_archive_item(IDarchiveItem, year, author, name, pdfName, pdfData)
        return redirect(url_for("home"))

    item = ArchiveItem.get_archive_item_by_id(IDarchiveItem)
    return render_template("editArchiveItem.html", item=item)

@app.route("/delete_archive_item/<int:IDarchiveItem>", methods=["POST"])
@admin_required
def delete_archive_item(IDarchiveItem):
    ArchiveItem.delete_archive_item(IDarchiveItem)
    return redirect(url_for("home"))

@app.route("/add_timeline_event", methods=["GET", "POST"])
@admin_required
def add_timeline_event_page():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        TimelineEvent.add_timeline_event(title, description, date)
        return redirect(url_for("home"))

    return render_template("addTimelineEvent.html")

@app.route("/edit_timeline_event/<int:IDtimelineEvent>", methods=["GET", "POST"])
@admin_required
def edit_timeline_event(IDtimelineEvent):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        TimelineEvent.edit_timeline_event(IDtimelineEvent, title, description, date)
        return redirect(url_for("home"))

    event = TimelineEvent.get_timeline_event_by_id(IDtimelineEvent)
    return render_template("editTimelineEvent.html", event=event)

@app.route("/delete_timeline_event/<int:IDtimelineEvent>", methods=["POST"])
@admin_required
def delete_timeline_event(IDtimelineEvent):
    TimelineEvent.delete_timeline_event(IDtimelineEvent)
    return redirect(url_for("home"))

@app.route("/timeline")
def timeline():
    events = TimelineEvent.get_all_timeline_events()
    return render_template("timeline.html", events=events)

@app.route("/board/<int:IDboard>")
def board_page(IDboard):
    board = Board.get_board_by_id(IDboard)
    return render_template("board.html", board=board)
 
@app.route("/archive")
def archive():
    items = ArchiveItem.get_all_archive_items()
    return render_template("archive.html", items=items)

@app.route("/archive/<int:IDarchiveItem>")
def archive_item_page(IDarchiveItem):
    item = ArchiveItem.get_archive_item_by_id(IDarchiveItem)
    return render_template("archiveItem.html", item=item)


@app.route("/art_terms", methods=["GET", "POST"])
@admin_required
def art_terms():
    if request.method == "POST":
        title = request.form["title"]
        definition = request.form["definition"]
        image_file = request.files["image_file"]
        imageData = image_file.read()

        admin = Admin.get_admin_by_username(session["admin"])
        IDadmin = admin["IDadmin"]

        ArtTerms.add_art_term(title, definition, imageData, IDadmin)
        return redirect(url_for("home"))
    return render_template("artTerms.html")

@app.route("/art_terms_list")
def art_terms_list():
    terms = ArtTerms.get_all_art_terms()
    return render_template("artTerms.html", terms=terms)

@app.route("/edit_art_term/<int:IDartTerm>", methods=["GET", "POST"])
@admin_required
def edit_art_term(IDartTerm):
    if request.method == "POST":
        title = request.form["title"]
        definition = request.form["definition"]
        image_file = request.files["image_file"]
        imageData = image_file.read()

        ArtTerms.edit_art_term(IDartTerm, title, definition, imageData)
        return redirect(url_for("home"))

    term = ArtTerms.get_art_term_by_id(IDartTerm)
    return render_template("editArtTerm.html", term=term)

@app.route("/delete_art_term/<int:IDartTerm>", methods=["POST"])
@admin_required
def delete_art_term(IDartTerm):
    ArtTerms.delete_art_term(IDartTerm)
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5002)