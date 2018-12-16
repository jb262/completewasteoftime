'''
This is the main module of the project containing classes to connect to the websites and providing the data in
a readable format.
'''

import re
from helper import helper, decorators
from websites import gamefaqs
from bs4 import BeautifulSoup


class GameFAQs:
    '''
    Class to connect to gamefaqs.com and provide basic information on video games.
    '''
    def __init__(self, headers=None):
        '''
        Initializes a GameFAQs instance.

        :param headers: Requests headers. If none is provided, the standard headers will be used, causing a 403.
        '''
        self.url = 'http://www.gamefaqs.com'
        self.headers = headers

    def gamesession(self, path, base=True, advanced=True, questions=False):
        '''
        Executes the requests for the base and advanced info pages and stores the response in instance variables.

        :param base: If true, the request for the base info class will be executed, if false, not.
        :param advanced: If true, the request for the advanced info class will be executed, if false, not.
        '''
        if base:
            self.response_base = helper.get_response(f'{self.url}{path}', self.headers)
        else:
            self.response_base = None

        if advanced:
            self.response_advanced = helper.get_response(f'{self.url}{path}/data', self.headers)
        else:
            self.response_advanced = None

        if questions:
            self.response_questions_answered = helper.get_response(f'{self.url}{path}/answers/answered', self.headers)
            self.response_questions_unresolved = helper.get_response(f'{self.url}{path}/answers/unresolved', self.headers)
        else:
            self.response_questions_answered = None
            self.response_questions_unresolved = None

    def close(self):
        '''
        Closes all open requests.
        '''
        if self.response_base:
            self.response_base.close()

        if self.response_advanced:
            self.response_advanced.close()

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
        return gamefaqs.gameparser.get_full_base_info

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ADVANCED)
    def get_full_advanced_info(self):
        '''
        Returns the full advanced info on the game.
        '''
        return gamefaqs.gameparser.get_advanced_info

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.BASE)
    def get_description(self):
        '''
        Returns the description of the game.
        '''
        return gamefaqs.gameparser.get_description

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.BASE)
    def get_base_info(self):
        '''
        Returns platforms, developer, release date of the game
        and franchise, ESRB rating and Metacritc score if available.
        '''
        return gamefaqs.gameparser.get_base_info

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.BASE)
    def get_user_ratings(self):
        '''
        Returns user statistic of the game: owned, rating, difficulty, length, completed.
        '''
        return gamefaqs.gameparser.get_user_ratings

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ADVANCED)
    def get_title_info(self):
        '''
        Returns title info of the game, may vary.

        Examples: Tales of Berseria: genre, developer, multiplayer, Wiki
        The Sims: genre, developer, ESRB-descriptors, Wiki
        '''
        return gamefaqs.gameparser.get_title_info

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ADVANCED)
    def get_versions(self):
        '''
        Returns versions of the game, including region, publisher, product ID, barcode, release date, rating if provided.
        '''
        return gamefaqs.gameparser.get_versions

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ADVANCED)
    def get_dlc(self):
        '''
        Returns name and GameFAQs-link of all Add-Ons/DLCs
        '''
        return gamefaqs.gameparser.get_dlc

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.QUESTIONS_ANSWERED)
    def get_answered_questions(self):
        '''
        Returns all answered questions sorted by topic, including link and answer count.
        '''
        return gamefaqs.gameparser.get_questions

    @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.QUESTIONS_UNRESOLVED)
    def get_unresolved_questions(self):
        '''
        Returns all unresolved questions sorted by topic, including link and answer count.
        '''
        return gamefaqs.gameparser.get_questions

    def get_all_questions(self):
        return {
            'Answered': self.get_answered_questions(),
            'Unresolved': self.get_unresolved_questions()}

    def get_answers(self, answer_link):
        self.response_answers = helper.get_response(
            f'{self.url}{answer_link}', self.headers)

        @decorators.gameinfodecorator(decorators.Parameters.GameFAQs.ANSWERS)
        def __get_answers(self, instance):
            return gamefaqs.gameparser.get_question_details

        return __get_answers(self, self)

    def search_game(self, game, max_pages=1):
        '''
        Searches a game on GameFAQs and returns a generator with the next 20 search results.
        If None is found, the method gamesearcher.parse_search_results raises a StopIteration error,
        making this event equal to reaching the end of the iterator.

        :param game: String containing the name of the game to be searched.
        :param max_pages: Number of maximum pages in the search result.

        :raise RuntimeError: If the request for the search page fails, a Runtime error is raised and the request closed.
        '''
        for page in range(max_pages):
            query = re.sub(r'\s', '+', game.strip())
            url = f'{self.url}/search?game={query}&page={page}'

            response = helper.get_response(url,self.headers)

            if response.status_code == 200:
                bs = BeautifulSoup(response.text, 'html.parser')

                yield gamefaqs.gamesearcher.parse_search_results(bs)
            else:
                response.close()
                raise RuntimeError(f'GameFAQs search failed with status code {response.status_code}')


if __name__ == '__main__':
    '''
    Basic example displaying the description of the game Monty Pythons Complete Waste of Time.
    '''
    gf = GameFAQs(headers={'User-Agent': 'Mozilla/5.0'})
    search_generator = gf.search_game('Monty Python\'s Complete Waste of Time')

    search_result = next(search_generator)

    link = search_result[0]['Link']
    name = search_result[0]['Name']

    gf.gamesession(link, base=False, advanced=False, questions=True)
    print(name)
    print(gf.get_description())

    gf.close()