# from clients.gmail import GmailClient

# TOKEN_FILE = 'client_artefacts/gmail/token.json'
# CREDENTIALS_FILE = 'client_artefacts/gmail/credentials.json'

# client = GmailClient(token_file=TOKEN_FILE, creds_file=CREDENTIALS_FILE)

# res = client.list_emails()

# messages = res.get('messages', [])

# for message in messages:
#     print('Message ID: ', message['id'])
#     print(message)
#     print('='*100)

# print('Number of messages found: ', len(messages))
# print('Result size estimate: ', res.get('resultSizeEstimate'))
# print('Next page token: ', res.get('nextPageToken'))

import os
from clients.imap import ImapHandler

TRASH_FOLDER = '[Gmail]/Bin'

client_args = {
    'email': os.getenv('GMAIL_ACC'),
    'password': os.getenv('GMAIL_APP_PASS'),
    'server': os.getenv('GMAIL_IMAP_SERVER')
}

client = ImapHandler(client_args=client_args)
# client.list_folders()

# messages = client.process_messages()
# messages = client.process_messages(fetch_messages=True)
messages = client.process_messages(fetch_messages=True, delete_messages=True, trash_folder=TRASH_FOLDER)

for message in messages:
    print('Message: ', message)
    print('*'*100)
