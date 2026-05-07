from . import get_db_connection

class Book:
    @staticmethod
    def create(title, author, condition, price, seller_id, course_name=None, department=None, isbn=None):
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
        conn.close()
        return book_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(book) for book in books]

    @staticmethod
    def get_by_id(book_id):
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        conn.close()
        return dict(book) if book else None

    @staticmethod
    def search(keyword):
        conn = get_db_connection()
        query = f"%{keyword}%"
        books = conn.execute(
            'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR department LIKE ?',
            (query, query, query)
        ).fetchall()
        conn.close()
        return [dict(book) for book in books]

    @staticmethod
    def update_status(book_id, status):
        conn = get_db_connection()
        conn.execute('UPDATE books SET status = ? WHERE id = ?', (status, book_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(book_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
