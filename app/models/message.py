from . import get_db_connection

class Message:
    @staticmethod
    def create(book_id, sender_id, content, receiver_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO messages (book_id, sender_id, receiver_id, content) VALUES (?, ?, ?, ?)',
            (book_id, sender_id, receiver_id, content)
        )
        conn.commit()
        msg_id = cursor.lastrowid
        conn.close()
        return msg_id

    @staticmethod
    def get_by_id(msg_id):
        conn = get_db_connection()
        msg = conn.execute('SELECT * FROM messages WHERE id = ?', (msg_id,)).fetchone()
        conn.close()
        return dict(msg) if msg else None

    @staticmethod
    def get_by_book(book_id):
        conn = get_db_connection()
        messages = conn.execute('SELECT * FROM messages WHERE book_id = ? ORDER BY created_at ASC', (book_id,)).fetchall()
        conn.close()
        return [dict(msg) for msg in messages]

    @staticmethod
    def get_private_messages(user1_id, user2_id, book_id=None):
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
        conn.close()
        return [dict(msg) for msg in messages]

    @staticmethod
    def delete(msg_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM messages WHERE id = ?', (msg_id,))
        conn.commit()
        conn.close()
