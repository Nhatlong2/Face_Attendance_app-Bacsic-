# ui/main_gui.py
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog,ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess, os, sys
from pathlib import Path
from scripts.chupanh import main as chupanh_main
from scripts.nhandien import main as nhandien_main
from services.user_service import UserService
from services.db_service import DatabaseService
import cv2, face_recognition, os
from utils.config import *
import shutil
import threading

ASSETS_PATH = Path(__file__).with_name("assets")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

def run_py(*args):
    try:
        cmd = [sys.executable] + [str(a) for a in args]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            messagebox.showinfo("Thông báo", result.stdout.strip())
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {args}\n{e.stderr}")

def mo_diem_danh():
    nhandien_main("Unknown")

def mo_them_nguoi():
    top = tk.Toplevel(root)
    top.title("Thêm người mới")
    top.geometry("300x150")

    tk.Label(top, text="Nhập tên:", font=("Arial", 12)).pack(pady=10)
    entry = tk.Entry(top, font=("Arial", 12))
    entry.pack(pady=5)

    def submit():
        name = entry.get().strip()
        if not name:
            messagebox.showerror("Lỗi", "Tên không được để trống")
            return
        threading.Thread(target=chupanh_main, args=(name,), daemon=True).start()
        top.destroy()

    tk.Button(top, text="Xác nhận", command=submit).pack(pady=10)
def mo_them_nguoi_file():
    top = tk.Toplevel(root)
    top.title("Thêm người mới từ ảnh")
    top.geometry("300x150")

    tk.Label(top, text="Nhập tên:", font=("Arial", 12)).pack(pady=10)
    entry = tk.Entry(top, font=("Arial", 12))
    entry.pack(pady=5)

    def submit():
        name = entry.get().strip()
        if not name:
            messagebox.showerror("Lỗi", "Tên không được để trống")
            return

        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not filepath:
            return

        # kết nối DB
        db = DatabaseService()
        users = UserService(db)
        user_id = users.add_user_returning_id(name)

        # tạo thư mục faces nếu chưa tồn tại
        os.makedirs(FACES_DIR, exist_ok=True)

        # copy ảnh vào thư mục
        filename = f"{user_id}_{name}.jpg"
        save_path = os.path.join(FACES_DIR, filename)
        shutil.copy(filepath, save_path)

        messagebox.showinfo("Thành công", f"Đã thêm {name} và lưu ảnh thành công!")

        top.destroy()
    tk.Button(top, text="Chọn ảnh và lưu", command=submit).pack(pady=10)

def xoa_nguoi_dung():
    name = simpledialog.askstring("Xóa người dùng", "Nhập tên người cần xóa:")
    if not name:
        return

    db = DatabaseService()
    users = UserService(db)
    success, msg = users.delete_user(name)

    if success:
        messagebox.showinfo("Thành công", msg)
    else:
        messagebox.showerror("Lỗi", msg)

def reset_system():
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa toàn bộ dữ liệu không?")
    if not confirm:
          return
    try:
         db = DatabaseService()
         db.execute("DELETE FROM Attendance")
         db.execute("DBCC CHECKIDENT ('dbo.Attendance', RESEED, 0)")
         db.execute("DELETE FROM Faces")
         db.execute("DBCC CHECKIDENT ('dbo.Faces', RESEED, 0)")
         db.execute("DELETE FROM Users")
         db.execute("DBCC CHECKIDENT ('dbo.Users', RESEED, 0)")
         db.close()

         # Xóa toàn bộ ảnh trong faces/
         for filename in os.listdir(FACES_DIR):
             file_path = os.path.join(FACES_DIR, filename)
             try:
                 os.remove(file_path)
             except Exception as e:
                 print(f"Không thể xóa file {file_path}: {e}")

         os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
         with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
             writer = csv.writer(f)
             writer.writerow(["user_id", "name", "session_id", "timestamp"])

         messagebox.showinfo("Thành công", "Đã reset toàn bộ dữ liệu và ảnh khuôn mặt!")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể reset dữ liệu: {e}")
def xem_danh_sach_nguoi_dung():
    top = tk.Toplevel(root)
    top.title("Danh sách người dùng")
    top.geometry("600x350")

    cols = ("ID", "Tên")
    tree = ttk.Treeview(top, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=180)
    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def load_data():
        db = DatabaseService()
        try:
            users = db.fetchall("SELECT id, name FROM Users")
        except Exception as e:
            db.close()
            top.after(0, lambda: messagebox.showerror("Lỗi", f"Không thể tải danh sách: {e}"))
            return

        db.close()

        if not users:
            top.after(0, lambda: messagebox.showinfo("Thông báo", "Chưa có người dùng nào trong hệ thống."))
            return

        # tính số ảnh của từng user
        data = []
        for user_id, name in users:
            count = len([f for f in os.listdir(FACES_DIR) if f.startswith(f"{user_id}_")])
            data.append((user_id, name, count))

        # update UI trên thread chính
        def update_tree():
            for row in data:
                tree.insert("", tk.END, values=row)

        top.after(0, update_tree)

    # chạy trong thread phụ
    threading.Thread(target=load_data, daemon=True).start()

