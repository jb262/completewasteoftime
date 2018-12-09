import re
from helper import helper
from gamefaqs import gameparser, gamesearcher
from bs4 import BeautifulSoup


class GameFAQs:
    def __init__(self, headers=None):
        self.url = 'http://www.gamefaqs.com'
        self.headers = headers

    def gamesession(self, path, base=True, advanced=True):
        if base:
            self.response_base = helper.get_response(f'{self.url}{path}', self.headers)
        else:
            self.response_base = None

        if advanced:
            self.response_advanced = helper.get_response(f'{self.url}{path}/data', self.headers)
        else:
            self.response_advanced = None

    def close(self):
        if self.response_base:
            self.response_base.close()

        if self.response_advanced:
            self.response_advanced.close()

    def get_full_game_info(self):
        result = dict()
        
        result['Base-Info'] = self.get_full_base_info()
        result['Advanced-Info'] = self.get_full_advanced_info()

        return result
    
    @helper.gameinfodecorator('base')
    def get_full_base_info(self):
        return gameparser.get_full_base_info

    @helper.gameinfodecorator('advanced')
    def get_full_advanced_info(self):
        return gameparser.get_advanced_info

    @helper.gameinfodecorator('base')
    def get_description(self):
        return gameparser.get_description

    @helper.gameinfodecorator('base')
    def get_base_info(self):
        return gameparser.get_base_info

    @helper.gameinfodecorator('base')
    def get_user_ratings(self):
        return gameparser.get_user_ratings

    @helper.gameinfodecorator('advanced')
    def get_title_info(self):
        return gameparser.get_title_info

    @helper.gameinfodecorator('advanced')
    def get_versions(self):
        return gameparser.get_versions

    @helper.gameinfodecorator('advanced')
    def get_dlc(self):
        return gameparser.get_dlc

    def search_game(self, game, max_pages=1):
        for page in range(max_pages):
            query = re.sub(r'\s', '+', game.strip())
            url = f'{self.url}/search?game={query}&page={page}'

            response = helper.get_response(url,self.headers)

            if response.status_code == 200:
                bs = BeautifulSoup(response.text, 'html.parser')

                yield gamesearcher.parse_search_results(bs)
            else:
                response.close()
                raise RuntimeError(f'GameFAQs search failed with status code {response.status_code}')


if __name__ == '__main__':
    gf = GameFAQs(headers={'User-Agent': 'Mozilla/5.0'})
    search_generator = gf.search_game('Monty Python\'s Complete Waste of Time')
    
    search_result = next(search_generator)

    link = search_result[0]['Link']
    name = search_result[0]['Name']

    gf.gamesession(link)
    print(name)
    print(gf.get_description())

    gf.close()