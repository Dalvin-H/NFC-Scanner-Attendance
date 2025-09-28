import tkinter as tk
import datetime

def open_new_window():
    # Get values from the entries
    name = name_entry.get()
    date = date_entry.get()
    course = course_entry.get()
    group = group_entry.get()
    classroom = class_entry.get()
    start_time = time_entry.get()
    notes = notes_box.get("1.0", tk.END).strip()  # get text from Text widget

    setup_window.destroy()  # close the current window
    
    list_window = tk.Tk()
    list_window.geometry("600x400")
    list_window.title("Attendance List")

    frame_meta = tk.Frame(list_window)
    frame_meta.pack(pady=10)

    tk.Label(frame_meta, text="Date:").grid(row=2, column=0, sticky="e")
    date_entry_meta = tk.Entry(frame_meta, width=30)
    date_entry_meta.grid(row=2, column=1)
    date_entry_meta.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

    # --- Attendance Table ---
    lst = [
        (1,'Raj','Mumbai',19),
        (2,'Aaryan','Pune',18),
        (3,'Vaishnavi','Mumbai',20),
        (4,'Rachna','Mumbai',21),
        (5,'Shubham','Delhi',21)
    ]

        # --- Attendance Table with Scrollbar ---
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


    class Table:
        def __init__(self, root, data, headers):
            # Clear old table first
            for widget in root.winfo_children():
                widget.destroy()
            # Add headers
            for j, header in enumerate(headers):
                e = tk.Entry(root, width=20, fg='black',
                            font=('Arial', 12, 'bold'))
                e.grid(row=0, column=j)
                e.insert(tk.END, header)
            # Build table (start at row=1 for data)
            total_rows = len(data)
            total_columns = len(data[0])
            for i in range(total_rows):
                for j in range(total_columns):
                    e = tk.Entry(root, width=20, fg='blue',
                                font=('Arial', 12))
                    e.grid(row=i+1, column=j)  # shift down by 1
                    e.insert(tk.END, data[i][j])

    # Initial table
    headers = ("ID", "Name", "City", "Age")
    table = Table(frame_table, lst, headers)

    

    # --- Add Student Function ---
    def add_student():
        new_id = len(lst) + 1
        new_student = (new_id, "NewName", "NewCity", 18)
        lst.append(new_student)
        Table(frame_table, lst, headers)  # rebuild table with headers

    # --- Save Function ---
    def save_file():
        date_val = date_entry_meta.get()
        print("Saving attendance for:", date_val)
        for row in lst:
            print(row)

    # --- Buttons ---
    btn_add = tk.Button(list_window, text="Add Student", command=add_student)
    btn_add.pack(pady=5)

    btn_save = tk.Button(list_window, text="Save Attendance List", command=save_file)
    btn_save.pack(pady=5)

    btn_close = tk.Button(list_window, text="Close", command=list_window.destroy)
    btn_close.pack(pady=10)

    list_window.mainloop()


# --- Setup Window ---
setup_window = tk.Tk()
setup_window.geometry("400x300")
setup_window.title("Attendance NFC Scanner Setup")

tk.Label(text='Name', pady=10).grid(row=0)
tk.Label(text='Date', pady=10).grid(row=1)
tk.Label(text='Course', pady=10).grid(row=2)
tk.Label(text='Group', pady=10).grid(row=3)
tk.Label(text='Classroom', pady=10).grid(row=4)
tk.Label(text='Start time', pady=10).grid(row=5)

tk.Label(text='Notes', padx=10).grid(row=0, column=2)
notes_box = tk.Text(width=20, height=6)
notes_box.grid(row=1, column=2, rowspan=3)

start_button = tk.Button(text="Start", width=15, height=5, command=open_new_window)
start_button.grid(row=4, column=2, rowspan=2)

name_entry = tk.Entry()
name_entry.grid(row=0, column=1, padx=10)

date_entry = tk.Entry()
date_entry.grid(row=1, column=1, padx=10)

course_entry = tk.Entry()
course_entry.grid(row=2, column=1, padx=10)

group_entry = tk.Entry()
group_entry.grid(row=3, column=1, padx=10)

class_entry = tk.Entry()
class_entry.grid(row=4, column=1, padx=10)

time_entry = tk.Entry()
time_entry.grid(row=5, column=1, padx=10)

setup_window.mainloop()
