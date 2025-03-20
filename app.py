import psutil
import socket
import platform
import tkinter as tk
from tkinter import scrolledtext
import threading
import time

def get_system_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = platform.system() + " " + platform.release()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "Hostname": hostname,
        "IP Address": ip_address,
        "OS": os_info,
        "CPU Usage": f"{cpu_usage}%",
        "RAM Usage": f"{ram.percent}% ({ram.used / (1024 ** 3):.2f} GB / {ram.total / (1024 ** 3):.2f} GB)",
        "Disk Usage": f"{disk.percent}% ({disk.used / (1024 ** 3):.2f} GB / {disk.total / (1024 ** 3):.2f} GB)"
    }

class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Supervisor")
        self.root.geometry("600x400")

        self.label = tk.Label(root, text="Network Supervisor - System Monitoring")
        self.label.pack()
        
        self.result_area = scrolledtext.ScrolledText(root, width=70, height=15)
        self.result_area.pack()
        
        self.refresh_button = tk.Button(root, text="Refresh", command=self.update_info)
        self.refresh_button.pack()
        
        self.auto_refresh = tk.BooleanVar()
        self.auto_refresh_check = tk.Checkbutton(root, text="Auto Refresh (5s)", variable=self.auto_refresh)
        self.auto_refresh_check.pack()
        
        self.update_info()
        self.start_auto_refresh()

    def update_info(self):
        self.result_area.delete(1.0, tk.END)
        info = get_system_info()
        for key, value in info.items():
            self.result_area.insert(tk.END, f"{key}: {value}\n")

    def auto_refresh_loop(self):
        while True:
            if self.auto_refresh.get():
                self.update_info()
            time.sleep(5)

    def start_auto_refresh(self):
        thread = threading.Thread(target=self.auto_refresh_loop, daemon=True)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()
