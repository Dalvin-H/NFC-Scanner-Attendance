import tkinter as tk
import datetime
import serial
import threading
import database

cursor = database.cursor
conn = database.conn



# Attendance list
attendance_list = []

def open_attendance(metadata, com_port):
    # Clear attendance for a new session
    database.empty_tables()
    attendance_list.clear()

    window = tk.Tk()
    window.geometry("800x500")
    window.title("Attendance NFC Scanner")

    # Header
    tk.Label(window, text=f"Class: {metadata['course']}").pack()
    tk.Label(window, text=f"Group: {metadata['group']}").pack()
    tk.Label(window, text=f"Date: {metadata['date']}").pack()

    # Attendance Table Frame
    container = tk.Frame(window)
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

    # Table class
    class Table:
        def __init__(self, root, data, headers):
            for widget in root.winfo_children():
                widget.destroy()
            for j, header in enumerate(headers):
                e = tk.Entry(root, width=20, fg='black', font=('Arial', 12, 'bold'))
                e.grid(row=0, column=j)
                e.insert(tk.END, header)
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    e = tk.Entry(root, width=20, fg='blue', font=('Arial', 12))
                    e.grid(row=i+1, column=j)
                    e.insert(tk.END, value)

    headers = ("ID", "Time", "Student Name", "Status")
    attendance_list.append((1, datetime.datetime.now().strftime("%H:%M:%S"), "Demo Student", "Present"))
    table = Table(frame_table, attendance_list, headers)

    def add_student_manual(name, status="Present"):
        new_id = len(attendance_list) + 1
        attendance_list.append((new_id, datetime.datetime.now().strftime("%H:%M:%S"), name, status))
        Table(frame_table, attendance_list, headers)

    def save_attendance():
        date_val = metadata["date"]
        for row in attendance_list:
            print(f"Saving {row} for {date_val}")
            database.add_attendance(date_val, row[1], row[2], row[3])


    btn_add = tk.Button(window, text="Add Student", command=lambda: add_student_manual("New Student"))
    btn_add.pack(pady=5)

    btn_save = tk.Button(window, text="Save Attendance", command=save_attendance)
    btn_save.pack(pady=5)

    btn_close = tk.Button(window, text="Close", command=window.destroy)
    btn_close.pack(pady=10)

    # --- Add Student Function (from NFC scan) ---
    def add_student(uid):
        result = database.get_student(uid)
        if result:
            student_name = result[0]
            now = datetime.datetime.now().strftime("%H:%M:%S")
            new_id = len(attendance_list) + 1
            attendance_list.append((new_id, now, student_name, "Present"))
            Table(frame_table, attendance_list, headers)
        else:
            print(f"Unknown UID: {uid}")

    # --- Serial Reader Thread ---
    def read_serial():
        try:
            ser = serial.Serial(com_port, 115200, timeout=1)
            print(f"Listening on {com_port}")
        except Exception as e:
            print(f"Serial error: {e}")
            return

        while True:
            line = ser.readline().decode("utf-8").strip()
            if line:
                print(f"UID: {line}")
                window.after(0, add_student, line)

    threading.Thread(target=read_serial, daemon=True).start()

    window.mainloop()
