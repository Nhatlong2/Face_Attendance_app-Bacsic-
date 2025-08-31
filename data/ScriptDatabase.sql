CREATE DATABASE FaceAttendanceDB
ON PRIMARY (
    NAME = FaceAttendanceDB_Data,
    FILENAME = 'D:\face_attendance_app\data\FaceAttendanceDB.mdf',
    SIZE = 10MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
)
LOG ON (
    NAME = FaceAttendanceDB_Log,
    FILENAME = 'D:\face_attendance_app\data\FaceAttendanceDB.ldf',
    SIZE = 5MB,
    MAXSIZE = 50MB,
    FILEGROWTH = 5MB
);
GO
USE FaceAttendanceDB;
GO
-- Bảng lưu thông tin người dùng
CREATE TABLE Users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- Bảng lưu embedding khuôn mặt
CREATE TABLE Faces (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    embedding VARBINARY(MAX), -- lưu vector đã serialize (pickle/np.array)
    image_path NVARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Bảng điểm danh
CREATE TABLE Attendance (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT GETDATE(),
    session_id NVARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);