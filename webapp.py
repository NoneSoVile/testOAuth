from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Replace these with your actual client ID, client secret, and redirect URI
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://localhost:5000/callback'
AUTHORIZATION_SERVER_TOKEN_ENDPOINT = 'https://localhost:8000/token'

@app.route('/')
def home():
    # Redirect user to authorization server for authentication
    return redirect('https://localhost:8000/auth?response_type=code&client_id=' + CLIENT_ID + '&redirect_uri=' + REDIRECT_URI)

@app.route('/callback')
def callback():
    # User will be redirected back to this route with 'code' in query params
    auth_code = request.args.get('code')
    print(f'auth_code: {auth_code}')

    # Exchange the authorization code for an access token
    token_exchange_response = requests.post(AUTHORIZATION_SERVER_TOKEN_ENDPOINT, data={
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })

    if token_exchange_response.ok:
        access_token = token_exchange_response.json().get('access_token')
        # Use the access token to make authenticated requests to the resource server
        return f'Access Token: {access_token}'
    else:
        return 'Failed to retrieve access token', 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)