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

USER = os.getenv('ABV_USER')
PASS = os.getenv('ABV_PASSWORD')
POP_SERVER = os.getenv('ABV_POP_SERVER')
POP_PORT = os.getenv('ABV_POP_PORT')

class ABVConnector:

    def __init__(self):
        pass
