from app.db import query_db, query_db_object


def get_food_categories_list():
    return query_db_object("SELECT id, name FROM food_categories")
