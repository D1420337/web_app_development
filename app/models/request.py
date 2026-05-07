from . import get_db_connection

class Request:
    @staticmethod
    def create(book_id, buyer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO requests (book_id, buyer_id) VALUES (?, ?)',
            (book_id, buyer_id)
        )
        conn.commit()
        req_id = cursor.lastrowid
        conn.close()
        return req_id

    @staticmethod
    def get_by_id(req_id):
        conn = get_db_connection()
        req = conn.execute('SELECT * FROM requests WHERE id = ?', (req_id,)).fetchone()
        conn.close()
        return dict(req) if req else None

    @staticmethod
    def get_by_buyer(buyer_id):
        conn = get_db_connection()
        requests = conn.execute('SELECT * FROM requests WHERE buyer_id = ? ORDER BY created_at DESC', (buyer_id,)).fetchall()
        conn.close()
        return [dict(req) for req in requests]

    @staticmethod
    def get_by_book(book_id):
        conn = get_db_connection()
        requests = conn.execute('SELECT * FROM requests WHERE book_id = ? ORDER BY created_at DESC', (book_id,)).fetchall()
        conn.close()
        return [dict(req) for req in requests]

    @staticmethod
    def update_status(req_id, status):
        conn = get_db_connection()
        conn.execute('UPDATE requests SET status = ? WHERE id = ?', (status, req_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(req_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM requests WHERE id = ?', (req_id,))
        conn.commit()
        conn.close()
