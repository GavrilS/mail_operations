import os
import email
from imapclient import IMAPClient

IMAP_CLIENT_DEFAULTS = {
    'email': os.getenv('GMAIL_ACC', ''),
    'password': os.getenv('GMAIL_APP_PASS', '')
}

class ImapHandler:

    def __init__(self, client_args=IMAP_CLIENT_DEFAULTS):
        self._parse_args(client_args)

    def _parse_args(self, client_args):
        if not client_args.get('email', ''):
            raise Exception('The ImapHandler requires email to be provided in the client settings!')

        if not client_args.get('password', ''):
            raise Exception('The ImapHandler requires password to be provided in the client settings!')

        self.email = client_args['email']
        self.password = client_args['password']
    