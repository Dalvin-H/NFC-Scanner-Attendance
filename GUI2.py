import tkinter as tk
import datetime
import serial
import sqlite3
import threading

# Database setup (SQLite)
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# --- Attendance Table Class ---
class Table:
    def __init__(self, root, data, headers):
        for widget in root.winfo_children():
            widget.destroy()
        # Headers
        for j, header in enumerate(headers):
            e = tk.Entry(root, width=20, fg='black',
                        font=('Arial', 12, 'bold'))
            e.grid(row=0, column=j)
            e.insert(tk.END, header)
        # Data
        for i, row in enumerate(data, start=1):
            for j, val in enumerate(row):
                e = tk.Entry(root, width=20, fg='blue',
                            font=('Arial', 12))
                e.grid(row=i, column=j)
                e.insert(tk.END, val)


# --- New Window after setup ---
def open_new_window():
    name = name_entry.get()
    date = date_entry.get()
    course = course_entry.get()
    group = group_entry.get()
    classroom = class_entry.get()
    start_time = time_entry.get()
    notes = notes_box.get("1.0", tk.END).strip()

    setup_window.destroy()

    list_window = tk.Tk()
    list_window.geometry("800x400")
    list_window.title("Attendance List")

    frame_meta = tk.Frame(list_window)
    frame_meta.pack(pady=10)

    tk.Label(frame_meta, text="Date:").grid(row=0, column=0, sticky="e")
    date_entry_meta = tk.Entry(frame_meta, width=30)
    date_entry_meta.grid(row=0, column=1)
    date_entry_meta.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

    # Attendance table data
    lst = []
    headers = ("ID", "Time", "Student Name", "Status")

    container = tk.Frame(list_window)
    container.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame_table = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_table, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_table.bind("<Configure>", on_frame_configure)

    table = Table(frame_table, lst, headers)

    # --- Add Student Function (from NFC scan) ---
    def add_student(uid):
        cursor.execute("SELECT name FROM users WHERE uid = ?", (uid,))
        result = cursor.fetchone()
        if result:
            student_name = result[0]
            now = datetime.datetime.now().strftime("%H:%M:%S")
            new_id = len(lst) + 1
            lst.append((new_id, now, student_name, "Present"))
            Table(frame_table, lst, headers)
        else:
            print(f"Unknown UID: {uid}")

    # --- Serial Reader Thread ---
    def read_serial():
        try:
            ser = serial.Serial(opt.get(), 115200, timeout=1)
            print(f"Listening on {opt.get()}")
        except Exception as e:
            print(f"Serial error: {e}")
            return

        while True:
            line = ser.readline().decode("utf-8").strip()
            if line:
                print(f"UID: {line}")
                list_window.after(0, add_student, line)

    threading.Thread(target=read_serial, daemon=True).start()

    # --- Save Function ---
    def save_file():
        date_val = date_entry_meta.get()
        print("Saving attendance for:", date_val)
        for row in lst:
            print(row)

    tk.Button(list_window, text="Save Attendance List", command=save_file).pack(pady=5)
    tk.Button(list_window, text="Close", command=list_window.destroy).pack(pady=10)

    list_window.mainloop()


# --- Setup Window ---
setup_window = tk.Tk()
setup_window.geometry("400x300")
setup_window.title("Attendance NFC Scanner Setup")

tk.Label(setup_window, text='Name', pady=10).grid(row=0, column=0)
tk.Label(setup_window, text='Date', pady=10).grid(row=1, column=0)
tk.Label(setup_window, text='Course', pady=10).grid(row=2, column=0)
tk.Label(setup_window, text='Group', pady=10).grid(row=3, column=0)
tk.Label(setup_window, text='Classroom', pady=10).grid(row=4, column=0)
tk.Label(setup_window, text='Start time', pady=10).grid(row=5, column=0)

tk.Label(setup_window, text='Notes', padx=10).grid(row=0, column=2)
notes_box = tk.Text(setup_window, width=20, height=6)
notes_box.grid(row=1, column=2, rowspan=3)

start_button = tk.Button(setup_window, text="Start", width=15, height=5, command=open_new_window)
start_button.grid(row=4, column=2, rowspan=2)

name_entry = tk.Entry(setup_window)
name_entry.grid(row=0, column=1, padx=10)

date_entry = tk.Entry(setup_window)
date_entry.grid(row=1, column=1, padx=10)

course_entry = tk.Entry(setup_window)
course_entry.grid(row=2, column=1, padx=10)

group_entry = tk.Entry(setup_window)
group_entry.grid(row=3, column=1, padx=10)

class_entry = tk.Entry(setup_window)
class_entry.grid(row=4, column=1, padx=10)

time_entry = tk.Entry(setup_window)
time_entry.grid(row=5, column=1, padx=10)

# --- COM Port Dropdown ---
COMS = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"]
opt = tk.StringVar(value="COM4")  # default
tk.OptionMenu(setup_window, opt, *COMS).grid(row=6, column=1, pady=10)

setup_window.mainloop()
