import sqlite3

from flask import g, current_app


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DB_FILE'])
    return db


def close_db(exception):
    db = getattr(g, '_database', None)
    if db:
        db.close()


def init_app(application):
    application.teardown_appcontext(close_db)
