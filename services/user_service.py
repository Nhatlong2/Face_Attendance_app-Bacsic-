from services.db_service import DatabaseService

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

    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE id = ?"
        self.db.execute(query, [user_id])
