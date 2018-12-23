'''
This module contains decorators and a parameter class for them.
'''

import re
import itertools
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


def allgamesdecorator(console):
    '''
    Decorator to retrieve all games for a given console, including gamefaqs links.

    :param console: Platform, for which all games should be retrieved.
    :raise RuntimeError: If the request for the `all-games-page` fails, a RuntimeError will be raised,
    returning the error code of the failed request.
    :raise RuntimeError: If the games lst is empty, a RuntimeError will be raised, telling the user that 
    no games for the specified console were found.
    '''
    def get_allgamesdecorator(func):
        def wrapper(*args):
            games = list()
            page = 0
            for _ in itertools.repeat(None):
                url = Parameters.GameFAQs.ALL_GAMES.format(
                    args[0].url, console, page)
                response = helper.get_response(url, args[0].headers)

                if response.status_code == 200:
                    bs = BeautifulSoup(response.text, 'html.parser')
                    
                    found_games = func(*args)(bs)

                    if len(found_games) == 0:
                        break
                    else:
                        games += found_games
                        page += 1
                else:
                    response.close()
                    raise RuntimeError(f'Request failed with status code {response.status_code}.')
            if len(games) == 0:
                raise RuntimeError(f'No games for \'{console}\' found.')
            return games
        return wrapper
    return get_allgamesdecorator

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
        ALL_GAMES = '{}/{}/category/999-all?page={}'

    class Gamerankings:
        '''
        Parameter class for Gamerankings
        '''
        OVERVIEW = 'response_overview'
        SEARCH_URL = '{}/browse.html?search={}&numrev=3&page={}'