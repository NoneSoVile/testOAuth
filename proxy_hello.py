from flask import Flask, request, Response, stream_with_context, redirect, url_for
import requests
import sys, os, re
app = Flask(__name__)

# The URL of the server to forward requests to
TARGET_SERVER_URL = 'http://47.116.191.228'
CONFIG_SERVER_URL = 'http://47.116.191.228'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
        # Get the URL to forward the request to
    url = f"{TARGET_SERVER_URL}/{path}"
    # Check if the path matches the exclusion pattern
    if path == "radarconfig": 
        return redirect(url_for('get_config_data'))  # Redirect to the excluded route
    elif path == "inputconfig" or path == "submitconfig":
        url = f"{CONFIG_SERVER_URL}/{path}"
    
    print(path)
    print(url)

    # Get the request method (GET, POST, etc.)
    method = request.method

    # Forward the request headers
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}

    # Forward the request data
    data = request.get_data()

 # Check if the request is for streaming data
    is_stream_request = False#'stream' in request.headers.get('Accept', '') or request.headers.get('Accept') == 'text/event-stream'

    # Forward the request to the target server
    with requests.request(method, url, headers=headers, data=data, params=request.args, stream=True) as response:
        # Check if the response is streaming type and if it's SSE
        if is_stream_request:# and response.headers.get('mimetype') == 'text/event-stream':
            print("text/event-stream response")
            def generate():
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        print(chunk)
                        yield chunk.decode('utf-8')

            return Response(stream_with_context(generate()), mimetype='text/event-stream', status=response.status_code, headers=dict(response.headers))
        elif is_stream_request:
            print("is_stream_request response")
            def generate():
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        print(chunk)
                        yield chunk

            return Response(stream_with_context(generate()), status=response.status_code, headers=dict(response.headers))
       
        else:
            print("ordianay response")
            return Response(response.content, status=response.status_code, headers=dict(response.headers))
        
@app.route('/sensor')
def get_sensor_data():
    sensor_url = f"{TARGET_SERVER_URL}/sensor"
    headers = {'Accept': 'text/event-stream'}

    def stream_sensor_data():
        try:
            with requests.get(sensor_url, headers=headers, stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        line_utf8 = line.decode('utf-8')
                        #print(line_utf8)
                        yield f"{line_utf8}\n\n"
        except requests.exceptions.RequestException as e:
            print(f"Error fetching sensor data: {e}")
            yield "Error fetching sensor data.\n"

    return Response(stream_sensor_data(), content_type='text/event-stream')

@app.route('/radarconfig')
def get_config_data():
    sensor_url = f"{CONFIG_SERVER_URL}/radarconfig"
    headers = {'Accept': 'text/event-stream'}

    def stream_config_data():
        try:
            with requests.get(sensor_url, headers=headers, stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        line_utf8 = line.decode('utf-8')
                        #print(line_utf8)
                        yield f"{line_utf8}\n\n"
        except requests.exceptions.RequestException as e:
            print(f"Error fetching config data: {e}")
            yield "Error fetching config data.\n"

    return Response(stream_config_data(), content_type='text/event-stream')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TARGET_SERVER_URL = sys.argv[1]
        CONFIG_SERVER_URL = sys.argv[1]
        
    if len(sys.argv) > 2:
        CONFIG_SERVER_URL = sys.argv[2]
    app.run(host='0.0.0.0', port=8080, debug=True)
