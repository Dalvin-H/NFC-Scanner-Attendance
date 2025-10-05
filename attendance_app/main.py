import attendance_app.setup_window_old as setup_window_old
import attendance_window  # your attendance window logic file

def start_app(metadata):
    print("Setup complete:", metadata)
    attendance_window.open_attendance(metadata, metadata["com_port"])  # pass COM port from metadata


setup_window_old.open_setup(start_app)
