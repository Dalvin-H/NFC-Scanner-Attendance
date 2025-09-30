import setup_window
import attendance_window  # your attendance window logic file

def start_app(metadata):
    print("Setup complete:", metadata)
    attendance_window.open_attendance(metadata, metadata["com_port"])  # pass COM port from metadata


setup_window.open_setup(start_app)
