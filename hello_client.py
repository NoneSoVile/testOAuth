import requests
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_sensor_data')
def get_sensor_data():
    sensor_url = 'http://localhost:5000/sensor'  # Replace with your server URL and port
    headers = {'Accept': 'text/event-stream'}

    try:
        with requests.get(sensor_url, headers=headers, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    print(f"Received sensor data: {line.decode('utf-8')}")
                    yield (line)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sensor data: {e}")

    return "Sensor data fetching finished."

if __name__ == '__main__':
    app.run(debug=True)
