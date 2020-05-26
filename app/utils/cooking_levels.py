from app.db import query_db, query_db_object


def get_cooking_levels():
    return query_db_object("SELECT id, name, description FROM cooking_levels")
