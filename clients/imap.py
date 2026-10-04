'''
This module is handling connecting to a mail box with imap, retrieving X number of emails 
and archiving them.

Functionality:
    - connect to email box
    - retrieve assigned number of messages
    - save them for future analysis
    - archive the messages in the mail box
'''
from imapclient import IMAPClient
from clients.basic_client import BasicClient

DEFAULT_FOLDER = 'INBOX'


class ImapHandler(BasicClient):

    def __init__(self, client_args=None):
        self.cls_name = self.__class__.__name__
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

    def process_messages(self, options=None, dto_creator=None):
        '''
        Main class method to handle the operations the user wants. For the Imap client the 
        options dictionary includes:
            - fetch_messages -> retrieves the message data for the specified number of the 
            oldest messages
            - delete_messages -> deletes the specified number of the oldest messages
            - list_folders -> prints the structure of the email box folders
            - trash_folder -> folder in the email box where to copy messages to be deleted
            - max_messages -> the specified number of messages to process
        All options are False by default, except for 'max_messages' which is 1 by default.
        The last parameter is a function creating an email dto to carry the data from the 
        different clients in a standard format.
        '''
        messages = []
        
        if not options or not dto_creator:
            print('Cannot process any emails, because the required options/mail data container are not provided!')

        else:
            with IMAPClient(self.server, ssl=True) as client:
                client.login(self.email, self.password)
                client.select_folder(DEFAULT_FOLDER)

                message_ids = self._get_message_ids(client, int(options.get('max_messages', 1)))

                if options.get('fetch_messages', False):
                    print('Fetching full messages')
                    messages = self._fetch_messages(client, message_ids, dto_creator)

                if options.get('delete_messages', False):
                    print('Deleting messages. Trash folder - ', options.get('trash_folder', ''))
                    self._delete_messages(client, message_ids, options.get('trash_folder', ''))

                if options.get('list_folders', False):
                    self._list_folders()

        return messages

    def _get_message_ids(self, client, max_messages=1):
        messages = []

        all_msg_ids = client.search(['ALL'])
        # print('All msg ids: ', all_msg_ids)

        oldest_ids = all_msg_ids[:max_messages]
        print('Message ids: ', oldest_ids)
        return oldest_ids

    def _fetch_messages(self, client, message_ids, dto_creator):
        response = client.fetch(message_ids, ['ENVELOPE'])
        messages = []
        
        for msg_id, data in response.items():
            envelope = data[b'ENVELOPE']
            messages.append(
                dto_creator(
                    subject=envelope.subject.decode() if envelope.subject else "No Subject",
                    date=envelope.date,
                    sender=envelope.sender,
                    receiver=envelope.to,
                    message_id=msg_id
                )
            )
            # print('envelope: ', envelope)
            # print('*'*100)
        
        return messages

    def _delete_messages(self, client, message_ids, trash_folder):
        if trash_folder:
            client.copy(message_ids, trash_folder)
        client.delete_messages(message_ids)
        client.expunge()

    def _list_folders(self):
        with IMAPClient(self.server, ssl=True) as client:
            client.login(self.email, self.password)
            for flags, delimeter, name in client.list_folders():
                print(flags, delimeter, name)
