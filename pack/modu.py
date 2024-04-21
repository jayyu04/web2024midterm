import sqlite3
import csv
import json


def create_database(database_path, users_file, books_file):
    conn = sqlite3.connect(database_path)

    conn.execute('''CREATE TABLE IF NOT EXISTS users
                 (userid INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS books
                 (book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 publisher TEXT NOT NULL,
                 year INTEGER NOT NULL)''')

    conn.commit()
    conn.close()
    print("資料庫及資料表建立完成。")   # 測試指令
    import_users(database_path, users_file)
    import_books(database_path, books_file)


def import_users(database_path, users_file):
    conn = sqlite3.connect(database_path)
    with open(users_file, 'r') as file:
        users = [(row['username'], row['password'])
                 for row in csv.DictReader(file)]
    print("要寫入的使用者資料：", users)  # 測試指令
    conn.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        users
    )
    conn.commit()
    conn.close()


def import_books(database_path, books_file):
    conn = sqlite3.connect(database_path)
    with open(books_file, 'r') as file:
        books = json.load(file)
    print("要寫入的書籍資料：", books)  # 測試指令
    for book in books:
        conn.execute(
            "INSERT INTO books (title, author, publisher, year) "
            "VALUES (?, ?, ?, ?)",
            (book['title'], book['author'], book['publisher'], book['year'])
        )

    conn.commit()
    conn.close()


def login(database_path, username, password):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def add_book(database_path, title, author, publisher, year):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("""
        INSERT INTO books (title, author, publisher, year)
        VALUES (?, ?, ?, ?)
        """, (title, author, publisher, year))
    conn.commit()
    conn.close()


def delete_book(database_path, title):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE title=?", (title,))
    conn.commit()
    conn.close()


def update_book(database_path, title, new_title, author, publisher, year):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("""
        UPDATE books
        SET title=?, author=?, publisher=?, year=?
        WHERE title=?
        """, (new_title, author, publisher, year, title))
    conn.commit()
    conn.close()


def search_books(database_path, keyword):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("""
        SELECT book_id, title, author, publisher, year
        FROM books
        WHERE title LIKE ? OR author LIKE ?
        """, ('%'+keyword+'%', '%'+keyword+'%'))
    result = c.fetchall()
    conn.close()
    # print(result)   # 測試指令
    return result


def get_all_books(database_path):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    result = c.fetchall()
    conn.close()
    return result
