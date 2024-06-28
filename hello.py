from flask import Flask, send_from_directory, render_template, send_file, request, abort, Response, render_template_string
import sys, os, re
import json
import random
import time
import math
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! yf tech '

@app.route('/pic')
def serve_image():
    return send_from_directory('static/dogs', 'e5.png')

@app.route('/index')
def serve_html():
    return render_template('index.html')

@app.route('/vi')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Streaming</title>
    </head>
    <body>
        <h1>Video Streaming</h1>
        <video width="640" height="480" controls>
            <source src="/video" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </body>
    </html>
    '''

@app.route('/video')
def video():
    path = 'static/video/0.mp4'
    range_header = request.headers.get('Range', None)
    if not os.path.exists(path):
        abort(404)

    file_size = os.path.getsize(path)
    start = 0
    end = file_size - 1
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        if match:
            start = int(match.group(1))
            if match.group(2):
                end = int(match.group(2))
    
    chunk_size = end - start + 1
    with open(path, 'rb') as f:
        f.seek(start)
        data = f.read(chunk_size)

    response = Response(data, 206, mimetype='video/mp4', content_type='video/mp4')
    response.headers.add('Content-Range', f'bytes {start}-{end}/{file_size}')
    response.headers.add('Accept-Ranges', 'bytes')
    return response


# Global variables to store configuration data
radarPosX = -1.0
radarPosY = 0.0
radarAngle = 0.0
lineWidth = 5.0

def generate_config_data():
    # List of object names
    object_names = ["radar configs"]

    while True:
        # Generate a list of objects with random values for the specified attributes
        data = []
        for name in object_names:
            data.append({
                "configName": name,
                "lineWidth": lineWidth,
                "radarPosX": radarPosX,
                "radarPosY": radarPosY,
                "radarAngle": radarAngle
            })
        
        json_data = json.dumps(data)
        yield f"{json_data}\n"
        time.sleep(2.5)
        
@app.route('/radarconfig')
def config_data():
    return Response(generate_config_data(), mimetype='text/event-stream')

# Route for user input form
@app.route('/inputconfig')
def input_config():
    html_form = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Input Config Data</title>
      </head>
      <body>
        <div class="container">
          <h1>Input Radar Config Data</h1>
          <form action="/submitconfig" method="post">
            <div>
              <label for="radarPosX">Radar Pos X:</label>
              <input type="number"  step="any" id="radarPosX" name="radarPosX" value="{{ radarPosX }}">
            </div>
            <div>
              <label for="radarPosY">Radar Pos Y:</label>
              <input type="number"  step="any" id="radarPosY" name="radarPosY" value="{{ radarPosY }}">
            </div>
            <div>
              <label for="radarAngle">Radar Angle:</label>
              <input type="number"  step="any" id="radarAngle" name="radarAngle" value="{{ radarAngle }}">
            </div>
            <div>
              <label for="lineWidth">Line Width:</label>
              <input type="number"  step="any" id="lineWidth" name="lineWidth" value="{{ lineWidth }}">
            </div>
            <button type="submit">Submit</button>
          </form>
        </div>
      </body>
    </html>
    '''
    return render_template_string(html_form, radarPosX=radarPosX, radarPosY=radarPosY, radarAngle=radarAngle, lineWidth=lineWidth)

# Route to handle form submission
@app.route('/submitconfig', methods=['POST'])
def submit_config():
    global radarPosX, radarPosY, radarAngle, lineWidth
    radarPosX = float(request.form['radarPosX'])
    radarPosY = float(request.form['radarPosY'])
    radarAngle = float(request.form['radarAngle'])
    lineWidth = float(request.form['lineWidth'])
    return "Configuration updated successfully!"


        
def generate_sensor_data2():
    # List of object names
    object_names = ["Object One", "Object Two", "Object Three"]

    while True:
        # Generate a list of objects with random values for the specified attributes
        data = []
        for name in object_names:
            data.append({
                "Obstacle": name,
                "distance": random.uniform(0, 10),
                "Speed": random.uniform(0, 50),
                "InitialAngle": random.uniform(-10, 10),
                "EndAngle": random.uniform(50, 100),
                "ReflectionIntensity": random.uniform(0, 1)
            })
        
        json_data = json.dumps(data)
        yield f"{json_data}\n"
        time.sleep(0.5)
        
