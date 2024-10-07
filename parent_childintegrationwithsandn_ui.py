import csv
import psutil
import subprocess
import tkinter as tk
from tkinter import ttk

class ProcessInfoGUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame  # Use parent frame instead of root directly
        self.parent_frame.title("Process Information")
        
        # Styling setup (optional)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=6, background="#66BB6A")  # Green color for buttons
        self.style.configure("TLabel", font=("Courier New", 10), background="#FFFF99")

        # Label for combobox
        self.label = ttk.Label(self.parent_frame, text="Select a connected PID:")
        self.label.pack(pady=10)

        # Combobox for PID selection
        self.combo_box = ttk.Combobox(self.parent_frame)
        self.combo_box.pack(pady=5)

        # Display button
        self.display_button = ttk.Button(self.parent_frame, text="Display Information", command=self.display_info)
        self.display_button.pack(pady=10)

        # Textbox for process and signer information
        self.text_box = tk.Text(self.parent_frame, wrap=tk.WORD, height=20, width=80)
        self.text_box.pack()

        # Load connected PIDs from CSV
        self.connected_pids = self.read_connected_pids_from_csv("process_data.csv")
        self.populate_combobox()

    def read_connected_pids_from_csv(self, file_path):
        """Reads connected PIDs from a CSV file."""
        connected_pids = []
        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    pid = int(row[0])
                    connected_pids.append(pid)
        except FileNotFoundError:
            self.text_box.insert(tk.END, f"Error: {file_path} not found.\n")
        except Exception as e:
            self.text_box.insert(tk.END, f"Error reading {file_path}: {e}\n")
        return connected_pids

    def populate_combobox(self):
        """Populates the combobox with connected PIDs."""
        if self.connected_pids:
            self.combo_box["values"] = self.connected_pids
        else:
            self.combo_box["values"] = ["No PIDs available"]

    def display_info(self):
        """Displays information for the selected PID."""
        try:
            selected_pid = int(self.combo_box.get())
        except ValueError:
            self.text_box.insert(tk.END, "Please select a valid PID.\n")
            return

        self.text_box.delete(1.0, tk.END)  # Clear the text box

        try:
            self.display_process_tree(selected_pid)
            self.get_signer_information(selected_pid)
        except psutil.NoSuchProcess:
            self.text_box.insert(tk.END, "Process not found.\n")
        except Exception as e:
            self.text_box.insert(tk.END, f"An error occurred: {e}\n")

    def display_process_tree(self, target_pid):
        """Displays the process tree for a given PID."""
        process_tree = self.get_process_tree(target_pid)
        self.text_box.insert(tk.END, "Process Tree:\n")
        self.text_box.insert(tk.END, process_tree)

    def get_process_tree(self, target_pid):
        """Retrieves the process tree for a given PID."""
        process_tree = ""
        try:
            process = psutil.Process(target_pid)
            indent = ''
            while True:
                process_tree += indent + f"PID: {process.pid}, Name: {process.name()}\n"
                children = process.children(recursive=False)
                if len(children) == 0:
                    break
                process = children[0]
                indent += '  '
        except psutil.NoSuchProcess:
            process_tree = "Process not found."
        return process_tree

    def get_signer_information(self, process_id):
        """Retrieves signer information using PowerShell."""
        try:
            process_exe = psutil.Process(process_id).exe()
        except psutil.AccessDenied:
            self.text_box.insert(tk.END, "Access Denied: Could not retrieve executable path.\n")
            return
        except psutil.NoSuchProcess:
            self.text_box.insert(tk.END, "Process not found.\n")
            return

        if not process_exe:
            self.text_box.insert(tk.END, "Process executable path not available.\n")
            return

        powershell_script = (
            f"Get-AuthenticodeSignature -FilePath '{process_exe}' | "
            "Select-Object -ExpandProperty SignerCertificate | "
            "Format-List"
        )
        
        cmd = ["powershell", "-Command", powershell_script]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            self.text_box.insert(tk.END, "Signer Information:\n")
            self.text_box.insert(tk.END, result.stdout)
        else:
            self.text_box.insert(tk.END, "Error while retrieving signer information:\n")
            self.text_box.insert(tk.END, result.stderr)

# Main application logic with parent integration
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parent Application")

        # Create a frame for the child component
        self.child_frame = ttk.Frame(self.root)
        self.child_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Initialize the ProcessInfoGUI in the parent frame
        self.process_info_gui = ProcessInfoGUI(self.child_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)  # Create the main application and integrate ProcessInfoGUI
    root.mainloop()
