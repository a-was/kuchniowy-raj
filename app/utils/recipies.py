from app.db import query_db, query_db_object


def get_recipes_list(checked=None):
    sql = """
        SELECT r.recipe_id, 
            r.user_id, u.username, 
            r.type_of_food_id, tf.name AS type_of_food, 
            r.food_category_id, fc.name AS food_category, 
            r.name, r.creation_date, r.description, r.rating, r.checked, r.time_required, r.views
        FROM recipes r
        INNER JOIN users u USING(user_id)
        INNER JOIN types_of_food tf USING(type_of_food_id)
        INNER JOIN food_categories fc USING(food_category_id)
    """
    if checked is None:
        return query_db_object(sql)
    elif checked is True:
        return query_db_object(sql + " WHERE checked = 1")
    else:
        return query_db_object(sql + " WHERE checked = 0")


def recipe_exists(name):
    res = query_db("SELECT COUNT(*) FROM recipes WHERE name = ?", name, one=True)
    return True if res[0] > 0 else False


def new_recipe(user_id, name, type_of_food, food_category, description, time):
    query_db("""
        INSERT INTO recipes (user_id, type_of_food_id, food_category_id, name, description, time_required)
        VALUES (?, ?, ?, ?, ?, ?)
    """, user_id, type_of_food, food_category, name, description, time, commit=True)
