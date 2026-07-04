'''
This module takes extracted email information and wraps it in an object to pass between 
different layers/operations.

Required fields:
    - date - when the email was sent
    - receiver - to whom was the email addressed
    - sender - from who was the email sent
    - subject - the subject of the email
'''

class EmailDTO:

    def __init__(self,date=None,receiver=None,sender=None,subject=None):
        self.date = date
        self.receiver = receiver
        self.sender = sender
        self.subject = subject

    @property
    def date(self):
        return self.__date
    
    @date.setter
    def date(self, date):
        if not date:
            raise Exception('Date must be set!')
        self.__date = date
    
    @property
    def receiver(self):
        return self.__receiver
    
    @receiver.setter
    def receiver(self, receiver):
        if not receiver:
            raise Exception('Receiver must be set!')
        self.__receiver = receiver

    @property
    def sender(self):
        return self.__sender
    
    @sender.setter
    def sender(self, sender):
        if not sender:
            raise Exception('Sender must be set!')
        self.__sender = sender

    @property
    def subject(self):
        return self.__subject
    
    @subject.setter
    def subject(self, subject):
        if not subject:
            raise Exception('Subject must be set!')
        self.__subject = subject
