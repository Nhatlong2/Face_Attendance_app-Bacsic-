import cv2
import sys
from datetime import datetime

# import service và models
from services.db_service import DatabaseService
from services.attendance_service import AttendanceService
from models.detector import FaceDetector
from models.recognizer import FaceRecognizer
from models.liveness import LivenessDetector
from services.user_service import UserService
from utils.config import *
from tkinter import messagebox

db = DatabaseService()

def main(name=None):
    # kết nối DB
    attendance = AttendanceService(db, CSV_PATH)
    users = UserService(db)
    if not name:
        messagebox.showerror("Lỗi", "Tên không hợp lệ.")
        return
    user_id = users.add_user_returning_id(name)
    # load models
    detector = FaceDetector()
    recognizer = FaceRecognizer(db)
    liveness = LivenessDetector(LANDMARK_PATH)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không mở được camera.")
        sys.exit(1)

    messagebox.showinfo("Thông báo", f"Nhấn 'q' để thoát.")
    session_id = datetime.now().strftime("%Y%m%d%H%M")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # detect faces
        faces = detector.detect_faces(frame)

        # liveness check
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        is_live = liveness.is_blinking(gray)

        # nhận diện
        results = recognizer.recognize(frame, faces)

        for (x, y, w, h), (uid, name) in zip(faces, results):
            color = (0, 255, 0) if is_live else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, str(name), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # nếu nhận diện thành công và liveness OK thì log attendance
            if uid is not None and is_live:
                attendance.log_attendance(uid, name, session_id)

        # hiển thị
        cv2.imshow("Face Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
