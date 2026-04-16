import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class User:
    @staticmethod
    def create(username, password_hash, role='user'):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Username already exists
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        users = conn.execute("SELECT * FROM users").fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def update(user_id, role=None, password_hash=None):
        conn = get_db_connection()
        if role and password_hash:
            conn.execute("UPDATE users SET role = ?, password_hash = ? WHERE id = ?", (role, password_hash, user_id))
        elif role:
            conn.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
        elif password_hash:
            conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
