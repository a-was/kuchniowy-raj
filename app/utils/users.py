import re

from werkzeug.security import generate_password_hash, check_password_hash

from app.config import Config
from app.db import query_db, query_db_object


def validate_passwords(p1, p2):
    if p1 != p2 or not re.fullmatch(Config.PASSWORD_REGEX, p1):
        return False
    else:
        return True


def validate_username(username):
    return True if re.fullmatch(Config.USERNAME_REGEX, username) else False


def authenticate_user(username, password):
    user_row = query_db("SELECT password FROM users WHERE username = ?", username, one=True)
    return check_password_hash(user_row[0], password) if user_row else False


def exists(username):
    res = query_db("SELECT COUNT(*) FROM users WHERE username = ?", username, one=True)
    return True if res[0] > 0 else False


def set_admin(user_id):
    query_db("UPDATE users SET role_id = (SELECT role_id FROM roles WHERE name = 'Administrator') WHERE user_id = ?",
             user_id, commit=True)


def set_user(user_id):
    query_db("UPDATE users SET role_id = (SELECT role_id FROM roles WHERE name = 'User') WHERE user_id = ?",
             user_id, commit=True)


def new_user(username, password, sex, cooking_level):
    query_db("""
        INSERT INTO users (username, password, sex, role_id, cooking_level_id) 
        VALUES (?, ?, ?, ?,
            (SELECT role_id FROM roles WHERE name LIKE 'User') 
        )
    """, username, generate_password_hash(password), sex, cooking_level, commit=True)


def change_password(username, password):
    query_db("UPDATE users SET password = ? WHERE username = ?",
             generate_password_hash(password), username, commit=True)


def get_all_users():
    return query_db_object("""
        SELECT u.user_id, u.username, u.creation_date, u.last_login_date, 
            u.role_id, r.name AS role,
            u.cooking_level_id, cl.name AS cooking_level,
            u.sex
        FROM users u
        INNER JOIN roles r USING (role_id)
        LEFT JOIN cooking_levels cl USING (cooking_level_id) 
    """)


def delete_user(user_id):
    query_db("DELETE FROM users WHERE user_id = ?", user_id, commit=True)
