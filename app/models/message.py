from . import get_db_connection
import sqlite3

class Message:
    @staticmethod
    def create(book_id, sender_id, content, receiver_id=None):
        """
        建立新的留言或私訊。
        
        Args:
            book_id (int): 關聯的書籍 ID
            sender_id (int): 發送者 ID
            content (str): 訊息內容
            receiver_id (int, optional): 接收者 ID (若無則視為公開留言)
            
        Returns:
            int or None: 成功回傳新訊息 ID，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (book_id, sender_id, receiver_id, content) VALUES (?, ?, ?, ?)',
                (book_id, sender_id, receiver_id, content)
            )
            conn.commit()
            msg_id = cursor.lastrowid
            return msg_id
        except sqlite3.Error as e:
            print(f"Database error in Message.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有訊息 (管理用途)。
        
        Returns:
            list: 訊息資料字典的列表
        """
        try:
            conn = get_db_connection()
            messages = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
            return [dict(msg) for msg in messages]
        except sqlite3.Error as e:
            print(f"Database error in Message.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(msg_id):
        """
        透過 ID 取得特定訊息。
        
        Args:
            msg_id (int): 訊息 ID
            
        Returns:
            dict or None: 訊息資料字典，若不存在則回傳 None
        """
        try:
            conn = get_db_connection()
            msg = conn.execute('SELECT * FROM messages WHERE id = ?', (msg_id,)).fetchone()
            return dict(msg) if msg else None
        except sqlite3.Error as e:
            print(f"Database error in Message.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_book(book_id):
        """
        取得書籍下的公開留言 (receiver_id is NULL)。
        
        Args:
            book_id (int): 書籍 ID
            
        Returns:
            list: 留言字典列表
        """
        try:
            conn = get_db_connection()
            messages = conn.execute(
                'SELECT * FROM messages WHERE book_id = ? AND receiver_id IS NULL ORDER BY created_at ASC', 
                (book_id,)
            ).fetchall()
            return [dict(msg) for msg in messages]
        except sqlite3.Error as e:
            print(f"Database error in Message.get_by_book: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_private_messages(user1_id, user2_id, book_id=None):
        """
        取得兩個使用者之間的私訊紀錄。
        
        Args:
            user1_id (int): 第一個使用者 ID
            user2_id (int): 第二個使用者 ID
            book_id (int, optional): 可選的書籍過濾
            
        Returns:
            list: 私訊字典列表
        """
        try:
            conn = get_db_connection()
            query = '''
                SELECT * FROM messages 
                WHERE ((sender_id = ? AND receiver_id = ?) 
                   OR (sender_id = ? AND receiver_id = ?))
            '''
            params = [user1_id, user2_id, user2_id, user1_id]
            
            if book_id:
                query += ' AND book_id = ?'
                params.append(book_id)
                
            query += ' ORDER BY created_at ASC'
            
            messages = conn.execute(query, tuple(params)).fetchall()
            return [dict(msg) for msg in messages]
        except sqlite3.Error as e:
            print(f"Database error in Message.get_private_messages: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(msg_id, content=None):
        """
        更新訊息 (實務上訊息可能不允許修改，但為符合介面)。
        """
        try:
            if not content:
                return True
            conn = get_db_connection()
            conn.execute('UPDATE messages SET content = ? WHERE id = ?', (content, msg_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Message.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(msg_id):
        """
        刪除特定訊息。
        
        Args:
            msg_id (int): 訊息 ID
            
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM messages WHERE id = ?', (msg_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Message.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
