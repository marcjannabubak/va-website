from flask import Flask, render_template, request, redirect, url_for, session, send_file
import io
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
    board = Board.get_board_by_id(1)
    posts = Post.get_posts_by_board(1)
    return render_template("home.html", board=board, posts=posts)



#admin functions routes
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
        board = Board.get_board_by_id(1)
        posts = Post.get_posts_by_board(1)
        return render_template("home.html", error="Invalid username or password", board=board, posts=posts)


@app.route("/logout")
def logout():
    session.pop("admin", None)
    session.pop("role", None)
    return redirect(url_for("home"))



@app.route("/edit")
@admin_required
def edit():
    return render_template("edit.html")

#post functions routes

@app.route("/add_post/<int:IDboard>", methods=["GET", "POST"])
@admin_required
def add_post_page(IDboard):
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date = request.form["date"]

        admin = Admin.get_admin_by_username(session["admin"])
        IDadmin = admin["IDadmin"]

        Post.add_post(title, content, date, IDboard, IDadmin)
        return redirect(url_for("board_page", IDboard=IDboard))

    board = Board.get_board_by_id(IDboard)
    return render_template("addPost.html", board=board)

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


#archive item functions routes

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
        pdf_file = request.files.get("pdf_file")

        if pdf_file and pdf_file.filename:
            pdfName = pdf_file.filename
            pdfData = pdf_file.read()
        else:
            existing = ArchiveItem.get_archive_item_by_id(IDarchiveItem)
            pdfName = existing["pdfName"]
            pdfData = existing["pdfData"]

        ArchiveItem.edit_archive_item(IDarchiveItem, year, author, name, pdfName, pdfData)
        return redirect(url_for("home"))

    item = ArchiveItem.get_archive_item_by_id(IDarchiveItem)
    return render_template("editArchiveItem.html", item=item)

@app.route("/delete_archive_item/<int:IDarchiveItem>", methods=["POST"])
@admin_required
def delete_archive_item(IDarchiveItem):
    ArchiveItem.delete_archive_item(IDarchiveItem)
    return redirect(url_for("home"))


#timeline event functions routes

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

@app.route("/timeline/<int:IDtimelineEvent>")
def timeline_event_page(IDtimelineEvent):
    event = TimelineEvent.get_timeline_event_by_id(IDtimelineEvent)
    return render_template("timelineevent.html", event=event)


#board functions routes
@app.route("/board/<int:IDboard>")
def board_page(IDboard):
    board = Board.get_board_by_id(IDboard)
    posts = Post.get_posts_by_board(IDboard)
    return render_template("board.html", board=board, posts=posts)

@app.route("/resources")
def resources():
    board2 = Board.get_board_by_id(2)
    board3 = Board.get_board_by_id(3)
    posts2 = Post.get_posts_by_board(2)
    posts3 = Post.get_posts_by_board(3)
    return render_template("resources.html", board2=board2, board3=board3, posts2=posts2, posts3=posts3)
 
@app.route("/archive")
def archive():
    items = ArchiveItem.get_all_archive_items()
    return render_template("archive.html", items=items)

@app.route("/archive/<int:IDarchiveItem>")
def archive_item_page(IDarchiveItem):
    item = ArchiveItem.get_archive_item_by_id(IDarchiveItem)
    return render_template("archiveItem.html", item=item)

@app.route("/archive/<int:IDarchiveItem>/pdf")
def serve_archive_pdf(IDarchiveItem):
    item = ArchiveItem.get_archive_item_by_id(IDarchiveItem)
    return send_file(io.BytesIO(item["pdfData"]), mimetype="application/pdf", download_name=item["pdfName"])

@app.route("/art_term/<int:IDartTerm>/image")
def serve_art_term_image(IDartTerm):
    term = ArtTerms.get_art_term_by_id(IDartTerm)
    return send_file(io.BytesIO(term["image"]), mimetype="image/jpeg")

#art term functions routes

@app.route("/art_terms")
def art_terms():
    terms = ArtTerms.get_all_art_terms()
    return render_template("artTerms.html", terms=terms)

@app.route("/add_art_term", methods=["GET", "POST"])
@admin_required
def add_art_term():
    if request.method == "POST":
        title = request.form["title"]
        definition = request.form["definition"]
        image_file = request.files["image_file"]
        imageData = image_file.read()

        admin = Admin.get_admin_by_username(session["admin"])
        IDadmin = admin["IDadmin"]

        ArtTerms.add_art_term(title, definition, imageData, IDadmin)
        return redirect(url_for("art_terms"))

    return render_template("addArtTerm.html")

@app.route("/edit_art_term/<int:IDartTerm>", methods=["GET", "POST"])
@admin_required
def edit_art_term(IDartTerm):
    if request.method == "POST":
        title = request.form["title"]
        definition = request.form["definition"]
        image_file = request.files.get("image_file")
        imageData = image_file.read() if image_file and image_file.filename else None

        if imageData is None:
            existing = ArtTerms.get_art_term_by_id(IDartTerm)
            imageData = existing["image"]

        ArtTerms.edit_art_term(IDartTerm, title, definition, imageData)
        return redirect(url_for("home"))

    term = ArtTerms.get_art_term_by_id(IDartTerm)
    return render_template("editArtTerm.html", term=term)




@app.route("/delete_art_term/<int:IDartTerm>", methods=["POST"])
@admin_required
def delete_art_term(IDartTerm):
    ArtTerms.delete_art_term(IDartTerm)
    return redirect(url_for("home"))


#main function to run app.py
if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5002)
