from flask import Flask, render_template, jsonify
import psutil
import subprocess
import platform
import socket
from ping3 import ping

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status")
def status():
    battery = psutil.sensors_battery()
    battery_status = {
        "percent": battery.percent if battery else "N/A",
        "plugged": battery.power_plugged if battery else "N/A"
    }

    if platform.system() == "Windows":
        try:
            wifi_result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
            wifi_connected = "connected" in wifi_result.lower()
        except:
            wifi_connected = False

        try:
            bt_result = subprocess.check_output(
                'powershell "Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq 'OK' }"',
                shell=True
            ).decode()
            bt_connected = "OK" in bt_result
        except:
            bt_connected = False
    else:
        wifi_connected = "Unsupported"
        bt_connected = "Unsupported"

    try:
        ping_result = ping("google.com", timeout=2)
        ping_status = "Online" if ping_result else "Offline"
    except:
        ping_status = "Offline"

    return jsonify({
        "battery": battery_status,
        "wifi": wifi_connected,
        "bluetooth": bt_connected,
        "internet": ping_status,
        "cpu_usage": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "hostname": socket.gethostname()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)