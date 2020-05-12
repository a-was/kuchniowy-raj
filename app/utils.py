from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from .db import query_db


def login_required(f):
    def decorator(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    decorator.__name__ = f.__name__
    return decorator


def authenticate_user(username, password):
    user_row = query_db("SELECT password FROM users WHERE nick = ?", username, one=True)
    return check_password_hash(user_row[0], password) if user_row else None


def new_user(nick, password, sex, cooking_level):
    query_db("""
        INSERT INTO users (nick, password, sex, role_id, cooking_level_id) 
        VALUES (?, ?, ?,
            (SELECT role_id FROM roles WHERE name LIKE 'User'), 
            (SELECT cooking_level_id FROM cooking_levels WHERE name = ? )
        )
    """, nick, generate_password_hash(password), sex, cooking_level, commit=True)


def add_user_to_session(username):
    query_db("UPDATE users SET last_login_date = DATETIME('now', 'localtime') WHERE nick = ?",
             username, commit=True)

    session.permanent = True
    session['user'] = {
        'username': username
    }


def get_all_recipes():
    pass
