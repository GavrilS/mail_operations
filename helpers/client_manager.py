'''
Manager class that determines what is the proper client class to use based on the email 
server.
'''
from clients.imap import IMAPClient
from clients.pop import PopClient

EMAIL_CLIENTS = {
    'gmail.com': 'imap',
    'abv.bg': 'pop'
}


def get_client(config):
    if 'gmail' in config['server']:
        return IMAPClient(config)
    elif 'abv' in config['server']:
        return PopClient(config)
    else:
        print(f"The server {config['server']} is not currently supported!")
        return None
