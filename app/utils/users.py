import re

from werkzeug.security import generate_password_hash, check_password_hash

from app.config import Config
from app.db import query_db


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


def new_user(username, password, sex, cooking_level):
    query_db("""
        INSERT INTO users (username, password, sex, role_id, cooking_level_id) 
        VALUES (?, ?, ?,
            (SELECT role_id FROM roles WHERE name LIKE 'User'), 
            (SELECT cooking_level_id FROM cooking_levels WHERE name = ? )
        )
    """, username, generate_password_hash(password), sex, cooking_level, commit=True)


def change_password(username, password):
    query_db("UPDATE users SET password = ? WHERE username = ?",
             generate_password_hash(password), username, commit=True)
