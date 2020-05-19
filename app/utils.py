from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from .db import query_db, query_db_object


def login_required(f):
    def decorator(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    decorator.__name__ = f.__name__
    return decorator


def authenticate_user(username, password):
    user_row = query_db("SELECT password FROM users WHERE username = ?", username, one=True)
    return check_password_hash(user_row[0], password) if user_row else None


def new_user(username, password, sex, cooking_level):
    query_db("""
        INSERT INTO users (username, password, sex, role_id, cooking_level_id) 
        VALUES (?, ?, ?,
            (SELECT role_id FROM roles WHERE name LIKE 'User'), 
            (SELECT cooking_level_id FROM cooking_levels WHERE name = ? )
        )
    """, username, generate_password_hash(password), sex, cooking_level, commit=True)


def add_user_to_session(username):
    query_db("UPDATE users SET last_login_date = DATETIME('now', 'localtime') WHERE username = ?",
             username, commit=True)
    row = query_db_object("""
        SELECT u.username, r.name AS role_name, u.creation_date, u.last_login_date, u.sex
        FROM users u  
        INNER JOIN roles r USING(role_id)
        WHERE username = ? 
    """, username, one=True)

    session.permanent = True
    session['user'] = row


def change_password(username, password):
    query_db("UPDATE users SET password = ? WHERE username = ?",
             generate_password_hash(password), username, commit=True)


def get_recipes_list():
    pass


def get_cooking_levels_list():
    return query_db_object("SELECT name, description FROM cooking_levels")


def get_food_categories_list():
    return query_db_object("SELECT name FROM food_categories")
