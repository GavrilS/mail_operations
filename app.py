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
        client.process_messages(options=config, dto_creator=create_email_dto)
        print('Client: ', client)
        print('*'*100)



if __name__=='__main__':
 
    main()