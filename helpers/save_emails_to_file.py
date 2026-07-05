'''
This helper script takes email data and saves it to file. The email data is in the form of 
a mail_dto object.
'''
import os
from pathlib import Path

def save_email_data_to_file(path, filename, email_dto):
    '''
    The function takes a directory path, a filename and an email_dto as arguments. If the 
    path doesn't exists it will raise an exception. If the path exists it will look for the 
    file. It will open it in 'append' mode if it exists or it will create it if it doesn't 
    exists. It will then write the email_dto data to the file and add a new line at the end, 
    to be ready for the next entry. Upon completion it will return 
    '''
    path_obj = Path(path)
    if not path_obj.exists() or not path_obj.is_dir():
        raise Exception(f"The directory '{path}' doesn't exists!")

    with open(f"{path}/{filename}", 'a') as f:
        f.write(str(email_dto))
        f.write('\n')
    
    return 'Successfully saved the email data.'
