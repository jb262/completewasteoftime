'''
This module conatins the abstract parent class for all website
model classes, which contains skeleton implementations of the
__init__, gamesession and close methods.
'''

from abc import ABC, abstractmethod
from helper import helper


class Website(ABC):
    '''
    Template class for implementing new gaming website models.
    '''
    @abstractmethod
    def __init__(self, headers=None):
        '''
        Initializes an object of the Website class.
    
        :param headers: Dictionary, containing the key User-Agent.
        '''
        self.headers = headers


    @abstractmethod
    def gamesession(self, path, **kwargs):
        '''
        Sets up the responses for the specified info pages. If a parameter is set to true, a request
        for the corresponding url will be executed. This url must be stored in a dictionary called pages
        inside the implementing class with a key identical to the specified parameter. The corresponding
        value inside that dictionary must be the url. The following assumption is made: The url to be
        request is of the form {url of the website}{game specific path}{url of the info page, identical
        for all games}.

        :param path: Path to the game specific url.
        '''
        for key, value in kwargs.items():
            page = self.pages[key]
            response = helper.get_response(f'{self.url}{path}{page}', self.headers)
            setattr(self, f'response_{key}', response if value else None)

    @abstractmethod
    def close(self):
        '''
        Closes all open requests.
        '''
        for page in self.pages.keys():
            response = getattr(self, f'response_{page}')
            if response:
                response.close()
