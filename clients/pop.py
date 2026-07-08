'''
This module is handling connecting to an abv.bg mail box, retrieving X number of emails and 
archiving them.

Functionality:
    - connect to email box
    - retrieve assigned number of messages
    - save them for future analysis
    - archive the messages in the mail box
'''
import os
import poplib
from helpers.mail_dto import EmailDTO


POP_CLIENT_DEFAULTS = {
    'user': os.getenv('ABV_USER'),
    'password': os.getenv('ABV_PASSWORD'),
    'server': os.getenv('ABV_POP_SERVER'),
    'port': os.getenv('ABV_POP_PORT'),
    'connection_type': 'pop'
}

LINES_TO_SAVE = {
    'date': 'Date: ',
    'receiver': 'To: ',
    'sender': 'From: ',
    'subject': 'Subject: '
}

class PopClient:

    def __init__(self, client_args=None, *args, **kwargs):
        self._parse_client_args(client_args)
        self._set_connection()

    def _parse_client_args(self, client_args):
        print('Client args: ', client_args)
        if not client_args:
            raise Exception('Missing arguments for setting up ABV mail client!')
        
        if not client_args.get('user', None):
            raise Exception('Missing user name for the ABV mail client!')
        
        if not client_args.get('password', None):
            raise Exception('Missing password for ABV mail client!')
        
        if not client_args.get('server', None):
            raise Exception('Missing server for ABV mail client!')
        
        if not client_args.get('port', None):
            raise Exception('Missing port for ABV mail client!')
        
        self.user = client_args['user']
        self.password = client_args['password']
        self.server = client_args['server']
        self.port = int(client_args['port'])
        self.connection_type = client_args.get('connection_type', 'pop')

    def _set_connection(self):
        if 'pop' in self.connection_type.lower():
            self.client = poplib.POP3_SSL(self.server, self.port)
            self.client.user(self.user)
            self.client.pass_(self.password)
        else:
            raise Exception(f"ABV client does not support connection of type: {self.connection_type}")

    def retrieve_messages(self, num_messages=1):
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
        
        print('Messages to process: ', messages_to_process)
        return messages_to_process
    
    def check_message_format(self, num_messages=1):
        for i in range(num_messages):
            for j in self.client.retr(i+1)[1]:
                print(j)
                print('-'*100)
            print('='*100)
            print('='*100)

    def mark_messages_for_deletion(self, num_messages=1):
        self.client.dele(num_messages)
    
    def quit_connection(self):
        self.client.quit()
