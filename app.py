from flask import Flask, render_template
import psutil
import platform
import socket

app = Flask(__name__)

@app.route("/")
def home():
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "N/A"
    plugged = battery.power_plugged if battery else "N/A"

    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return render_template("index.html",
                           battery_percent=battery_percent,
                           plugged=plugged,
                           cpu_usage=cpu_usage,
                           memory_usage=memory_usage,
                           hostname=hostname,
                           ip_address=ip_address)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
