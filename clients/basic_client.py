'''
Basic client blueprint for the client classes.
'''

class BasicClient:

    def __init__(self):
        self.cls_name = self.__class__.__name__
        self.email = None
        self.server = None

    def __repr__(self):
        return f'{self.cls_name}(server={self.server}; email={self.email})'

    def __str__(self):
        return self.__repr__()