def generate_sensor_data3():
    # List of object names
    object_names = ["Object One", "Object Two", "Object Three"]

    # Initial ranges for each object
    initial_ranges = {
        "Object One": {
            "distance": (2, 4),
            "Speed": (0, 50),
            "InitialAngle": (-40, -30),
            "EndAngle": (-20, 0),
            "ReflectionIntensity": (0, 1)
        },
        "Object Two": {
            "distance": (4, 7),
            "Speed": (10, 60),
            "InitialAngle": (10, 30),
            "EndAngle": (30, 50),
            "ReflectionIntensity": (0.1, 0.9)
        },
        "Object Three": {
            "distance": (7 ,10),
            "Speed": (5, 55),
            "InitialAngle": (50, 65),
            "EndAngle": (75, 85),
            "ReflectionIntensity": (0.2, 0.8)
        }
    }

    # Initial values and parameters for smooth transitions
    initial_values = {
        name: {
            "distance": random.uniform(*initial_ranges[name]["distance"]),
            "Speed": random.uniform(*initial_ranges[name]["Speed"]),
            "InitialAngle": random.uniform(*initial_ranges[name]["InitialAngle"]),
            "EndAngle": random.uniform(*initial_ranges[name]["EndAngle"]),
            "ReflectionIntensity": random.uniform(*initial_ranges[name]["ReflectionIntensity"])
        }
        for name in object_names
    }
    
    current_time = 0.1#time.time()
    print(current_time)
    while True:
        #current_time_milliseconds = int(current_time)
        #print(current_time)
        current_time += 0.1#current_time_milliseconds/57

        # Generate a list of objects with smoothly changing values
        data = []
        for name in object_names:
            data.append({
                "Obstacle": name,
                "distance": initial_values[name]["distance"] + math.sin(current_time) * 4,
                "Speed": initial_values[name]["Speed"] + math.cos(current_time) * 5,
                "InitialAngle": initial_values[name]["InitialAngle"] + math.sin(current_time) * 40,
                "EndAngle": initial_values[name]["EndAngle"] + math.cos(current_time) * 20,
                "ReflectionIntensity": initial_values[name]["ReflectionIntensity"] + math.sin(current_time) * 0.1
            })

        json_data = json.dumps(data)
        yield f"{json_data}\n"
        time.sleep(0.2)
        
def generate_sensor_data5():
    # List of object names
    object_names = ["Object One", "Object Two", "Object Three", "Object Four", "Object Five"]

    # Initial ranges for each object
    initial_ranges = {
        object_names[0]: {
            "distance": (1, 4),
            "Speed": (0, 50),
            "InitialAngle": (-40, -30),
            "EndAngle": (-20, 0),
            "ReflectionIntensity": (0, 1)
        },
        object_names[1]: {
            "distance": (0, 4),
            "Speed": (10, 60),
            "InitialAngle": (10, 30),
            "EndAngle": (30, 50),
            "ReflectionIntensity": (0.1, 0.9)
        },
        object_names[2]: {
            "distance": (0 ,3),
            "Speed": (5, 55),
            "InitialAngle": (150, 165),
            "EndAngle": (175, 185),
            "ReflectionIntensity": (0.2, 0.8)
        },
        object_names[3]: {
            "distance": (1 ,2),
            "Speed": (5, 55),
            "InitialAngle": (150, 165),
            "EndAngle": (175, 185),
            "ReflectionIntensity": (0.2, 0.8)
        },
        object_names[4]: {
            "distance": (0 ,1),
            "Speed": (5, 55),
            "InitialAngle": (150, 165),
            "EndAngle": (175, 185),
            "ReflectionIntensity": (0.2, 0.8)
        }
        
    }

    # Initial values and parameters for smooth transitions
    initial_values = {
        name: {
            "distance": random.uniform(*initial_ranges[name]["distance"]),
            "Speed": random.uniform(*initial_ranges[name]["Speed"]),
            "InitialAngle": random.uniform(*initial_ranges[name]["InitialAngle"]),
            "EndAngle": random.uniform(*initial_ranges[name]["EndAngle"]),
            "ReflectionIntensity": random.uniform(*initial_ranges[name]["ReflectionIntensity"])
        }
        for name in object_names
    }
    
    current_time = 0.1#time.time()
    print(current_time)
    while True:
        #current_time_milliseconds = int(current_time)
        #print(current_time)
        current_time += 0.1#current_time_milliseconds/57

        # Generate a list of objects with smoothly changing values
        data = []
        for name in object_names:
            data.append({
                "Obstacle": name,
                "distance": initial_values[name]["distance"] + math.sin(current_time) * 1.5,
                "Speed": initial_values[name]["Speed"] + math.cos(current_time) * 5,
                "InitialAngle": initial_values[name]["InitialAngle"] + math.sin(current_time) * 50,
                "EndAngle": initial_values[name]["EndAngle"] + math.cos(current_time) * 50,
                "ReflectionIntensity": initial_values[name]["ReflectionIntensity"] + math.sin(current_time) * 0.1
            })

        json_data = json.dumps(data)
        yield f"{json_data}\n"
        time.sleep(0.06)

@app.route('/stream', methods=['POST'])
def stream():
    def generate():
        for chunk in request.stream:
            print(chunk.decode('utf-8'))
            yield chunk
    return Response(generate(), content_type='text/plain')

@app.route('/sensor')
def sensor_data():
    return Response(generate_sensor_data5(), mimetype='text/event-stream')

@app.route('/sensorpage')
def sensorpage():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sensor Data Stream</title>
    </head>
    <body>
        <h1>Sensor Data Stream</h1>
        <div id="data"></div>
        <script type="text/javascript">
            var eventSource = new EventSource("/sensor");
            eventSource.onmessage = function(event) {
                document.getElementById("data").innerHTML = event.data;
            };
        </script>
    </body>
    </html>
    '''



if __name__ == '__main__':
    port=80
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port, debug=True)
