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

# Global variables to store configuration data
radarPosX = -1.0
radarPosY = 0.0
radarAngle = 0.0
lineWidth = 5.0
pixelSizeScale = 1.0

def generate_config_data():
    # List of object names
    object_names = ["radar configs"]

    while True:
        # Generate a list of objects with random values for the specified attributes
        data = []
        for name in object_names:
            data.append({               
                "configName": name,
                "pixelSizeScale": pixelSizeScale, 
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
            <div>
              <label for="pixelSizeScale">pixelSizeScale:</label>
              <input type="number"  step="any" id="pixelSizeScale" name="pixelSizeScale" value="{{ pixelSizeScale }}">
            </div>
            <button type="submit">Submit</button>
          </form>
        </div>
      </body>
    </html>
    '''
    return render_template_string(html_form, pixelSizeScale=pixelSizeScale, radarPosX=radarPosX, radarPosY=radarPosY, radarAngle=radarAngle, lineWidth=lineWidth)

# Route to handle form submission
@app.route('/submitconfig', methods=['POST'])
def submit_config():
    global radarPosX, radarPosY, radarAngle, lineWidth, pixelSizeScale
    radarPosX = float(request.form['radarPosX'])
    radarPosY = float(request.form['radarPosY'])
    radarAngle = float(request.form['radarAngle'])
    lineWidth = float(request.form['lineWidth'])
    pixelSizeScale = float(request.form['pixelSizeScale'])
    return "Configuration updated successfully!"


if __name__ == '__main__':
    port=80
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port, debug=True)
