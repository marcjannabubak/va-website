import tkinter as tk
from tkinter import messagebox
import requests


FLASK_URL=
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    try:
        response = requests.post(FLASK_URL, json={'username': username, 'password': password})
       