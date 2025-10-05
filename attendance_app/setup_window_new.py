from customtkinter import *
import serial.tools.list_ports
import time
import threading

# =========================
# GLOBAL CONFIGURATION
# =========================
WINDOW_SIZE = "600x400"

# Colors
COLOR_BG = "#E6E6E6"
COLOR_TEXT = "#313131"
COLOR_ENTRY_BG = "white"
COLOR_ENTRY_BORDER = "white"
COLOR_ENTRY_TEXT = "black"

# Font
FONT_LABEL = ("Arial", 16, "bold")

# Padding
PAD_X = 20
PAD_Y = 10
ENTRY_CORNER_RADIUS = 32
ENTRY_WIDTH = 200  # pixels

# Refresh interval for COM ports (seconds)
COM_REFRESH_INTERVAL = 1


# =========================
# HELPER FUNCTIONS
# =========================
def list_com_ports():
    """Return a list of available COM ports with descriptions."""
    return [f"{port.device} — {port.description}" for port in serial.tools.list_ports.comports()]


def update_com_ports(combobox):
    """Continuously update available COM ports."""
    global available_coms
    while True:
        new_ports = list_com_ports()
        if new_ports != available_coms:
            available_coms = new_ports
            combobox.configure(values=available_coms)
            combobox.set("Choose COM port")
        time.sleep(COM_REFRESH_INTERVAL)

def open_setup(start_callback):
    # =========================
    # MAIN WINDOW SETUP
    # =========================
    setup_window = CTk()
    #setup_window.geometry(WINDOW_SIZE)

    # Right-side frame
    col_frame = CTkFrame(setup_window, fg_color=COLOR_BG)
    col_frame.grid(row=0, column=1, rowspan=11, columnspan=2, sticky="nsew")

    # Column label (for layout clarity)
    label_col1 = CTkLabel(setup_window, text='col1', pady=PAD_Y, padx=100)
    label_col1.grid(row=0, column=0)

    # =========================
    # INPUT FIELDS
    # =========================
    def create_label(master, text, row, column, pady=(PAD_Y, 2)):
        label = CTkLabel(master, text=text, pady=pady[0], text_color=COLOR_TEXT,
                        font=FONT_LABEL, bg_color=COLOR_BG)
        label.grid(row=row, column=column, sticky="w", padx=PAD_X, pady=pady)
        return label

    def create_entry(master, row, column, **kwargs):
        entry = CTkEntry(master,
                        corner_radius=ENTRY_CORNER_RADIUS,
                        fg_color=COLOR_ENTRY_BG,
                        text_color=COLOR_ENTRY_TEXT,
                        border_color=COLOR_ENTRY_BORDER,
                        bg_color=COLOR_BG,
                        width=ENTRY_WIDTH)
        entry.grid(row=row, column=column, sticky="w", padx=PAD_X, **kwargs)
        return entry

    def add_placeholder(entry, placeholder_text):
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, "end")
                entry.configure(text_color=COLOR_ENTRY_TEXT)

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder_text)
                entry.configure(text_color="grey")  # placeholder text color

        entry.insert(0, placeholder_text)
        entry.configure(text_color="grey")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)


    # Name
    create_label(setup_window, "Name Teacher", 0, 1, pady=(PAD_Y, 2))
    name_entry = create_entry(setup_window, 1, 1, pady=(2, PAD_Y))
    add_placeholder(name_entry, "insert your name")

    # Course
    create_label(setup_window, "Course", 2, 1, pady=(PAD_Y, 2))
    course_entry = create_entry(setup_window, 3, 1, pady=(2, PAD_Y))
    add_placeholder(course_entry, "eg: FabLab Experience")

    # Group
    create_label(setup_window, "Group", 4, 1, pady=(PAD_Y, 2))
    group_entry = create_entry(setup_window, 5, 1, pady=(2, PAD_Y))
    add_placeholder(group_entry, "eg: 2-MCT-b")

    # Classroom
    create_label(setup_window, "Classroom", 6, 1, pady=(PAD_Y, 2))
    classroom_entry = create_entry(setup_window, 7, 1, pady=(2, PAD_Y))
    add_placeholder(classroom_entry, "eg: B-109")

    # Start time
    create_label(setup_window, "Start time", 8, 1, pady=(PAD_Y, 2))
    start_time_entry = create_entry(setup_window, 9, 1, pady=(2, PAD_Y))
    add_placeholder(start_time_entry, "hh:mm format")

    # Date
    create_label(setup_window, "Date", 0, 2, pady=(PAD_Y, 2))
    date_entry = create_entry(setup_window, 1, 2, pady=(2, PAD_Y))

    # COM port dropdown
    create_label(setup_window, "USB COM", 2, 2)
    available_coms = list_com_ports()
    com_list = CTkComboBox(setup_window, values=available_coms,
                        bg_color=COLOR_BG, fg_color=COLOR_ENTRY_BG,
                        border_color=COLOR_ENTRY_BORDER, text_color=COLOR_ENTRY_TEXT, width=ENTRY_WIDTH)
    com_list.set("Choose COM-port")
    com_list.grid(row=3, column=2, sticky="w", padx=PAD_X, pady=PAD_Y)

    # Notes
    create_label(setup_window, "Notes", 4, 2)
    notes_entry = CTkTextbox(setup_window, bg_color=COLOR_BG, fg_color=COLOR_ENTRY_BG,
                        border_color=COLOR_ENTRY_BORDER, text_color=COLOR_ENTRY_TEXT, width=ENTRY_WIDTH)
    notes_entry.grid(row=5, column=2, rowspan=5, sticky="w", padx=PAD_X, pady=PAD_Y)

    setup_window.update_idletasks()

    # =========================
    # THREAD FOR COM PORTS
    # =========================
    threading.Thread(target=update_com_ports, args=(com_list,), daemon=True).start()

    def on_start():
            metadata = {
                "name": name_entry.get(),
                "date": date_entry.get(),
                "course": course_entry.get(),
                "group": group_entry.get(),
                "classroom": classroom_entry.get(),
                "start_time": start_time_entry.get(),
                "notes": notes_entry.get("1.0", tk.END).strip(),
                "com_port": opt_var.get().split(" ")[0]  # Extract COM port only
            }
            setup_window.destroy()
            start_callback(metadata)

    start_button = CTkButton(
        setup_window,
        text="Start",
        height=40,  # makes it taller
        command=on_start,
        fg_color=COLOR_TEXT,
        bg_color=COLOR_BG,
        text_color="white",
        corner_radius=32,
        font=("Arial", 16, "bold")  # big and bold text
    )
    start_button.grid(row=10, column=1, columnspan=2, sticky="ew", padx=PAD_X, pady=PAD_Y)

    # =========================
    # RUN WINDOW
    # =========================
    setup_window.mainloop()
