from flask import Flask, render_template, jsonify
import psutil
import socket
from ipaddress import ip_interface

app = Flask(__name__)

def get_system_info():
    """Récupère les informations système, y compris le masque CIDR"""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    cidr = None

    # Récupération du masque de sous-réseau en notation CIDR
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.address == ip_address and addr.family == socket.AF_INET:
                cidr = ip_interface(f"{addr.address}/{addr.netmask}").network.prefixlen
                break

    return {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "hostname": hostname,
        "ip": f"{ip_address}/{cidr}" if cidr else ip_address,  # Ajout du CIDR si disponible
        "os": f"{psutil.os.name} ({psutil.os.sys.platform})"
    }

@app.route('/')
def index():
    """Affiche la page principale"""
    info = get_system_info()
    return render_template("index.html", info=info)

@app.route('/update_data')
def update_data():
    """Envoie uniquement les valeurs brutes pour l'affichage"""
    info = get_system_info()
    print("🔹 Données envoyées :", info)  # Debugging
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)
