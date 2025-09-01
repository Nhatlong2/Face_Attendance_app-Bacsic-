import cv2
import os
import sys
import face_recognition
import numpy as np
from datetime import datetime
from tkinter import messagebox, Tk
from services.db_service import DatabaseService
from services.user_service import UserService
from utils.config import FACES_DIR

db = DatabaseService()

def main(name=None):
    # kết nối DB
    users = UserService(db)

    # nếu chưa có tham số truyền vào thì lấy từ sys.argv
    if not name:
        if len(sys.argv) > 1:
            name = sys.argv[1].strip()
        else:
            messagebox.showerror("Lỗi", "Chưa nhập tên người dùng!")
            sys.exit(1)

    if not name:
        messagebox.showerror("Lỗi", "Tên không hợp lệ.")
        sys.exit(1)

    user_id = users.add_user_returning_id(name)

    # mở camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Lỗi", "Không mở được camera.")
        sys.exit(1)

    messagebox.showinfo("Thông báo", f"Nhấn 'c' để chụp ảnh cho {name}, 'q' để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Đăng ký khuôn mặt", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            # lưu ảnh
            filename = f"{user_id}_{name}.jpg"
            os.makedirs(FACES_DIR, exist_ok=True)
            save_path = os.path.join(FACES_DIR, filename)
            cv2.imwrite(save_path, frame)
            messagebox.showinfo("Thông báo", f"Đã lưu ảnh: {save_path}")

            # tạo embedding
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, boxes)

            if len(encodings) > 0:
                embedding = encodings[0]
                db.execute(
                    "INSERT INTO Faces (user_id, embedding, image_path) VALUES (?, ?, ?)",
                    [user_id, embedding.tobytes(), save_path]
                )
                messagebox.showinfo("Thông báo", f"Đã thêm embedding cho {name}")
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy khuôn mặt, thử lại.")

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()