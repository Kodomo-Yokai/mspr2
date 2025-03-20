from flask import Flask, render_template
import psutil
import socket
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

def get_system_info():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "os": f"{psutil.os.name} ({psutil.os.sys.platform})"
    }

def generate_pie_chart(label, value, title):
    fig = go.Figure(data=[go.Pie(labels=[label, "Libre"], values=[value, 100-value], hole=0.3)])
    fig.update_layout(title_text=title)
    return pio.to_html(fig, full_html=False)

@app.route('/')
def index():
    info = get_system_info()
    cpu_chart = generate_pie_chart("CPU Utilisé", info["cpu"], "Utilisation CPU (%)")
    ram_chart = generate_pie_chart("RAM Utilisée", info["ram"], "Utilisation RAM (%)")
    disk_chart = generate_pie_chart("Stockage Utilisé", info["disk"], "Utilisation Stockage (%)")

    return render_template("index.html", info=info, cpu_chart=cpu_chart, ram_chart=ram_chart, disk_chart=disk_chart)

if __name__ == '__main__':
    app.run(debug=True)
