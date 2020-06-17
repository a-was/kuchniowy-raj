from app.db import query_db, query_db_object


def get_types_of_food_list():
    return query_db_object("SELECT type_of_food_id, name FROM types_of_food ORDER BY name")
