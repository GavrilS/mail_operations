'''
This module is handling connecting to a mail box with pop, retrieving X number of emails and 
archiving them.

Functionality:
    - connect to email box
    - retrieve assigned number of messages
    - save them for future analysis
    - archive the messages in the mail box
'''
import poplib
from clients.basic_client import BasicClient


LINES_TO_SAVE = {
    'date': 'Date: ',
    'receiver': 'To: ',
    'sender': 'From: ',
    'subject': 'Subject: '
}

class PopClient(BasicClient):

    def __init__(self, client_args=None, *args, **kwargs):
        self.cls_name = self.__class__.__name__
        self._parse_client_args(client_args)
        self._set_connection()

    def _parse_client_args(self, client_args):
        print('Client args: ', client_args)
        if not client_args:
            raise Exception('Missing arguments for setting up Pop mail client!')
        
        if not client_args.get('email', None):
            raise Exception('Missing email account for the Pop mail client!')
        
        if not client_args.get('password', None):
            raise Exception('Missing password for Pop mail client!')
        
        if not client_args.get('server', None):
            raise Exception('Missing server for Pop mail client!')
        
        if not client_args.get('port', None):
            raise Exception('Missing port for Pop mail client!')
        
        self.email = client_args['email']
        self.password = client_args['password']
        self.server = client_args['server']
        self.port = int(client_args['port'])

    def _set_connection(self):
        self.client = poplib.POP3_SSL(self.server, self.port)
        self.client.user(self.user)
        self.client.pass_(self.password)

    def process_messages(self, options=None, dto_creator=None):
        '''
        Main class method to handle the operations the user wants. For the Pop client the 
        options dictionary includes:
            - fetch_messages -> retrieves the message data for the specified number of the 
            oldest messages
            - delete_messages -> deletes the specified number of the oldest messages
            - check_messages -> prints the message structure of the specified number of 
            messages; better to use with just one or two
            - max_messages -> the specified number of messages to process
        All options are False by default, except for 'max_messages' which is 1 by default.
        The last parameter is a function creating an email dto to carry the data from the 
        different clients in a standard format.
        '''
        
        messages = []

        if not options or not dto_creator:
            print('Cannot process any emails, because the required options/mail data container are not provided!')

        else:
            self._set_connection()

            if options.get('fetch_messages', False):
                messages = self._retrieve_messages(int(options.get('max_messages', 1)), dto_creator)
            
            if options.get('delete_messages', False):
                self._mark_messages_for_deletion(int(options.get('max_messages', 1)))

            if options.get('check_messages', False):
                self._check_message_format(int(options.get('max_messages', 1)))

            self._quit_connection()

        return messages

    def _retrieve_messages(self, max_messages=1, dto_creator=None):
        
        messages_to_process = []
        for i in range(max_messages):
            message = {}
            for j in self.client.retr(i+1)[1]:
                line = j.decode('utf-8')
                for k, v in LINES_TO_SAVE.items():
                    if line.startswith(v):
                        message[k] = line
                        break
            
            messages_to_process.append(
                dto_creator(
                    date=message['date'],
                    receiver=message['receiver'],
                    sender=message['sender'],
                    subject=message['subject']
                )
            )
        
        return messages_to_process
    
    def _check_message_format(self, max_messages=1):
        for i in range(max_messages):
            for j in self.client.retr(i+1)[1]:
                print(j)
                print('-'*100)
            print('='*100)
            print('='*100)

    def _mark_messages_for_deletion(self, max_messages=1):
        self.client.dele(max_messages)
    
    def _quit_connection(self):
        self.client.quit()
        self.client = None