def mo_quan_ly_nguoi_dung():
    # Tạo cửa sổ con
    ql_win = tk.Toplevel(root)
    ql_win.title("Quản lý người dùng")
    ql_win.geometry("400x300")
    ql_win.resizable(False, False)

    tk.Label(ql_win, text="QUẢN LÝ NGƯỜI DÙNG", font=("Arial", 14, "bold")).pack(pady=15)

    # Nút thêm người mới (camera)
    tk.Button(ql_win, text="Thêm người mới (camera)", font=("Arial", 11),
              image=icon_themnguoi,compound="left", command=mo_them_nguoi).pack(pady=5)

    # Nút thêm người mới (file ảnh)
    tk.Button(ql_win, text="Thêm người mới (file ảnh)", font=("Arial", 11),
              image=icon_themnguoi,compound="left", command=mo_them_nguoi_file).pack(pady=5)

    # Nút xóa người dùng
    tk.Button(ql_win, text="Xóa người dùng", font=("Arial", 11),
              image=icon_delete,compound="left", command=xoa_nguoi_dung).pack(pady=5)

    # Nút reset dữ liệu
    tk.Button(ql_win, text="Reset dữ liệu", font=("Arial", 11),
              image=icon_reset,compound="left", command=reset_system).pack(pady=5)
def xem_diem_danh():
    top = tk.Toplevel(root)
    top.title("Lịch sử điểm danh")
    top.geometry("600x400")

    cols = ("id", "Tên", "Thời gian")
    tree = ttk.Treeview(top, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=180)
    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # bỏ header nếu có
            for row in reader:
                if len(row) >= 3:
                    id, name, time = row[0], row[1], row[2]
                    tree.insert("", tk.END, values=(id, name, time))
    except FileNotFoundError:
        messagebox.showinfo("Thông báo", "Chưa có dữ liệu điểm danh")

root = tk.Tk()
root.title("Hệ thống điểm danh khuôn mặt")
root.geometry("500x300")
root.resizable(False, False)

# nền
try:
    bg = Image.open(ASSETS_PATH / "background.png").resize((500, 300))
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # giữ tham chiếu để tránh GC. :contentReference[oaicite:3]{index=3}
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # đặt full nền. :contentReference[oaicite:4]{index=4}
except:
    root.configure(bg="white")

def load_icon(name, size=(24, 24)):
    img = Image.open(ASSETS_PATH / name).resize(size)
    icon = ImageTk.PhotoImage(img)
    return icon

icon_diemdanh = load_icon("face_icon.png")
icon_themnguoi = load_icon("add_user.png")
icon_thoat = load_icon("exit_icon.png")
icon_reset = load_icon("delete_icon.png")
icon_delete = load_icon("delete_users_icon.png")
icon_list = load_icon("list_icon.png")
icon_dashboard = load_icon("dashboard_icon.png")
icon_history = load_icon("history_icon.png")

title = tk.Label(root, text="HỆ THỐNG ĐIỂM DANH", font=("Arial", 20, "bold"), bg="#ffffff")
title.place(relx=0.5, rely=0.1, anchor="center")

# Frame chính giữa chứa các nút
center_frame = tk.Frame(root, bg="#ffffff")
center_frame.pack(pady=40)

btn_diem_danh = tk.Button(
    center_frame,
    text=" Điểm danh",
    font=("Arial", 14),
    image=icon_diemdanh,
    compound="left",
    padx=10,
    width=180,
    command=mo_diem_danh
)
btn_diem_danh.pack(pady=10)

btn_quan_ly_users = tk.Button(
    center_frame,
    text=" Quản lý người dùng",
    font=("Arial", 14),
    image=icon_dashboard,
    compound="left",
    padx=10,
    width=180,
    command=mo_quan_ly_nguoi_dung
)
btn_quan_ly_users.pack(pady=10)
btn_xem_diem_danh = tk.Button(
    root, text=" Xem điểm danh", font=("Arial", 12),
    image=icon_list, compound="left", padx=10,
    command=xem_diem_danh
)
btn_xem_diem_danh.pack(pady=3)
# Frame dưới cùng
bottom_frame = tk.Frame(root, bg="#ffffff")
bottom_frame.pack(side="bottom", fill="x", pady=20)

btn_xem_ds = tk.Button(
    bottom_frame,
    text=" Xem danh sách người dùng",
    font=("Arial", 11),
    image=icon_list,
    compound="left",
    padx=5,
    command=xem_danh_sach_nguoi_dung
)
btn_xem_ds.pack(side="left", padx=20)

btn_exit = tk.Button(
    bottom_frame,
    text=" Thoát",
    font=("Arial", 11),
    image=icon_thoat,
    compound="left",
    padx=5,
    command=root.destroy
)
btn_exit.pack(side="right", padx=20)
root.configure(bg="#ffffff")
root.mainloop()
