from flask import session, redirect, url_for

from app.db import query_db, query_db_object


def login_required(f):
    def decorator(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('.login'))

    decorator.__name__ = f.__name__
    return decorator


def admin_required(f):
    def decorator(*args, **kwargs):
        if session['user']['role_name'].lower() == 'administrator':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('.index'))

    decorator.__name__ = f.__name__
    return decorator


def add_user_to_session(username):
    query_db("UPDATE users SET last_login_date = DATETIME('now', 'localtime') WHERE username = ?",
             username, commit=True)
    row = query_db_object("""
        SELECT u.user_id, u.username, r.name AS role_name, u.creation_date, u.last_login_date, u.sex
        FROM users u  
        INNER JOIN roles r USING(role_id)
        WHERE username = ? 
    """, username, one=True)

    session.permanent = True
    session['user'] = row


def get_user_id():
    user = session.get('user')
    return user['user_id'] if user else None


def get_user_name():
    user = session.get('user')
    return user['username'] if user else None
