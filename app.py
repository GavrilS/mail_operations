'''
Runs a backup and clear of a mail box.
'''
import sys
from helpers.save_emails_to_file import save_email_data_to_file
from helpers.load_configs import ConfigLoader
from helpers.mail_dto import create_email_dto
from clients.client_manager import get_client


def main():
    file_paths = []
    if not len(sys.argv) > 1:
        file_paths = input('File paths for configs were not specified when running the script. You can pass multiple file paths separated by empty space: ').split(' ')
    else:
        for file in sys.argv[1:]:
            file_paths.append(file)

    if not len(file_paths) > 0:
        print('No files were specified - ending execution!')
        return

    print('File paths: ', file_paths)

    config_loader = ConfigLoader()
    configs = config_loader.load_configs(file_paths)

    process_config(configs)


def process_config(configs):

    print('Configs: ', configs)
    for config in configs:
        client = get_client(config)
        print('Client: ', client)
        messages = client.process_messages(options=config, dto_creator=create_email_dto)
        if messages:
            print('There are messages to save!')
            # TODO Add the backup functionality and see what options are there to split the 
            # process messages functionality when there is a delete flag to first back up and 
            # then delete the messages
            # The backup functionality should consist of 2 options - create local backup in 
            # a file and save the email data to a DB
        print('Messages: ', messages)
        print('*'*100)



if __name__=='__main__':
 
    main()