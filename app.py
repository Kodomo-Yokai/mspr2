import psutil
import socket
import platform
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.root.geometry("800x600")

        self.label = tk.Label(root, text="Network Supervisor - System Monitoring", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=10)
        
        self.result_area = scrolledtext.ScrolledText(self.result_frame, width=70, height=10, font=("Arial", 12))
        self.result_area.pack()
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        
        self.refresh_button = tk.Button(self.button_frame, text="Refresh", command=self.update_info, font=("Arial", 12, "bold"))
        self.refresh_button.grid(row=0, column=0, padx=5)
        
        self.auto_refresh = tk.BooleanVar()
        self.auto_refresh_check = tk.Checkbutton(self.button_frame, text="Auto Refresh (5s)", variable=self.auto_refresh, font=("Arial", 12))
        self.auto_refresh_check.grid(row=0, column=1, padx=5)
        
        self.fig, self.axs = plt.subplots(1, 3, figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10)
        
        self.update_info()
        self.start_auto_refresh()

    def update_info(self):
        self.result_area.delete(1.0, tk.END)
        info = get_system_info()
        for key, value in info.items():
            self.result_area.insert(tk.END, f"{key}: {value}\n\n")
        self.update_graphs(info)

    def update_graphs(self, info):
        self.axs[0].clear()
        self.axs[1].clear()
        self.axs[2].clear()
        
        self.axs[0].pie([float(info["CPU Usage"].replace('%', '')), 100 - float(info["CPU Usage"].replace('%', ''))], labels=["Used", "Free"], autopct='%1.1f%%', colors=['red', 'green'])
        self.axs[0].set_title("CPU Usage")
        
        ram_percent = float(info["RAM Usage"].split('%')[0])
        self.axs[1].pie([ram_percent, 100 - ram_percent], labels=["Used", "Free"], autopct='%1.1f%%', colors=['blue', 'lightblue'])
        self.axs[1].set_title("RAM Usage")
        
        disk_percent = float(info["Disk Usage"].split('%')[0])
        self.axs[2].pie([disk_percent, 100 - disk_percent], labels=["Used", "Free"], autopct='%1.1f%%', colors=['orange', 'yellow'])
        self.axs[2].set_title("Disk Usage")
        
        self.canvas.draw()

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
