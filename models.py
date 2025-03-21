import sqlite3
from hashlib import sha256

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  email TEXT UNIQUE, 
                  password TEXT)''')
    conn.commit()
    conn.close()

def register_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                  (email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    c.execute("SELECT id FROM users WHERE email = ? AND password = ?", 
              (email, hashed_password))
    user = c.fetchone()
    conn.close()
    return user