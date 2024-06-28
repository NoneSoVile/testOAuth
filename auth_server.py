from flask import Flask, request, redirect, render_template_string, session, jsonify
from uuid import uuid4

app = Flask(__name__)

# This would be your registered client
CLIENTS = {
    'your-client-id': {
        'client_secret': 'your-client-secret',
        'redirect_uri': 'http://localhost:5000/callback'
    }
}

# Simple in-memory "database" for this example
AUTHORIZATION_CODES = {}
ACCESS_TOKENS = {}

@app.route('/auth')
def authorize():
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    print(f'auth server : client_id: {client_id} redirect_uri: {redirect_uri}')
    # In a real scenario, you would authenticate the user here
    # and confirm their authorization to access the data

    # Check if the client_id and redirect_uri are valid
    expectedurl = CLIENTS[client_id]['redirect_uri']
    print(f'expectedurl {expectedurl}')
    if client_id in CLIENTS and expectedurl == redirect_uri:
        # Generate an authorization code
        code = str(uuid4())
        print(f'code: {code}')
        AUTHORIZATION_CODES[code] = {'client_id': client_id}
        # Redirect back to the client with the auth code
        return redirect(f'{redirect_uri}?code={code}')
    else:
        return 'Invalid client_id or redirect_uri', 400

@app.route('/token', methods=['POST'])
def token():
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    code = request.form.get('code')

    # Validate client credentials and auth code
    if client_id in CLIENTS and CLIENTS[client_id]['client_secret'] == client_secret and code in AUTHORIZATION_CODES:
        # Generate an access token
        access_token = str(uuid4())
        print(f'auth server access_token {access_token}')
        ACCESS_TOKENS[access_token] = {'client_id': client_id}
        # Return the access token
        return jsonify(access_token=access_token)
    else:
        return 'Invalid client credentials or authorization code', 400
    
@app.route('/consent', methods=['POST'])
def consent():
    # User granted consent, now generate the authorization code
    client_id = session.get('client_id')
    redirect_uri = session.get('redirect_uri')
    
    if client_id and redirect_uri:
        # Generate an authorization code
        code = str(uuid4())
        AUTHORIZATION_CODES[code] = {'client_id': client_id}
        # Redirect back to the client with the auth code
        return redirect(f'{redirect_uri}?code={code}')
    else:
        return 'Consent not granted or session expired', 400

if __name__ == '__main__':
    app.run(port=8000, debug=True)