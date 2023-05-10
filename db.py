import sqlite3
import os


def create():
    if not os.path.isfile('blog.db'):
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users
        (userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        blocked INTEGER NOT NULL)
                       """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs
        (blogID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(userID) REFERENCES users(userID))
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments
        (commentID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        blogID INTEGER,
        text TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(userID) REFERENCES users(userID),
        FOREIGN KEY(blogID) REFERENCES blogs(blogID))
        """)
        
        conn.commit()
        conn.close()


def getConnection():
    conn = sqlite3.connect('blog.db')
    return conn