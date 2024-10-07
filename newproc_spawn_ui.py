import sys
import psutil
import ctypes
import tkinter as tk
from tkinter import ttk
import csv

def bytes_to_kb(bytes_value):
    return bytes_value / 1024

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class ProcessMonitorApp:
    def __init__(self, parent):
        self.root = parent  # Use the parent (Frame) provided by the main application

        # Create the output Treeview in the parent frame
        self.output_tree = ttk.Treeview(self.root)
        self.output_tree["columns"] = ("PID", "Name", "Command Line", "User", "Instance", "CPU (%)", "Memory (MB)")
        for column in self.output_tree["columns"]:
            self.output_tree.heading(column, text=column)
            self.output_tree.column(column, anchor="center")
        self.output_tree.pack(expand=True, fill='both')

        # Buttons
        self.stop_button = tk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_button.pack()

        self.export_csv_button = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv)
        self.export_csv_button.pack()

        self.process_data = []  # List to hold process data for CSV
        self.monitoring = True
        self.monitor_processes()

    def stop_monitoring(self):
        self.monitoring = False

    def monitor_processes(self):
        existing_processes = set(psutil.pids())

        while self.monitoring:
            current_processes = set(psutil.pids())
            new_processes = current_processes - existing_processes

            for pid in new_processes:
                try:
                    process = psutil.Process(pid)

                    pid_str = str(process.pid)
                    name = process.name()
                    cmdline = " ".join(process.cmdline())
                    cpu_percent = process.cpu_percent(interval=0.1)
                    memory_mb = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

                    try:
                        user = process.username()
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        user = "N/A"

                    try:
                        instance = process.create_time()
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        instance = "N/A"

                    # Add data to treeview
                    self.output_tree.insert("", "end", values=(pid_str, name, cmdline, user, instance, f"{cpu_percent:.2f}", f"{memory_mb:.2f}"))

                    # Collect process data for CSV
                    self.process_data.append([pid_str, name, cmdline, user, instance, f"{cpu_percent:.2f}", f"{memory_mb:.2f}"])

                    # Update the GUI
                    self.root.update()

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.Error):
                    pass

            existing_processes = current_processes

    def export_to_csv(self):
        # Specify the CSV file path
        csv_file_path = "process_data.csv"
        
        # Write the collected process data to a CSV file
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the headers
            writer.writerow(["PID", "Name", "Command Line", "User", "Instance", "CPU (%)", "Memory (MB)"])
            # Write the process data
            writer.writerows(self.process_data)
        
        print(f"Process data exported to {csv_file_path}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ProcessMonitorApp(root)
#     root.mainloop()
