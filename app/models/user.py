import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    建立並回傳一個 SQLite 資料庫連線。
    使用 sqlite3.Row 作為 row_factory，讓查詢結果支援透過欄位名稱取值 (例如 row['id'])。
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

class User:
    """處理使用者相關的資料庫操作模型"""
    
    @staticmethod
    def create(username, password_hash, role='user'):
        """
        新增一位使用者到資料庫。
        
        Args:
            username (str): 使用者的登入帳號
            password_hash (str): 已加密的密碼雜湊值
            role (str, optional): 權限角色，預設為 'user'
            
        Returns:
            int: 成功建立後的使用者 id，若帳號已存在或發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Username '{username}' already exists.")
            return None
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        依據使用者 ID 查詢單筆使用者資料。
        
        Args:
            user_id (int): 使用者 ID
            
        Returns:
            dict: 成功時回傳使用者字典資料，找不到或錯誤時回傳 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Error getting user by ID {user_id}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_username(username):
        """
        依據帳號查詢單筆使用者資料，主要用於登入驗證。
        
        Args:
            username (str): 使用者帳號
            
        Returns:
            dict: 成功時回傳使用者字典資料，找不到或錯誤時回傳 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Error getting user by username {username}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得系統內所有的使用者列表。
        
        Returns:
            list[dict]: 包含所有使用者定義的字典串列，若有錯誤則回傳空串列
        """
        try:
            conn = get_db_connection()
            users = conn.execute("SELECT * FROM users").fetchall()
            return [dict(u) for u in users]
        except sqlite3.Error as e:
            print(f"Error getting all users: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(user_id, role=None, password_hash=None):
        """
        更新使用者的密碼或角色權限。
        
        Args:
            user_id (int): 目標使用者 ID
            role (str, optional): 新的角色權限
            password_hash (str, optional): 新的密碼雜湊值
            
        Returns:
            bool: 是否更新成功
        """
        try:
            conn = get_db_connection()
            if role and password_hash:
                conn.execute("UPDATE users SET role = ?, password_hash = ? WHERE id = ?", (role, password_hash, user_id))
            elif role:
                conn.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
            elif password_hash:
                conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user {user_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(user_id):
        """
        依據 ID 刪除使用者。
        
        Args:
            user_id (int): 要刪除的使用者 ID
            
        Returns:
            bool: 執行是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user {user_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
