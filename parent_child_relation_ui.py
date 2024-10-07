import tkinter as tk
from tkinter import ttk
import psutil
import threading

def show_warning_message(parent):
    popup = tk.Toplevel(parent)
    popup.title("Warning")
    popup.configure(bg="red")

    message = "Process Not Found"
    label = tk.Label(popup, text=message, fg="black", bg="red")
    label.pack(padx=80, pady=20)

    warning_label = tk.Label(popup, text="⚠️", font=("Arial", 40), fg="black", bg="red")
    warning_label.pack()

    close_button = tk.Button(popup, text="OK", command=popup.destroy)
    close_button.pack(pady=35)

class ProcessInfoApp:
    def __init__(self, parent):
        self.parent = parent

        # Create and place GUI elements in the parent frame
        self.process_name_label = ttk.Label(self.parent, text="Enter Process Name:")
        self.process_name_label.pack(pady=10)

        self.process_name_entry = ttk.Entry(self.parent)
        self.process_name_entry.pack(pady=5)

        self.find_button = ttk.Button(self.parent, text="Find Process", command=self.start_search)
        self.find_button.pack(pady=10)

        self.result_label = ttk.Label(self.parent, text="")
        self.result_label.pack()

    def start_search(self):
        """Start the process search in a separate thread to avoid freezing the UI."""
        self.result_label.config(text="Searching...", foreground="blue")
        search_thread = threading.Thread(target=self.find_and_display_process)
        search_thread.start()

    def find_and_display_process(self):
        process_name = self.process_name_entry.get()
        target_process = None

        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'].lower() == process_name.lower():
                target_process = process
                break

        if target_process is None:
            self.result_label.config(text=f"Process not found: {process_name}", foreground="black")
            show_warning_message(self.parent)  # Use the parent for the warning message
        else:
            process_id = target_process.info['pid']
            process_name = target_process.info['name']
            process_path = get_process_path(process_id)
            parent_process_id, parent_process_name, parent_process_path = get_parent_process_info(process_id)

            self.result_label.config(text="Target Process Information:\n" +
                                     f"Process Name: {process_name}\n" +
                                     f"Process ID: {process_id}\n" +
                                     f"Process Path: {process_path}\n" +
                                     f"Parent Process ID: {parent_process_id}\n" +
                                     f"Parent Process Name: {parent_process_name}\n" +
                                     f"Parent Process Path: {parent_process_path}", foreground="green")

def get_parent_process_info(process_id):
    try:
        parent = psutil.Process(process_id)
        return parent.ppid(), parent.name(), parent.exe()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None, "", ""

def get_process_path(process_id):
    try:
        process = psutil.Process(process_id)
        return process.exe()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "Access denied for this PID: " + str(process_id)
