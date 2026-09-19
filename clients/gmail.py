
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
LABELS = ['INBOX']

class GmailClient:

    def __init__(self, token_file=None, creds_file=None):
        self._set_token_file(token_file)
        self._set_creds_file(creds_file)
        self._load_creds()

    def _set_token_file(self, token_file):
        if not token_file:
            raise Exception('Token file is needed!')

        self.token_file = token_file

    def _set_creds_file(self, creds_file):
        if not creds_file:
            raise Exception('Credentials file is needed!')

        self.creds_file = creds_file

    def _load_creds(self):
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_file(self.token_file, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_file, 'w') as f:
                f.write(creds.to_json())

        self.creds = creds

    def list_emails(self):
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            results = (
                service.users().messages().list(userId='me', labelIds=LABELS).execute()
            )

            return results
        except HttpError as e:
            print(f"An error occurred: {e}")
