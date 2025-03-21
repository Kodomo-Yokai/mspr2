from flask import Flask, render_template, jsonify
import psutil
import socket

app = Flask(__name__)

def get_system_info():
    """Récupère les informations système"""
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
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