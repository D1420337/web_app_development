import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    建立並回傳一個 SQLite 資料庫連線。
    設定 sqlite3.Row 使查詢結果支援鍵值存取。
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

class Recipe:
    """處理食譜相關的資料庫操作模型"""
    
    @staticmethod
    def create(user_id, title, description, ingredients, steps, image_url=None):
        """
        新增一筆食譜記錄到資料庫。
        
        Args:
            user_id (int): 建立該食譜的作者 ID (對應 users table)
            title (str): 食譜名稱
            description (str): 食譜簡介
            ingredients (str): 所需食材
            steps (str): 料理步驟
            image_url (str, optional): 預定圖片網址
            
        Returns:
            int: 成功時回傳建立的食譜 ID，失敗則回傳 None
        """
        try:
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
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating recipe: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得資料庫內所有的食譜，依建立時間降序排列 (最新的在前)。
        
        Returns:
            list[dict]: 包含所有食譜字典的串列，出錯時回傳空串列。
        """
        try:
            conn = get_db_connection()
            recipes = conn.execute("SELECT * FROM recipes ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in recipes]
        except sqlite3.Error as e:
            print(f"Error fetching all recipes: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        """
        依據食譜 ID 取得單一食譜的詳細資料。
        
        Args:
            recipe_id (int): 欲查詢的食譜 ID
            
        Returns:
            dict: 成功時回傳該食譜字典，找不到或出錯時回傳 None。
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
            return dict(recipe) if recipe else None
        except sqlite3.Error as e:
            print(f"Error getting recipe by ID {recipe_id}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(recipe_id, title, description, ingredients, steps, image_url=None):
        """
        更新單指定 ID 的食譜資料。會連帶更新 updated_at 戳記。
        
        Args:
            recipe_id (int): 欲更新的食譜 ID
            title (str): 新名稱
            description (str): 新簡述
            ingredients (str): 新食材
            steps (str): 新步驟
            image_url (str, optional): 新圖片網址
            
        Returns:
            bool: 執行是否成功
        """
        try:
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
            return True
        except sqlite3.Error as e:
            print(f"Error updating recipe {recipe_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(recipe_id):
        """
        刪除特定 ID 的食譜記錄。
        
        Args:
            recipe_id (int): 欲刪除的食譜 ID
            
        Returns:
            bool: 執行是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting recipe {recipe_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def search(query):
        """
        關鍵字搜尋食譜，配對目標為「食譜名稱」或「食材內容」。
        
        Args:
            query (str): 搜尋關鍵字
            
        Returns:
            list[dict]: 符合條件的食譜字典串列，依據建立時間降序。
        """
        try:
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
            return [dict(r) for r in recipes]
        except sqlite3.Error as e:
            print(f"Error searching recipes with query '{query}': {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
