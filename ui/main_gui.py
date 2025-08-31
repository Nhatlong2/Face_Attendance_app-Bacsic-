# ui/main_gui.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess, os, sys
from pathlib import Path

ASSETS_PATH = Path(__file__).with_name("assets")
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # face_attendance_app/
SCRIPTS_DIR = PROJECT_ROOT / "scripts"  # nếu bạn để nhandien.py/chupanh.py trong scripts/

def run_py(script_path):
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)  # xử lý tốt path có dấu cách
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {script_path}\n{e}")  # subprocess.run chuẩn. :contentReference[oaicite:2]{index=2}

def mo_diem_danh():
    run_py(SCRIPTS_DIR / "nhandien.py")

def mo_them_nguoi():
    run_py(SCRIPTS_DIR / "chupanh.py")

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

title = tk.Label(root, text="HỆ THỐNG ĐIỂM DANH", font=("Arial", 20, "bold"), bg="#ffffff")
title.place(relx=0.5, rely=0.1, anchor="center")

tk.Button(root, text="  Điểm danh", font=("Arial", 12),
          image=icon_diemdanh, compound="left", padx=10, command=mo_diem_danh).place(relx=0.5, rely=0.4, anchor="center")

tk.Button(root, text="  Thêm người mới", font=("Arial", 12),
          image=icon_themnguoi, compound="left", padx=10, command=mo_them_nguoi).place(relx=0.5, rely=0.55, anchor="center")

tk.Button(root, text="  Thoát", font=("Arial", 12),
          image=icon_thoat, compound="left", padx=10, command=root.destroy).place(relx=0.5, rely=0.70, anchor="center")

root.mainloop()
