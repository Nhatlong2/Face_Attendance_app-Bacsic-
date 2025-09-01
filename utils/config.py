# utils/config.py
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_CONFIG = {
    "server": "DESKTOP-09UU83A",              # hoặc tên instance, ví dụ "localhost\\SQLEXPRESS"
    "database": "FaceAttendanceDB",     # tên database bạn đã tạo
    "auth": "windows",                  # "windows" nếu dùng Windows Authentication, "sql" nếu dùng SQL Authentication
    "username": None,                   # điền khi auth="sql"
    "password": None                    # điền khi auth="sql"
}

CSV_PATH = str(PROJECT_ROOT / "data" / "attendance.csv")
FACES_DIR = str(PROJECT_ROOT / "data" / "faces")   # sửa lại thành path tuyệt đối
LANDMARK_PATH = str(PROJECT_ROOT / "shape_predictor_68_face_landmarks.dat")
