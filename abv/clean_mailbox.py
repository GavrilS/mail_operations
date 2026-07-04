'''
This script is handling connecting to an abv.bg mail box, retrieving X number of emails and 
archiving them.

Functionality:
    - connect to email box
    - retrieve assigned number of messages
    - save them for future analysis
    - archive the messages in the mail box
'''
import os
import poplib


POP_CLIENT_DEFAULTS = {
    'user': os.getenv('ABV_USER'),
    'password': os.getenv('ABV_PASSWORD'),
    'server': os.getenv('ABV_POP_SERVER'),
    'port': os.getenv('ABV_POP_PORT'),
    'connection_type': 'pop'
}

class ABVClient:

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
        self.client = poplib.POP3_SSL(self.user, self.port)

    def retrieve_messages(self, num_messages=10):
        print(self.client.list())


if __name__=='__main__':
    client = ABVClient(client_args=POP_CLIENT_DEFAULTS)
    client.retrieve_messages()
