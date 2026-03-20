import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify
import requests



#login system
app = Flask(__name__)
users={
    "admin", "password",
    "test","testing"}
@app.route('/login',methods=['POST'] )
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and check_password_hash(users[username], password):
        return jsonify({"status":"success","message": "Login successful!"}), 200
    else:
        return jsonify({"status":"error", "message": "Invalid credentials!"}), 401
if __name__=='__main__':
    app.run(debug=True)



#db from uml 
def init_db():
    conn = sqlite3.connect('va.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Admin (
        IDadmin INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ArchiveItem (
        IDarchiveItem INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        author TEXT NOT NULL,
        name TEXT NOT NULL,
        image TEXT NOT NULL,
        IDadmin INTEGER,
        FOREIGN KEY (IDadmin) REFERENCES Admin(IDadmin)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Board (
        IDboard INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        resourceOrDP1OrDP2 TEXT NOT NULL,
        IDadmin INTEGER,
        FOREIGN KEY (IDadmin) REFERENCES Admin(IDadmin)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Post (
        IDpost INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        IDboard INTEGER,
        IDadmin INTEGER,
        FOREIGN KEY (IDboard) REFERENCES Board(IDboard),
        FOREIGN KEY (IDadmin) REFERENCES Admin(IDadmin)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS TimelineEvent (
        IDtimelineEvent INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        date TEXT NOT NULL
    )''')

   
    #conn.commit()
   
  

#methods for db
class Admin:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

   
    def __str__(self):
        return f"Admin: {self.username}, Role: {self.role}"


class ArchiveItem:
    def __init__(self, year, author, name, image):
        self.year = year
        self.author = author
        self.name = name
        self.image = image

    def upload(self):
        # to do - saving to db algorithm
        pass

    def sort():
        # to do - sorting algorithm
        pass
    def authenticate():
        # to do - authentication algorithm
        pass

    def __str__(self):
        return f"{self.name} by {self.author} ({self.year})"


class Board:
    def __init__(self, title, resourceOrDP1OrDP2):
        self.title = title
        self.resourceOrDP1OrDP2 = resourceOrDP1OrDP2

    def __str__(self):
        return f"Board: {self.title}"


class Post:
    def __init__(self, title, content, date, IDboard):
        self.title = title
        self.content = content
        self.date = date
        self.IDboard = IDboard

    def __str__(self):
        return f"Post: {self.title} on {self.date}"


class TimelineEvent:
    def __init__(self, title, description, date):
        self.title = title
        self.description = description
        self.date = date

    def __str__(self):
        return f"{self.title} - {self.date}"


if __name__ == '__main__':
    init_db()