import tkinter as tk
from tkinter import messagebox
import sqlite3

# Создание базы данных и таблицы пользователей, если они не существуют
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для регистрации нового пользователя
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Регистрация", "Пользователь успешно зарегистрирован!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
    finally:
        conn.close()

# Функция для авторизации пользователя
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        messagebox.showinfo("Авторизация", "Успешная авторизация!")
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")

# Функция для открытия окна регистрации
def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Регистрация")

    tk.Label(registration_window, text="Логин:").pack()
    username_entry = tk.Entry(registration_window)
    username_entry.pack()

    tk.Label(registration_window, text="Пароль:").pack()
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.pack()

    tk.Button(registration_window, text="Зарегистрироваться", command=lambda: register_user(username_entry.get(), password_entry.get())).pack()

# Основное окно приложения
root = tk.Tk()
root.title("Авторизация")

tk.Label(root, text="Логин:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Пароль:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Авторизоваться", command=lambda: login_user(username_entry.get(), password_entry.get())).pack()
tk.Button(root, text="Регистрация", command=open_registration_window).pack()

# Создание базы данных
create_database()

# Запуск основного цикла приложения
root.mainloop()
