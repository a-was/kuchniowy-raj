CREATE TABLE IF NOT EXISTS `cooking_levels` (
  `cooking_level_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT UNIQUE NOT NULL,
  `description` TEXT
);

CREATE TABLE IF NOT EXISTS `roles` (
  `role_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `username` TEXT UNIQUE NOT NULL,
  `creation_date` DATE NOT NULL DEFAULT (DATETIME('now', 'localtime')),
  `last_login_date` DATE CHECK ( last_login_date >= creation_date ),
  `role_id` INTEGER NOT NULL,
  `cooking_level_id` INTEGER,
  `sex` TEXT CHECK (sex IN ('F','M')),
  `password` TEXT NOT NULL,
  CONSTRAINT users_role_id_fk
      FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE RESTRICT,
  CONSTRAINT users_cooking_levels_id_fk
      FOREIGN KEY (cooking_level_id) REFERENCES cooking_levels (cooking_level_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `types_of_food` (
  `type_of_food_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS `food_categories` (
  `food_category_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS `ingredients` (
  `ingredient_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS `recipes` (
  `recipe_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_id` INTEGER,
  `type_of_food_id` INTEGER,
  `food_category_id` INTEGER,
  `name` TEXT UNIQUE NOT NULL,
  `creation_date` DATE NOT NULL DEFAULT (DATETIME('now', 'localtime')),
  `description` TEXT NOT NULL,
  `rating` INTEGER CHECK (rating BETWEEN 1 AND 10),
  `checked` BOOLEAN NOT NULL DEFAULT 0 CHECK(checked IN (0,1)),
  `time_required` INTEGER NOT NULL,
  `views` INTEGER DEFAULT 0 CHECK ( views >= 0 ),
  CONSTRAINT recipes_user_id_fk
      FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
  CONSTRAINT recipes_type_of_food_id_fk
      FOREIGN KEY (type_of_food_id) REFERENCES types_of_food (type_of_food_id) ON DELETE RESTRICT,
  CONSTRAINT recipes_food_category_id_fk
      FOREIGN KEY (food_category_id) REFERENCES food_categories (food_category_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `recipes_ingredients` (
  `recipe_id` INTEGER NOT NULL,
  `ingredient_id` INTEGER NOT NULL,
  `count` INTEGER NOT NULL,
  CONSTRAINT recipes_ingredients_recipe_id_fk
      FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE RESTRICT,
  CONSTRAINT recipes_ingredients_ingredient_id_fk
      FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id) ON DELETE RESTRICT
);
