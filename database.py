from datetime import date
import sqlite3


#this creates the db tables from the uml diagram
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
        pdfName TEXT NOT NULL,
        pdfData BLOB NOT NULL,
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
    c.execute('''CREATE TABLE IF NOT EXISTS ArtTerms(
             IDartTerm INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             definition TEXT NOT NULL
             image BLOB NOT NULL
             FOREIGN KEY (IDadmin) REFERENCES Admin(IDadmin)
         )''' )
   
    conn.commit()




   






#methods for db
class Admin:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
#cheecks if the admin exists in the db
    def check_admin(username, password):
        conn = sqlite3.connect('va.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            "SELECT * FROM Admin WHERE username = ? AND password = ?",
            (username, password)
        )
        admin = c.fetchone()

        
        return admin

#finds and returns the admin with the username from db

    def get_admin_by_username(username):
        conn = sqlite3.connect('va.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Admin WHERE username = ?", (username,))
        admin = c.fetchone()


        return admin
   
    def __str__(self):
        return f"Admin: {self.username}, Role: {self.role}"


class ArchiveItem:
    def __init__(self, year, author, name, pdfName, pdfData, IDadmin):
        self.year = year
        self.author = author
        self.name = name
        self.pdfName = pdfName
        self.pdfData = pdfData
        self.IDadmin = IDadmin

    def upload(self):
        conn = sqlite3.connect("va.db")
        c = conn.cursor()

        c.execute("""
            INSERT INTO ArchiveItem (year, author, name, pdfName, pdfData, IDadmin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.year,
            self.author,
            self.name,
            self.pdfName,
            self.pdfData,
            self.IDadmin
        ))

        conn.commit()
    

    def sort(self, items):
        n = len(items)
        i = 0
        while i < n - 1:
            j = 0
            while j < n - i - 1:
                if items[j].year < items[j + 1].year:
                    t = items[j]
                    items[j] = items[j + 1]
                    items[j + 1] = t
                j += 1
            i += 1
        return items
   
    def get_all_archive_items():
        conn = sqlite3.connect("va.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM ArchiveItem ORDER BY year DESC")
        items = c.fetchall()

    
        return items
    def get_archive_item_by_id(IDarchiveItem):
        conn = sqlite3.connect("va.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM ArchiveItem WHERE IDarchiveItem = ?", (IDarchiveItem,))
        item = c.fetchone()
        return item

    def __str__(self):
        return f"{self.name} by {self.author} ({self.year})"


class Board:
    def __init__(self, title, resourceOrDP1OrDP2):
        self.title = title
        self.resourceOrDP1OrDP2 = resourceOrDP1OrDP2

    def __str__(self):
        return f"Board: {self.title}"

    def get_board_by_id(IDboard):
        conn = sqlite3.connect("va.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Board WHERE IDboard = ?", (IDboard,))
        board = c.fetchone()
        return board
    
class Post:
    def __init__(self, title, content, date, IDboard):
        self.title = title
        self.content = content
        self.date = date
        self.IDboard = IDboard

    def __str__(self):
        return f"Post: {self.title} on {self.date}"
    def get_all_posts():
        conn = sqlite3.connect('va.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Post ORDER BY IDpost DESC")
        posts = c.fetchall()

    
        return posts

    def add_post(title, content, date, IDboard, IDadmin):
        conn = sqlite3.connect('va.db')
        c = conn.cursor()

        c.execute(
            "INSERT INTO Post (title, content, date, IDboard, IDadmin) VALUES (?, ?, ?, ?, ?)",
            (title, content, date, IDboard, IDadmin)
        )

        conn.commit()

class TimelineEvent:
    def __init__(self, title, description, date):
        self.title = title
        self.description = description
        self.date = date
    def add_timeline_event(title, description, date):
        conn = sqlite3.connect("va.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO TimelineEvent (title, description, date) VALUES (?, ?, ?)",
            (title, description, date)
        )
        conn.commit()
    

    def get_all_timeline_events():
        conn = sqlite3.connect("va.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM TimelineEvent ORDER BY date DESC")
        events = c.fetchall()
    
        return events
    def __str__(self):
        return f"{self.title} - {self.date}"

    class ArtTerms:
        def __init__(self, title, definition, image):
            self.title = title
            self.definition = definition
            self.image = image

        def add_art_term(title, defiiniton, image, IDadmin):
            conn = sqlite3.connect("va.db")
            c = conn.cursor()

            c.execute(
                "INSERT INTO ArtTerms (title, definition, image, IDadmin) VALUES (?, ?, ?, ?)",
                (title, defiiniton, image, IDadmin)
            )
            conn.commit()

        def __str__(self):
            return f"Art Term: {self.title}"

if __name__ == '__main__':
    init_db()