# Face Attendance System

Ứng dụng điểm danh bằng khuôn mặt với Tkinter, OpenCV, Dlib, và Face Recognition.
Yêu cầu

Python 3.8+

SQL Server với DB FaceAttendanceDB đã khởi tạo (Users, Faces, Attendance)

Camera

Chức năng

Thêm người dùng mới (qua camera)

Nhận diện và điểm danh

Kiểm tra liveness (chớp mắt)

Xuất dữ liệu điểm danh (CSV + DB)

Ghi chú

Cấu hình DB trong utils/config.py

Landmark model shape_predictor_68_face_landmarks.dat cần tải từ dlib model zoo
## Cấu trúc thư mục
face_attendance_app/
├── main.py # Điểm vào chính
├── ui/ # Giao diện người dùng (Tkinter)
│ └── main_gui.py
├── scripts/ # Các script chạy độc lập (nhandien.py, chupanh.py)
├── models/ # Detector, Recognizer, Liveness
├── services/ # Database, User, Attendance
├── utils/ # Config
├── data/ # Dữ liệu (faces/, attendance.csv)
└── README.md


## Cài đặt
git clone https://github.com/Nhatlong2/Face_Attendance_app-Bacsic-.git
cd Face_Attendance_app-Bacsic-
pip install -r requirements.txt