'''
This model conatins the implementation of the Gamerankings website model,
including relevant methods to search a game and retrieve information about it.
'''

import re
from websites.gamerankings import gamesearcher, reviewparser
from websites.model import Website
from websites import decorators
from helper import helper
from bs4 import BeautifulSoup


class Gamerankings(Website):
    '''
    Class to connect to gamerankings.com and provide review information about video games.
    '''
    def __init__(self, headers=None):
        '''
        Initializes an instance of a Gamerankings object.

        :param headers: Dictionary containing header information to be passed to the request.
        '''
        super(Gamerankings, self).__init__(headers=headers)
        self.url = 'http://www.gamerankings.com'
        self.pages = {
            'reviews': '/articles.html'}
        
    def gamesession(self, path, reviews=True):
        '''
        Enables parsing the review page of a game by executing a request for its review page.

        :param path: Path to the game specific base info page.
        :param reviews: True, if the review page should be parsable, else false.
        '''
        super(Gamerankings, self).gamesession(path, reviews=reviews)

    def close(self):
        '''
        Closes all open requests.
        '''
        super(Gamerankings, self).close()

    @decorators.gameinfodecorator(decorators.Parameters.Gamerankings.OVERVIEW)
    def get_reviews(self):
        '''
        Returns the reviewing medium, the reviewer specific rating, a normalized rating
        on the scale 0-100%, the date of the review and the link to the review if provided.
        '''
        return reviewparser.get_rankings

    def search_game(self, game, max_pages=1):
        '''
        Returns a generator providing the next 50 search results for a given search string.

        :param game: Name of the game to be searched for.
        :param max_pages: Maximum number of pages to be yielded by the generator.
        '''
        @decorators.gamesearchdecorator(decorators.Parameters.Gamerankings.SEARCH_URL)
        def search(self, game, max_pages):
            return gamesearcher.parse_search_results
        return search(self, game=game, max_pages=max_pages)