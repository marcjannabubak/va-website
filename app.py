from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "va-secret-key"

admins = {
    "DPteacher1": "art2020000",
    "PreDPteacher": "art1010000"
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username in admins and admins[username] == password:
        session["admin"] = username
    else:
        return render_template("home.html", error="Invalid username or password")

    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=5002)