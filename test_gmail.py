from clients.gmail import GmailClient

TOKEN_FILE = 'client_artefacts/gmail/token.json'
CREDENTIALS_FILE = 'client_artefacts/gmail/credentials.json'

client = GmailClient(token_file=TOKEN_FILE, creds_file=CREDENTIALS_FILE)

res = client.list_emails()

messages = res.get('messages', [])

for message in messages:
    print('Message ID: ', message['id'])
    print(message)
    print('='*100)

print('Number of messages found: ', len(messages))
print('Result size estimate: ', res.get('resultSizeEstimate'))
print('Next page token: ', res.get('nextPageToken'))
