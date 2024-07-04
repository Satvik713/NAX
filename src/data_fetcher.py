from flask import Flask, redirect, url_for, session, request, render_template
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import google.oauth2.credentials
import os

app = Flask(__name__)
app.secret_key = '-----'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow OAuthlib to work in an insecure transport environment (we will need to do something about this later)

CLIENT_SECRETS_FILE = "/home/satvik/nax/NAX/src/client_secret_994006796738-jphfs21bme59t9pidkuqj7qfkj5r7j9m.apps.googleusercontent.com.json"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] # provides read only access of the gmail account 

@app.route('/')
def index():
    return render_template('index.html')  # we will change this later to the actual template 

@app.route('/authorize')
def authorize():
    """
    Initiates the OAuth 2.0 authorization flow.
    Redirects the user to the Google authorization URL.
    """
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES) # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow steps
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    
    print(f"Redirect URI: {flow.redirect_uri}")  
    
    authorization_url, state = flow.authorization_url(access_type='offline')
    session['state'] = state # Store the state in the session bcoz we will use it later during the callback
    
    print(f"Authorization URL: {authorization_url}") 
    
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    """
    Handles the callback from the OAuth 2.0 server.
    Fetches the access token and stores credentials in the session.
    """
    state = session['state']
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials) 
    
    # Redirect to the processing function
    return redirect(url_for('process_emails'))

def credentials_to_dict(credentials):
    """
    Converts credentials object to a dictionary for storing in the session.
    """
    return {
        'token': credentials.token, 
        'refresh_token': credentials.refresh_token, 
        'token_uri': credentials.token_uri, 
        'client_id': credentials.client_id, 
        'client_secret': credentials.client_secret, 
        'scopes': credentials.scopes
    }

def dict_to_credentials(credentials_dict):
    """
    Converts the credentials dictionary back to a credentials object.
    """
    return google.oauth2.credentials.Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict['refresh_token'],
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )

@app.route('/process_emails')
def process_emails():
    """
    Fetches and processes e-commerce related emails from the user's Gmail account.
    """
    if 'credentials' not in session:
        return redirect('authorize')

    credentials = dict_to_credentials(session['credentials'])
    service = build('gmail', 'v1', credentials=credentials)

    results = service.users().messages().list(userId='me', q='subject:order OR subject:purchase').execute()
    messages = results.get('messages', [])

    email_contents = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        snippet = msg['snippet']
        email_contents.append(snippet)

    return render_template('emails.html', email_contents=email_contents)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
