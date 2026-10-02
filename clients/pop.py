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
from helpers.mail_dto import EmailDTO
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

    def process_messages(self, retrieve=True, delete=True, check_messages=False, message_number=1):
        self._set_connection()

        messages = []
        if retrieve:
            messages = self._retrieve_messages(message_number)
        
        if delete:
            self._mark_messages_for_deletion(message_number)

        if check_messages:
            self._check_message_format()

        self._quit_connection()

        return messages

    def _retrieve_messages(self, num_messages=1):
        
        messages_to_process = []
        for i in range(num_messages):
            message = {}
            for j in self.client.retr(i+1)[1]:
                line = j.decode('utf-8')
                for k, v in LINES_TO_SAVE.items():
                    if line.startswith(v):
                        message[k] = line
                        break
            messages_to_process.append(
                EmailDTO(
                    date=message['date'],
                    receiver=message['receiver'],
                    sender=message['sender'],
                    subject=message['subject']
                )
            )
        
        return messages_to_process
    
    def _check_message_format(self, num_messages=1):
        for i in range(num_messages):
            for j in self.client.retr(i+1)[1]:
                print(j)
                print('-'*100)
            print('='*100)
            print('='*100)

    def _mark_messages_for_deletion(self, num_messages=1):
        self.client.dele(num_messages)
    
    def _quit_connection(self):
        self.client.quit()
        self.client = None
