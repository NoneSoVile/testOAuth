from flask import Flask, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Change this to a random secret in production

# Replace these with your actual client ID, client secret, and auth server details
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
AUTH_SERVER_AUTHORIZE_ENDPOINT = 'http://localhost:8000/auth'
AUTH_SERVER_TOKEN_ENDPOINT = 'http://localhost:8000/token'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def home():
    # Redirect user to auth server for authentication
    auth_url = f"{AUTH_SERVER_AUTHORIZE_ENDPOINT}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # User will be redirected back to this route with 'code' in query params
    code = request.args.get('code')
    if code:
        # Exchange the authorization code for an access token
        token_response = requests.post(AUTH_SERVER_TOKEN_ENDPOINT, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        })

        if token_response.ok:
            # Store the access token in the session (or a more secure storage)
            session['access_token'] = token_response.json().get('access_token')
            return 'Authorization code exchanged for access token successfully!'
        else:
            return 'Failed to retrieve access token', 400
    else:
        return 'No code provided', 400

if __name__ == '__main__':
    app.run(port=5001, debug=True)