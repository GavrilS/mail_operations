'''
Basic client blueprint for the client classes.
'''

class BasicClient:

    def __init__(self):
        self.cls_name = self.__class__.__name__

    def __repr__(self):
        return f'{self.cls_name}()'