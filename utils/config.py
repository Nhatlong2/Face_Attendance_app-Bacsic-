# utils/config.py

DB_CONFIG = {
    "server": "DESKTOP-09UU83A",              # hoặc tên instance, ví dụ "localhost\\SQLEXPRESS"
    "database": "FaceAttendanceDB",     # tên database bạn đã tạo
    "auth": "windows",                  # "windows" nếu dùng Windows Authentication, "sql" nếu dùng SQL Authentication
    "username": None,                   # điền khi auth="sql"
    "password": None                    # điền khi auth="sql"
}

CSV_PATH = "data/attendance.csv"
FACES_DIR = "data/faces/"
LANDMARK_PATH = "shape_predictor_68_face_landmarks.dat"
