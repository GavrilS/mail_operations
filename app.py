'''
Runs a backup and clear of a mail box.
'''
import sys
from helpers.save_emails_to_file import save_email_data_to_file
from helpers.load_configs import ConfigLoader
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

    config_loader = ConfigLoader()

    for file in file_paths:
        process_configs(config_loader, file)


def process_configs(config_loader, file):
    pass




if __name__=='__main__':
 
    main()