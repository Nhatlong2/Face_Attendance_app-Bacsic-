import cv2
import os
import sys
import face_recognition
import numpy as np
from datetime import datetime

from services.db_service import DatabaseService
from services.user_service import UserService


db = DatabaseService()


# nơi lưu ảnh
FACES_DIR = "data/faces/"

def main():
    # kết nối DB
    users = UserService(db)

    # hỏi tên người dùng mới
    name = input("Nhập tên người dùng mới: ").strip()
    if not name:
        print("Tên không hợp lệ.")
        sys.exit(1)
    user_id = users.add_user_returning_id(name)

    # mở camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không mở được camera.")
        sys.exit(1)

    print("Nhấn 'c' để chụp ảnh, 'q' để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Đăng ký khuôn mặt", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            # lưu ảnh vào thư mục faces
            filename = f"{user_id}_{name}.jpg"
            save_path = os.path.join(FACES_DIR, filename)
            cv2.imwrite(save_path, frame)
            print(f"Đã lưu ảnh: {save_path}")

            # tạo embedding
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, boxes)

            if len(encodings) > 0:
                embedding = encodings[0]
                # lưu vào DB (bảng Faces)
                db.execute(
                    "INSERT INTO Faces (user_id, embedding, image_path) VALUES (?, ?, ?)",
                    [user_id, embedding.tobytes(), save_path]
                )
                print(f"Đã thêm embedding cho user_id={user_id}")
            else:
                print("Không tìm thấy khuôn mặt, thử lại.")

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    db.close()

if __name__ == "__main__":
    main()
