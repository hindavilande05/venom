import tkinter as tk
from tkinter import ttk
import psutil
from network_complete_ui import InternetConnectionsApp  # First .py file
from newproc_spawn_ui import ProcessMonitorApp  # Second .py file
from parent_child_relation_ui import ProcessInfoApp  # Import needed functions
from parent_childintegrationwithsandn_ui import ProcessInfoGUI  # Fourth .py file

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KernelBuddy - Malware Analysis Tool")


        # Add owner label at the bottom
        self.owner_label = ttk.Label(self.root, text="Owner - Hindavi", style="TLabel")
        self.owner_label.pack(side=tk.BOTTOM, pady=10)

       

        # Create a Notebook (tabs container)
        self.tab_control = ttk.Notebook(self.root)

        # Create tabs
        self.network_tab = ttk.Frame(self.tab_control)
        self.process_monitor_tab = ttk.Frame(self.tab_control)
        self.process_info_tab = ttk.Frame(self.tab_control)
        self.signer_info_tab = ttk.Frame(self.tab_control)

        # Add tabs to the Notebook
        self.tab_control.add(self.network_tab, text="Network Connections")
        self.tab_control.add(self.process_monitor_tab, text="Process Monitor")
        self.tab_control.add(self.process_info_tab, text="Process Info")
        self.tab_control.add(self.signer_info_tab, text="PID Signer Info")
        self.tab_control.pack(expand=1, fill="both")

        # Initialize and place content into each tab
        self.create_network_tab()
        self.create_process_monitor_tab()
        self.create_process_info_tab()
        self.create_signer_info_tab()

        # Add owner label at the bottom
        self.owner_label = ttk.Label(self.root, text="Owner - Hindavi at Bommon", style="TLabel")
        self.owner_label.pack(side=tk.BOTTOM, pady=10)

    def set_dark_mode(self):
        """Configure the dark theme for the application."""
        self.style.theme_use('clam')

        # Set dark colors
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure("TNotebook", background="#2e2e2e", foreground="#ffffff")
        self.style.configure("TNotebook.Tab", background="#444444", foreground="#ffffff")
        self.style.map("TNotebook.Tab", background=[("selected", "#1e1e1e")])

        # Configure general widget colors
        self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
        self.style.configure("TButton", background="#444444", foreground="#ffffff")
        self.style.configure("Treeview", background="#2e2e2e", foreground="#ffffff", fieldbackground="#2e2e2e")
        self.style.configure("Treeview.Heading", background="#444444", foreground="#ffffff")

        # Configure scrollbar colors
        self.style.configure("Vertical.TScrollbar", background="#444444", foreground="#ffffff")

        # Set background for root window
        self.root.configure(bg="#2e2e2e")

    def create_network_tab(self):
        """Initializes the Network Connections tab."""
        self.network_tab.grid_rowconfigure(0, weight=1)
        self.network_tab.grid_columnconfigure(0, weight=1)
        InternetConnectionsApp(self.network_tab)  # Load the InternetConnectionsApp from your first file

    def create_process_monitor_tab(self):
        """Initializes the Process Monitor tab."""
        self.process_monitor_tab.grid_rowconfigure(0, weight=1)
        self.process_monitor_tab.grid_columnconfigure(0, weight=1)
        ProcessMonitorApp(self.process_monitor_tab)  # Load the ProcessMonitorApp from your second file

    def create_process_info_tab(self):
        # """Initializes the Process Information tab."""
        # # Create entry and button in the tab
        # process_name_label = ttk.Label(self.process_info_tab, text="Enter Process Name:")
        # process_name_label.pack(pady=10)

        # self.process_name_entry = ttk.Entry(self.process_info_tab)
        # self.process_name_entry.pack(pady=5)

        # find_button = ttk.Button(self.process_info_tab, text="Find Process", command=self.find_process)
        # find_button.pack(pady=10)

        # self.result_label = ttk.Label(self.process_info_tab, text="")
        # self.result_label.pack()
        """Initializes the Process Information tab."""
        ProcessInfoApp(self.process_info_tab)  # Use the tab frame as the parent

    # def find_process(self):
    #     """Finds and displays process information."""
    #     process_name = self.process_name_entry.get()
    #     target_process = None

    #     for process in psutil.process_iter(['pid', 'name']):
    #         if process.info['name'].lower() == process_name.lower():
    #             target_process = process
    #             break

    #     if target_process is None:
    #         self.result_label.config(text=f"Process not found: {process_name}", foreground="red")
    #     else:
    #         process_id = target_process.info['pid']
    #         process_name = target_process.info['name']
    #         process_path = get_process_path(process_id)
    #         parent_process_id, parent_process_name, parent_process_path = get_parent_process_info(process_id)

    #         # Display results
    #         self.result_label.config(
    #             text=f"Process Name: {process_name}\n"
    #                  f"Process ID: {process_id}\n"
    #                  f"Process Path: {process_path}\n"
    #                  f"Parent Process ID: {parent_process_id}\n"
    #                  f"Parent Process Name: {parent_process_name}\n"
    #                  f"Parent Process Path: {parent_process_path}",
    #             foreground="green"
    #         )

    def create_signer_info_tab(self):
        """Initializes the PID Signer Info tab."""
        self.signer_info_tab.grid_rowconfigure(0, weight=1)
        self.signer_info_tab.grid_columnconfigure(0, weight=1)
        ProcessInfoGUI(self.signer_info_tab)  # Load the ProcessInfoGUI from your fourth file


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
