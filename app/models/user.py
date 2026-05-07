from . import get_db_connection
import sqlite3

class User:
    @staticmethod
    def create(username, email, password_hash, role='student'):
        """
        建立新的使用者。
        
        Args:
            username (str): 使用者名稱
            email (str): 電子郵件
            password_hash (str): 加密後的密碼
            role (str): 使用者角色，預設為 'student'
            
        Returns:
            int or None: 成功回傳新使用者的 ID，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                (username, email, password_hash, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.Error as e:
            print(f"Database error in User.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有使用者。
        
        Returns:
            list: 使用者資料字典的列表
        """
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            return [dict(u) for u in users]
        except sqlite3.Error as e:
            print(f"Database error in User.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        透過 ID 取得使用者。
        
        Args:
            user_id (int): 使用者 ID
            
        Returns:
            dict or None: 使用者資料字典，若不存在則回傳 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_email(email):
        """
        透過 Email 取得使用者。
        
        Args:
            email (str): 電子郵件
            
        Returns:
            dict or None: 使用者資料字典，若不存在則回傳 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_email: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(user_id, username=None, password_hash=None):
        """
        更新使用者資料。
        
        Args:
            user_id (int): 使用者 ID
            username (str, optional): 新的使用者名稱
            password_hash (str, optional): 新的密碼雜湊
            
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            if username:
                conn.execute('UPDATE users SET username = ? WHERE id = ?', (username, user_id))
            if password_hash:
                conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in User.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(user_id):
        """
        刪除使用者。
        
        Args:
            user_id (int): 使用者 ID
            
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in User.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
