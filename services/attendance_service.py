import csv
from datetime import datetime
from services.db_service import DatabaseService
from utils.config import CSV_PATH
class AttendanceService:
    def __init__(self, db: DatabaseService, csv_path=CSV_PATH):
        self.db = db
        self.csv_path = csv_path
        self._seen = set()
    def log_attendance(self, user_id, name, session_id):
        key = (user_id, session_id)
        if key in self._seen:
            return
        self._seen.add(key)
        timestamp = datetime.now()

        # Lưu vào DB
        query = "INSERT INTO Attendance (user_id, timestamp, session_id) VALUES (?, ?, ?)"
        self.db.execute(query, [user_id, timestamp, session_id])

        # Lưu vào CSV
        with open(self.csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([user_id, name, timestamp, session_id])
