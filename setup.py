import sqlite3


def connect_db():
    return sqlite3.connect("va.db")


def add_admin(conn):
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = "admin"

    c = conn.cursor()
    c.execute(
        "INSERT INTO Admin (username, password, role) VALUES (?, ?, ?)",
        (username, password, role)
    )
    conn.commit()

    print("Admin added.\n")


def view_admins(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Admin")
    admins = c.fetchall()

    print("\n=== Admins ===")
    for admin in admins:
        print(admin)
    print()

def add_board(conn):
    title = input("enter board title: ")
    resourceOrDP1OrDP2 = input("Enter board type: ")
    IDadmin = input("Enter admin ID: ")

    c = conn.cursor()
    c.execute(
        "INSERT INTO Board (title, resourceOrDP1OrDP2, IDadmin) VALUES (?, ?, ?)",
        (title, resourceOrDP1OrDP2, IDadmin)
    )
    conn.commit()

    print("board added\n")



def run():
    conn = connect_db()

    while True:
        print("==== ADMIN MENU ====")
        print("1: Add admin")
        print("2: View admins")
        print("3: add board")
        print("4: Exit")
        choice = input("Choose: ")

        if choice == "1":
            add_admin(conn)

        elif choice == "2":
            view_admins(conn)
        
        elif choice == "3":
            add_board(conn)

        elif choice == "4":
            print("Exiting db")
            conn.close()
            break

        else:
            print("not a valid choice.\n")


if __name__ == "__main__":
    run()