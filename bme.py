import smbus2
import bme280
import json
import subprocess
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 80

def get_uptime():
    try:
        # Read uptime from /proc/uptime
        with open("/proc/uptime", "r") as file:
            uptime_seconds = float(file.readline().split()[0])
        # Convert seconds to a more human-readable format
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        file.close()
        return f"{days}d {hours}h {minutes}m {seconds}s"
    except Exception as e:
        return f"Error reading uptime: {e}"

def get_cpu_temperature():
    try:
        # Run the vcgencmd command and get the output
        output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        # Extract the temperature value
        temp = output.split("=")[1].strip("C\n")
        return temp
    except Exception as e:
        return f"Error reading CPU temperature: {e}"

class sensor:
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        self.address = 0x77
        pass

    def data(self):
        return bme280.sample(self.bus, self.address, bme280.load_calibration_params(self.bus, self.address))

def get_sensor_data():
    data = sensor().data()
    return {
        "temperature": str(round(data.temperature,2)) + ' °C',
        "humidity": str(round(data.humidity,2)) + ' rH',
        "pressure": str(round(data.pressure,2)) + ' hPa',
        "dt": str(datetime.now()),
        "cpu_temperature": get_cpu_temperature() + 'C',
        "uptime": get_uptime()
    }

class JSONRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            data = get_sensor_data()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("", PORT), JSONRequestHandler)
    print(f"Server running on port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()
