'''
Manager class that determines what is the proper client class to use based on the email 
server.
'''

class ClientManager:

    def __init__(self, config):
        self.config = config

    def get_client(self):
        return