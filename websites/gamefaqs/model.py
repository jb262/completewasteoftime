'''
This model conatins the implementation of the GameFAQs website model,
including relevant methods to search a game and retrieve information about it.
'''

import re
from helper import helper
from websites.gamefaqs import gamesearcher, gameparser
from websites.model import Website
from websites import decorators
from bs4 import BeautifulSoup


class GameFAQs(Website):
    '''
    Class to connect to gamefaqs.com and provide basic information about video games.
    '''
    def __init__(self, headers=None):
        '''
        Initializes a GameFAQs instance.

        :param headers: Requests headers. If none is provided, the standard headers will be used, causing a 403.
        '''
        super(GameFAQs, self).__init__(headers=headers)
        self.url = 'http://www.gamefaqs.com'
        self.pages = {
            'base': '/',
            'advanced': '/data',
            'questions_answered': '/answers/answered',
            'questions_unresolved': '/answers/unresolved'
            }

    def gamesession(self, path, base=True, advanced=True, questions_answered=False, questions_unresolved=False):
        '''
        Executes the requests for the base and advanced info pages and stores the response in instance variables.

        :param base: If true, the request for the base info class will be executed, if false, not.
        :param advanced: If true, the request for the advanced info class will be executed, if false, not.
        '''
        super(GameFAQs, self).gamesession(
            path,
            base=base,
            advanced=advanced,
            questions_answered=questions_answered,
            questions_unresolved=questions_unresolved)

    def close(self):
        '''
        Closes all open requests.
        '''
        super(GameFAQs, self).close()

    def get_full_game_info(self):
        '''
        Returns both base and advanced info on the game.
        '''
        result = dict()
        
        result['Base-Info'] = self.get_full_base_info()
        result['Advanced-Info'] = self.get_full_advanced_info()

        return result
    
    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.BASE)
    def get_full_base_info(self):
        '''
        Returns the full base info on the game.
        '''
        return gameparser.get_full_base_info

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ADVANCED)
    def get_full_advanced_info(self):
        '''
        Returns the full advanced info on the game.
        '''
        return gameparser.get_advanced_info

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.BASE)
    def get_description(self):
        '''
        Returns the description of the game.
        '''
        return gameparser.get_description

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.BASE)
    def get_base_info(self):
        '''
        Returns platforms, developer, release date of the game
        and franchise, ESRB rating and Metacritc score if available.
        '''
        return gameparser.get_base_info

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.BASE)
    def get_user_ratings(self):
        '''
        Returns user statistic of the game: owned, rating, difficulty, length, completed.
        '''
        return gameparser.get_user_ratings

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ADVANCED)
    def get_title_info(self):
        '''
        Returns title info of the game, may vary.

        Examples: Tales of Berseria: genre, developer, multiplayer, Wiki
        The Sims: genre, developer, ESRB-descriptors, Wiki
        '''
        return gameparser.get_title_info

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ADVANCED)
    def get_versions(self):
        '''
        Returns versions of the game, including region, publisher, product ID, barcode, release date, rating if provided.
        '''
        return gameparser.get_versions

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ADVANCED)
    def get_dlc(self):
        '''
        Returns name and GameFAQs-link of all Add-Ons/DLCs
        '''
        return gameparser.get_dlc

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.QUESTIONS_ANSWERED)
    def get_answered_questions(self):
        '''
        Returns all answered questions sorted by topic, including link and answer count.
        '''
        return gameparser.get_questions

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.QUESTIONS_UNRESOLVED)
    def get_unresolved_questions(self):
        '''
        Returns all unresolved questions sorted by topic, including link and answer count.
        '''
        return gameparser.get_questions

    def get_all_questions(self):
        '''
        Returns all questions, both answered and unanswered ones.
        '''
        return {
            'Answered': self.get_answered_questions(),
            'Unresolved': self.get_unresolved_questions()}

    def get_answers(self, answer_link):
        '''
        Returns answers to a question given its link. The answers include their up- and downvotes.
        
        :param answer_link: Link to the question´s details page.
        '''
        self.response_answers = helper.get_response(
            f'{self.url}{answer_link}', self.headers)

        @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ANSWERS)
        def __get_answers(self, instance):
            return gameparser.get_question_details

        return __get_answers(self, self)

    def search_game(self, game, max_pages=1):
        '''
        Searches a game on GameFAQs and returns a generator with the next 20 search results.
        If None is found, the method gamesearcher.parse_search_results raises a StopIteration error,
        making this event equal to reaching the end of the iterator.

        :param game: String containing the name of the game to be searched.
        :param max_pages: Number of maximum pages in the search result.
        '''

        @decorators.gamesearchdecorator(decorators.Parameters.GameFAQs.SEARCH_URL)
        def search(self, game, max_pages):
            return gamesearcher.parse_search_results
        return search(self, game=game, max_pages=max_pages)