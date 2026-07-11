'''
Runs a backup and clear of a mail box.
'''
from helpers.save_emails_to_file import save_email_data_to_file
from clients.pop import PopClient, POP_CLIENT_DEFAULTS

ABV_MAIL_BACKUP_DIR = 'backup'
ABV_MAIL_BACKUP_FILE = 'abv_file'
MAIL_SAVED_SUCCESS_MSG = 'Successfully saved the email data.'
NUM_MESSAGES_TO_PROCESS = 1



def main():
    client = PopClient(client_args=POP_CLIENT_DEFAULTS)
    # messages = client.process_messages(retrieve=True, delete=False)
    # messages = client.process_messages(retrieve=True, delete=True)
    messages = client.process_messages(retrieve=False, delete=False, check_messages=True)
    
    for message in messages:
        print('Message: ', message)
        print('_'*100)



if __name__=='__main__':
 
    main()