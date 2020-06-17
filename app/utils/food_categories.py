from app.db import query_db, query_db_object


def get_food_categories_list():
    return query_db_object("SELECT food_category_id, name FROM food_categories ORDER BY name")
