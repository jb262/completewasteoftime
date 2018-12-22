'''
This module contains decorators and a parameter class for them.
'''

import re
from bs4 import BeautifulSoup
from helper import helper


def gameinfodecorator(page):
    '''
    Decorator to validate the request and perform data retrieval on the base and advanced info pages.

    The wrapper simply checks, if the request executed successfully (status code 200). If so, a BeautifulSoup
    instance for its response is created and the actual get-method executed. If not, an error is raised.
    If the request for the respective info page is None, it also raises an error.

    :param page: Specifies, which request is to be used.

    :raise RuntimeError: If there is no request for the specified info page or the request failed, a RuntimeError will be raised.
    '''
    def get_infodecorator(func):
        def wrapper(*args):
            result = dict()
            response = getattr(args[0], page)

            if not response:
                raise RuntimeError(f'No response from the {page.lower()} info request received.')

            if response.status_code == 200:
                bs = BeautifulSoup(response.text, 'html.parser')
                result = func(*args)(bs)
            else:
                response.close()
                raise RuntimeError(f'Cannot access {page.lower()} info page. The request failed with status code {response.status_code}')

            return result
        return wrapper
    return get_infodecorator


def gamesearchdecorator(url):
    '''
    Decorator to perform the usual steps needed for searching a game, given the template of the
    website´s seearch page url.

    :param url: The website´s template search page url.

    :raise RuntimeError: If the request for the search page fails, a RuntimeError will be raised, showing the status code
    of the failed request.
    '''
    def get_searchdecorator(func):
        def wrapper(*args, **kwargs):
            for page in range(kwargs['max_pages']):
                query = re.sub(r'\s', '+', kwargs['game'].strip())
                search_url = url.format(args[0].url, query, page)
                response = helper.get_response(search_url, args[0].headers)

                if response.status_code == 200:
                    bs = BeautifulSoup(response.text, 'html.parser')

                    yield func(*args, **kwargs)(bs)
                else:
                    response.close()
                    raise RuntimeError(f'Search failed with status code {response.status_code}')
        return wrapper
    return get_searchdecorator


class Parameters:
    '''
    Parameter class, which holds the strings which are passed to the above decorators.
    These parameters are specific to a certain website.
    '''
    class GameFAQs:
        '''
        Parameter class for GameFAQs
        '''
        BASE = 'response_base'
        ADVANCED = 'response_advanced'
        QUESTIONS_ANSWERED = 'response_questions_answered'
        QUESTIONS_UNRESOLVED = 'response_questions_unresolved'
        ANSWERS = 'response_answers'
        SEARCH_URL = '{}/search?game={}&page={}'

    class Gamerankings:
        '''
        Parameter class for Gamerankings
        '''
        OVERVIEW = 'response_overview'
        SEARCH_URL = '{}/browse.html?search={}&numrev=3&page={}'