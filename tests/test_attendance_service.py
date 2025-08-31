from services.db_service import DatabaseService
from services.user_service import UserService
from services.attendance_service import AttendanceService

def test_log_attendance(tmp_path):
    db = DatabaseService()
    users = UserService(db)

    # Thêm user tạm cho test
    users.add_user_returning_id("TestUser")
    user_id = users.list_users()[-1][0]  # lấy id vừa thêm

    csv_path = tmp_path / "attendance.csv"
    service = AttendanceService(db, str(csv_path))
    service.log_attendance(user_id, "TestUser", "session123")

    # Kiểm tra CSV
    assert csv_path.exists()
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert "TestUser" in lines[-1]

    # Dọn dẹp DB: xóa user và attendance vừa thêm
    db.execute("DELETE FROM Attendance WHERE user_id = ?", [user_id])
    users.delete_user(user_id)

    db.close()
