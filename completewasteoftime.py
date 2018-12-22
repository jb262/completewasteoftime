'''
This module contains a basic example on how to use the package.
'''
from websites.gamefaqs.model import GameFAQs
from websites.gamerankings.model import Gamerankings


if __name__ == '__main__':
    '''
    Basic example displaying the description of the game Monty Pythons Complete Waste of Time.
    '''
    gf = GameFAQs(headers={'User-Agent': 'Mozilla/5.0'})
    
    search_generator = gf.search_game('Monty Python\'s Complete Waste of Time')

    search_result = next(search_generator)

    link = search_result[0]['Link']
    name = search_result[0]['Name']

    gf.gamesession(link, advanced=False)  

    print(name)
    print(gf.get_description())

    gf.close()