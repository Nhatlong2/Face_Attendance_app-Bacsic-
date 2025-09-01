from services.db_service import DatabaseService
from utils.config import FACES_DIR
import os
import shutil
class UserService:
    def __init__(self, db: DatabaseService):
        self.db = db

    def add_user_returning_id(self, name):
        row = self.db.fetchall(
            "INSERT INTO Users (name) OUTPUT INSERTED.id VALUES (?)",
            [name]
        )[0]
        return int(row[0])

    def list_users(self):
        query = "SELECT id, name, created_at FROM Users"
        return self.db.fetchall(query)

    def delete_user(self, name):
        """Xóa người dùng khỏi DB (Attendance + Faces + Users) và thư mục faces"""
        try:
            # kiểm tra user có tồn tại không
            rows = self.db.fetchall("SELECT id FROM Users WHERE name = ?", [name])
            if not rows:
                return False, f"Người dùng '{name}' không tồn tại"

            user_id = rows[0][0]

            # 1. Xóa bản ghi trong Attendance (tránh lỗi FK)
            self.db.execute("DELETE FROM Attendance WHERE user_id = ?", [user_id])

            # 2. Xóa bản ghi trong Faces
            self.db.execute("DELETE FROM Faces WHERE user_id = ?", [user_id])

            # 3. Xóa user trong Users
            self.db.execute("DELETE FROM Users WHERE id = ?", [user_id])

            # 4. Xóa ảnh trong thư mục faces
            deleted_files = 0
            for filename in os.listdir(FACES_DIR):
                if filename.startswith(f"{user_id}_"):
                    filepath = os.path.join(FACES_DIR, filename)
                    try:
                        os.remove(filepath)
                        deleted_files += 1
                    except Exception as e:
                        return False, f"Không thể xóa file {filename}: {e}"

            return True, f"Đã xóa người dùng '{name}' thành công. {deleted_files} ảnh đã bị xóa."

        except Exception as e:
            return False, f"Lỗi khi xóa người dùng: {str(e)}"

    def get_user_name_by_id(self, user_id):
        row = self.db.fetchall("SELECT name FROM Users WHERE id = ?", [user_id])
        if row:
            return str(row[0]) 
        return None
