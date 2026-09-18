
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

TOKEN_FILE = 'token.json'
CREDS_FILE = 'credentials.json'

class GmailClient:

    def __init__(self):
        self._load_creds()

    def _load_creds():
        creds = None

        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_file(TOKEN_FILE, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDS_FILE, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, 'w') as f:
                f.write(creds.to_json())
