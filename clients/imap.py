import os
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

    def process_messages(self, num_messages=1, fetch_messages=False, delete_messages=False, trash_folder=None):
        with IMAPClient(self.server, ssl=True) as client:
            client.login(self.email, self.password)
            client.select_folder(DEFAULT_FOLDER)

            message_ids = self._get_message_ids(client, num_messages)
            messages = []
            if fetch_messages:
                print('Fetching full messages')
                messages = self._fetch_messages(client, message_ids)

            if delete_messages:
                print('Deleting messages. Trash folder - ', trash_folder)
                self._delete_messages(client, message_ids, trash_folder)

            return messages

    def _get_message_ids(self, client, num_messages=1):
        messages = []

        all_msg_ids = client.search(['ALL'])
        # print('All msg ids: ', all_msg_ids)

        oldest_ids = all_msg_ids[:num_messages]
        print('Message ids: ', oldest_ids)
        return oldest_ids

    def _fetch_messages(self, client, message_ids):
        response = client.fetch(message_ids, ['ENVELOPE'])
        messages = []
        
        for msg_id, data in response.items():
            envelope = data[b'ENVELOPE']
            messages.append({
                'subject': envelope.subject.decode() if envelope.subject else "No Subject",
                'date': envelope.date,
                'sender': envelope.sender,
                'receiver': envelope.to,
                'message_id': msg_id
            })
            # print('envelope: ', envelope)
            # print('*'*100)
        
        return messages

    def _delete_messages(self, client, message_ids, trash_folder):
        if trash_folder:
            client.copy(message_ids, trash_folder)
        client.delete_messages(message_ids)
        client.expunge()

    def list_folders(self):
        with IMAPClient(self.server, ssl=True) as client:
            client.login(self.email, self.password)
            for flags, delimeter, name in client.list_folders():
                print(flags, delimeter, name)
