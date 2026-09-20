import os
import email
from imapclient import IMAPClient

IMAP_CLIENT_DEFAULTS = {
    'email': os.getenv('IMAP_ACC', ''),
    'password': os.getenv('IMAP_PASS', ''),
    'server': os.getenv('IMAP_SERVER', '')
}
DEFAULT_FOLDER = 'INBOX'

class ImapHandler:

    def __init__(self, client_args=IMAP_CLIENT_DEFAULTS):
        self._parse_args(client_args)

    def _parse_args(self, client_args):
        if not client_args.get('email', ''):
            raise Exception('The ImapHandler requires email to be provided in the client settings!')

        if not client_args.get('password', ''):
            raise Exception('The ImapHandler requires password to be provided in the client settings!')

        if not client_args.get('server', ''):
            raise Exception('The ImapHandler requires a server to be provided in the client settings!')

        self.email = client_args['email']
        self.password = client_args['password']
        self.server = client_args['server']

    def get_message_ids(self, num_messages=1):
        with IMAPClient(self.server, ssl=True) as client:
            client.login(self.email, self.password)
            client.select_folder(DEFAULT_FOLDER)

            all_msg_ids = client.search(['ALL'])
            print('All msg ids: ', all_msg_ids)

            oldest_ids = all_msg_ids[:num_messages]
            print('Oldest ids: ', oldest_ids)
            return oldest_ids
