import sqlite3

from flask import g

from .config import Config

_DB_PROPERTY = '_database'


def get_db():
    db = getattr(g, _DB_PROPERTY, None)
    if db is None:
        db = sqlite3.connect(Config.DB_FILE)
        setattr(g, _DB_PROPERTY, db)
    return db


def close_db(exception):
    db = getattr(g, _DB_PROPERTY, None)
    if db is not None:
        db.close()


def init_app(application):
    application.teardown_appcontext(close_db)


def query_db(query, *args, one=False, commit=False):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    res = cursor.fetchall()
    if commit:
        db.commit()

    if res and one:
        return res[0]
    else:
        return res
