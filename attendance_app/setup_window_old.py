import tkinter as tk
from tkinter import StringVar, OptionMenu
import serial.tools.list_ports
import threading
import time

# Global variable for COM ports list
available_coms = []

def list_com_ports():
    return [port.device + " — " + port.description for port in serial.tools.list_ports.comports()]

def update_com_ports(opt_var, dropdown):
    global available_coms
    while True:
        new_ports = list_com_ports()
        if new_ports != available_coms:
            available_coms = new_ports
            dropdown['menu'].delete(0, 'end')
            for com in available_coms:
                dropdown['menu'].add_command(label=com, command=tk._setit(opt_var, com))
        time.sleep(1)  # refresh every second

def open_setup(start_callback):
    setup_window = tk.Tk()
    setup_window.geometry("400x400")
    setup_window.title("Attendance NFC Scanner Setup")

    tk.Label(setup_window, text='Name', pady=10).grid(row=0)
    tk.Label(setup_window, text='Date', pady=10).grid(row=1)
    tk.Label(setup_window, text='Course', pady=10).grid(row=2)
    tk.Label(setup_window, text='Group', pady=10).grid(row=3)
    tk.Label(setup_window, text='Classroom', pady=10).grid(row=4)
    tk.Label(setup_window, text='Start time', pady=10).grid(row=5)

    tk.Label(setup_window, text='Notes', padx=10).grid(row=0, column=2)
    notes_box = tk.Text(setup_window, width=20, height=6)
    notes_box.grid(row=1, column=2, rowspan=3)

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

    # COM selection dropdown
    opt_var = StringVar(value="Select COM")
    available_coms = list_com_ports()
    dropdown = OptionMenu(setup_window, opt_var, *available_coms)
    dropdown.grid(row=6, column=1, pady=10)

    # Background thread to update COM list dynamically
    threading.Thread(target=update_com_ports, args=(opt_var, dropdown), daemon=True).start()

    def on_start():
        metadata = {
            "name": name_entry.get(),
            "date": date_entry.get(),
            "course": course_entry.get(),
            "group": group_entry.get(),
            "classroom": class_entry.get(),
            "start_time": time_entry.get(),
            "notes": notes_box.get("1.0", tk.END).strip(),
            "com_port": opt_var.get().split(" ")[0]  # Extract COM port only
        }
        setup_window.destroy()
        start_callback(metadata)

    start_button = tk.Button(setup_window, text="Start", width=15, height=5, command=on_start)
    start_button.grid(row=7, column=1, pady=10)

    setup_window.mainloop()
