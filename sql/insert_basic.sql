INSERT INTO roles (name) VALUES ('Administrator');
INSERT INTO roles (name) VALUES ('User');

INSERT INTO users (username, sex, role_id, password)
VALUES ('admin', 'M',
        (SELECT role_id FROM roles WHERE name LIKE 'Administrator'),
        'pbkdf2:sha256:150000$oPK7AL9k$fc3009125734e47c89f9bb0a2ecc3aa11f614f1b0a40dca808fe125828318d94');

INSERT INTO cooking_levels (name) VALUES ('Amator');
INSERT INTO cooking_levels (name) VALUES ('Średnio zaawansowany');
INSERT INTO cooking_levels (name) VALUES ('Zaawansowany');
INSERT INTO cooking_levels (name) VALUES ('Mistrz kuchni');

INSERT INTO food_categories (name) VALUES ('Śniadanie');
INSERT INTO food_categories (name) VALUES ('Obiad');
INSERT INTO food_categories (name) VALUES ('Kolacja');
INSERT INTO food_categories (name) VALUES ('Przekąska');

INSERT INTO types_of_food (name) VALUES ('Ciasto');
INSERT INTO types_of_food (name) VALUES ('Zupa');
