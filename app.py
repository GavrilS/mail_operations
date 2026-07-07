'''
Runs a backup and clear of a mail box.
'''
from argparse import ArgumentParser
from helpers.save_emails_to_file import save_email_data_to_file
from clients.pop import PopClient, POP_CLIENT_DEFAULTS

ABV_MAIL_BACKUP_DIR = 'backup'
ABV_MAIL_BACKUP_FILE = 'abv_file'



def main():
    client = PopClient(client_args=POP_CLIENT_DEFAULTS)
    messages = client.retrieve_messages()
    # client.check_message_format()
    for message in messages:
        save_email_data_to_file(ABV_MAIL_BACKUP_DIR, ABV_MAIL_BACKUP_FILE, message)
    



if __name__=='__main__':
    # parser = ArgumentParser(description="Specify mail box to process.")
    # parser.add_argument('--mail_box', required=True)
    # args = parser.parse_args()
    # mail_box = args.mail_box

    main()