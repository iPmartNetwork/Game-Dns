from functools import wraps
from flask import session
import sqlite3

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def login_user(username, password):
    conn = sqlite3.connect('/app/database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cur.fetchone()
    conn.close()
    if user:
        session['username'] = username
        return True
    return False

def logout_user():
    session.pop('username', None)
