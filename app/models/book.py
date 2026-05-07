from . import get_db_connection
import sqlite3

class Book:
    @staticmethod
    def create(title, author, condition, price, seller_id, course_name=None, department=None, isbn=None):
        """
        建立新的二手書上架紀錄。
        
        Args:
            title (str): 書名
            author (str): 作者
            condition (str): 書況
            price (int): 價格
            seller_id (int): 賣家 ID (User ID)
            course_name (str, optional): 課程名稱
            department (str, optional): 適用科系
            isbn (str, optional): ISBN
            
        Returns:
            int or None: 成功回傳新書本 ID，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO books 
                   (title, author, course_name, department, isbn, condition, price, seller_id) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (title, author, course_name, department, isbn, condition, price, seller_id)
            )
            conn.commit()
            book_id = cursor.lastrowid
            return book_id
        except sqlite3.Error as e:
            print(f"Database error in Book.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有上架的書籍。
        
        Returns:
            list: 書籍資料字典的列表
        """
        try:
            conn = get_db_connection()
            books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
            return [dict(book) for book in books]
        except sqlite3.Error as e:
            print(f"Database error in Book.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(book_id):
        """
        透過 ID 取得特定書籍。
        
        Args:
            book_id (int): 書籍 ID
            
        Returns:
            dict or None: 書籍資料字典，若不存在則回傳 None
        """
        try:
            conn = get_db_connection()
            book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
            return dict(book) if book else None
        except sqlite3.Error as e:
            print(f"Database error in Book.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def search(keyword):
        """
        根據關鍵字搜尋書籍。
        
        Args:
            keyword (str): 搜尋關鍵字
            
        Returns:
            list: 符合條件的書籍字典列表
        """
        try:
            conn = get_db_connection()
            query = f"%{keyword}%"
            books = conn.execute(
                'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR department LIKE ? ORDER BY created_at DESC',
                (query, query, query)
            ).fetchall()
            return [dict(book) for book in books]
        except sqlite3.Error as e:
            print(f"Database error in Book.search: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(book_id, title=None, author=None, condition=None, price=None, course_name=None, department=None, isbn=None):
        """
        更新書籍資料。
        """
        try:
            conn = get_db_connection()
            query = "UPDATE books SET "
            fields = []
            values = []
            
            if title is not None:
                fields.append("title = ?")
                values.append(title)
            if author is not None:
                fields.append("author = ?")
                values.append(author)
            if condition is not None:
                fields.append("condition = ?")
                values.append(condition)
            if price is not None:
                fields.append("price = ?")
                values.append(price)
            if course_name is not None:
                fields.append("course_name = ?")
                values.append(course_name)
            if department is not None:
                fields.append("department = ?")
                values.append(department)
            if isbn is not None:
                fields.append("isbn = ?")
                values.append(isbn)
                
            if not fields:
                return True
                
            query += ", ".join(fields) + " WHERE id = ?"
            values.append(book_id)
            
            conn.execute(query, tuple(values))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Book.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update_status(book_id, status):
        """
        更新書籍狀態。
        
        Args:
            book_id (int): 書籍 ID
            status (str): 新的狀態 (available, reserved, sold)
            
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('UPDATE books SET status = ? WHERE id = ?', (status, book_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Book.update_status: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(book_id):
        """
        刪除書籍。
        
        Args:
            book_id (int): 書籍 ID
            
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Book.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
