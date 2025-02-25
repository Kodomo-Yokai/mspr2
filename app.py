import nmap
import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class SeahawksHarvester:
    def __init__(self, root):
        self.root = root
        self.root.title("Seahawks Harvester")
        self.root.geometry("600x400")

        self.label = tk.Label(root, text="Seahawks Harvester - Network Scanner")
        self.label.pack()
        
        self.scan_button = tk.Button(root, text="Scan Network", command=self.scan_network)
        self.scan_button.pack()
        
        self.result_area = scrolledtext.ScrolledText(root, width=70, height=15)
        self.result_area.pack()
        
        self.get_local_info()
    
    def get_local_info(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.result_area.insert(tk.END, f"Local Host: {hostname}\nIP Address: {ip_address}\n\n")
    
    def scan_network(self):
        self.result_area.insert(tk.END, "Scanning network...\n")
        self.result_area.update()
        scanner = nmap.PortScanner()
        local_ip = socket.gethostbyname(socket.gethostname())
        network = ".".join(local_ip.split(".")[:3]) + ".0/24"
        
        def run_scan():
            scanner.scan(hosts=network, arguments="-sn")
            self.result_area.insert(tk.END, "Scan Completed:\n")
            for host in scanner.all_hosts():
                self.result_area.insert(tk.END, f"Host: {host} ({scanner[host].hostname()})\n")
            self.result_area.insert(tk.END, "\n")
        
        thread = threading.Thread(target=run_scan)
        thread.start()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = SeahawksHarvester(root)
    root.mainloop()
