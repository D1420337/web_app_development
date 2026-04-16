import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Recipe:
    @staticmethod
    def create(user_id, title, description, ingredients, steps, image_url=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recipes (user_id, title, description, ingredients, steps, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, description, ingredients, steps, image_url)
        )
        conn.commit()
        recipe_id = cursor.lastrowid
        conn.close()
        return recipe_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        recipes = conn.execute("SELECT * FROM recipes ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def update(recipe_id, title, description, ingredients, steps, image_url=None):
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE recipes 
            SET title = ?, description = ?, ingredients = ?, steps = ?, image_url = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title, description, ingredients, steps, image_url, recipe_id)
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def search(query):
        conn = get_db_connection()
        search_query = f"%{query}%"
        recipes = conn.execute(
            """
            SELECT * FROM recipes 
            WHERE title LIKE ? OR ingredients LIKE ?
            ORDER BY created_at DESC
            """, 
            (search_query, search_query)
        ).fetchall()
        conn.close()
        return [dict(r) for r in recipes]
