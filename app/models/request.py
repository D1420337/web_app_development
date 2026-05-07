from . import get_db_connection
import sqlite3

class Request:
    @staticmethod
    def create(book_id, buyer_id):
        """
        建立新的預約請求。
        
        Args:
            book_id (int): 書籍 ID
            buyer_id (int): 買家 ID
            
        Returns:
            int or None: 成功回傳新請求 ID，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO requests (book_id, buyer_id) VALUES (?, ?)',
                (book_id, buyer_id)
            )
            conn.commit()
            req_id = cursor.lastrowid
            return req_id
        except sqlite3.Error as e:
            print(f"Database error in Request.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有請求 (一般不建議使用，但為符合介面保留)。
        
        Returns:
            list: 請求資料字典的列表
        """
        try:
            conn = get_db_connection()
            requests = conn.execute('SELECT * FROM requests ORDER BY created_at DESC').fetchall()
            return [dict(req) for req in requests]
        except sqlite3.Error as e:
            print(f"Database error in Request.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(req_id):
        """
        透過 ID 取得特定預約請求。
        
        Args:
            req_id (int): 請求 ID
            
        Returns:
            dict or None: 請求資料字典，若不存在則回傳 None
        """
        try:
            conn = get_db_connection()
            req = conn.execute('SELECT * FROM requests WHERE id = ?', (req_id,)).fetchone()
            return dict(req) if req else None
        except sqlite3.Error as e:
            print(f"Database error in Request.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_buyer(buyer_id):
        """
        取得買家發出的所有預約請求。
        
        Args:
            buyer_id (int): 買家 ID
            
        Returns:
            list: 請求資料字典列表
        """
        try:
            conn = get_db_connection()
            requests = conn.execute('SELECT * FROM requests WHERE buyer_id = ? ORDER BY created_at DESC', (buyer_id,)).fetchall()
            return [dict(req) for req in requests]
        except sqlite3.Error as e:
            print(f"Database error in Request.get_by_buyer: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_book(book_id):
        """
        取得針對特定書籍的所有預約請求。
        
        Args:
            book_id (int): 書籍 ID
            
        Returns:
            list: 請求資料字典列表
        """
        try:
            conn = get_db_connection()
            requests = conn.execute('SELECT * FROM requests WHERE book_id = ? ORDER BY created_at DESC', (book_id,)).fetchall()
            return [dict(req) for req in requests]
        except sqlite3.Error as e:
            print(f"Database error in Request.get_by_book: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(req_id, status=None):
        """
        更新請求狀態 (一般呼叫 update_status 即可，此函式為符合基本 CRUD 介面)。
        """
        if status:
            return Request.update_status(req_id, status)
        return True

    @staticmethod
    def update_status(req_id, status):
        """
        更新預約請求狀態。
        
        Args:
            req_id (int): 請求 ID
            status (str): 新的狀態 (pending, accepted, rejected)
            
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('UPDATE requests SET status = ? WHERE id = ?', (status, req_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Request.update_status: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(req_id):
        """
        刪除預約請求。
        
        Args:
            req_id (int): 請求 ID
            
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM requests WHERE id = ?', (req_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Request.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
