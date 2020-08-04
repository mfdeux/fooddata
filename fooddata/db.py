import csv
import sqlite3
from contextlib import closing


def load_all():
    load_categories()
    load_nutrients()
    load_food()


def load_categories(db_path: str, save_path: str):
    with open(f"{save_path}/food_category.csv") as fh:
        reader = csv.DictReader(fh)

        with closing(sqlite3.connect(db_path)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS food_categories (id TEXT PRIMARY KEY, code TEXT, description TEXT);")
                cursor.executemany('INSERT INTO food_categories VALUES(?,?,?) ON CONFLICT DO NOTHING;',
                                   [(record['id'], record['code'], record['description']) for record in reader])
                connection.commit()


def load_nutrients(db_path: str, save_path: str):
    with open(f"{save_path}/nutrient.csv") as mfh:
        reader = csv.DictReader(mfh)

        with closing(sqlite3.connect(db_path)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS nutrients (id TEXT PRIMARY KEY, name TEXT, unit TEXT);")
                cursor.executemany('INSERT INTO nutrients VALUES(?,?,?) ON CONFLICT DO NOTHING;',
                                   [(record['id'], record['name'], record['unit_name']) for record in reader])
                connection.commit()

    with open(f"{save_path}/food_nutrient.csv") as nfh:
        reader = csv.DictReader(nfh)

        with closing(sqlite3.connect(db_path)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS food_nutrients (id TEXT PRIMARY KEY, food_id TEXT, nutrient_id TEXT, amount REAL, FOREIGN KEY(food_id) REFERENCES foods(id), FOREIGN KEY(nutrient_id) REFERENCES nutrients(id));")
                cursor.executemany('INSERT INTO food_nutrients VALUES(?,?,?,?) ON CONFLICT DO NOTHING;',
                                   [(record['id'], record['fdc_id'], record['nutrient_id'], float(record['amount'])) for
                                    record in reader])
                connection.commit()


def load_food(db_path: str, save_path: str):
    with open(f"{save_path}/food.csv") as fh:
        reader = csv.DictReader(fh)

        with closing(sqlite3.connect(db_path)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS foods (id TEXT PRIMARY KEY, type TEXT, description TEXT, category_id TEXT, FOREIGN KEY(category_id) REFERENCES food_categories(id));")

                cursor.executemany('INSERT INTO foods VALUES(?,?,?,?) ON CONFLICT DO NOTHING;',
                                   [(record['fdc_id'], record['data_type'], record['description'],
                                     record['food_category_id'] if record['food_category_id'] else None) for record in
                                    reader])
                connection.commit()


def run_query(db_path: str, query: str):
    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row

        with closing(connection.cursor()) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows


def create_views(db_path: str):
    with closing(sqlite3.connect(db_path)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "CREATE VIEW IF NOT EXISTS foods_v AS SELECT foods.id, foods.type, foods.description, food_categories.description as category from foods LEFT JOIN food_categories on foods.category_id = food_categories.id;")
            cursor.execute(
                "CREATE VIEW IF NOT EXISTS food_nutrients_v AS SELECT food_nutrients.id,  food_nutrients.food_id, food_nutrients.nutrient_id, foods.type as food_type, foods.description as food, nutrients.name as nutrient, lower(nutrients.unit) as nutrient_unit , food_categories.description as food_category from food_nutrients LEFT JOIN nutrients ON nutrients.id = food_nutrients.nutrient_id LEFT JOIN foods ON foods.id = food_nutrients.food_id LEFT JOIN food_categories on foods.category_id = food_categories.id;")