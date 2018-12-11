# completewasteoftime
A basic parser for http://www.gamefaqs.com

## Required Python packages
* bs4
* requests

## Purpose
This parser is only meant to perform human-like searches and requests on http://www.gamefaqs.com for retrieving information about your favourite video games.
Its intent is to scrape basic information of a video game from http://www.gamefaqs.com, including description, release date, genre, developer, Metacritic score, and more.

## Usage
After including the files into your project, two base operations can be executed:
* Search a game by its name.
* Parse provided information about the game, given the link to its base info page.

To to so, following steps must be executed:
* Instantiate an object of the type GameFAQs. For the following requests to succeed, a header dictionary with the key 'User-Agent' must be specified. Example: ```gf = GameFAQs(headers={'User-Agent': 'The Spanish Inquisition'})```
* To perform a search, generator mus be created by assigning the instantiated object's ```search_game(name)```-method to it. Example ```search_generator = gf._search_game('Monty Python\s Complete Waste of Time')```.
* To retrieve the next max. 20 search results, access the generators next items. Example: ```search_result = next(search_generator)```.
* The ```search_result```contains a list of those max. 20 search results, which themselves are dictionaries with the keys ```'Name', 'Link', 'Genre', 'Company', 'Year', 'Consoles'```. The ```'Consoles'``` item itself is a dictionary with the keys ```'Name', 'Link'```, containing the name of the system the game is on and the direct link to the system's version of the game.
* By providing a link, ideally retrieved from the ```search_result```, the game information can be accessed. Before doing so, the requests for the base and/or advanced info page must be prepared and executed. This is the job of the ```gamesession(link, base, advanced)```-method of the GameFAQs-instance. By setting the base or advanced parameter to False, the base respectively the advanced info page won't be requested and cannot be parsed afterwards. Example: ```gf.gamesession(link, base=True, advanced=True)```
* Now, the data can be accessed. The following methods of the GameFAQs instance can be used:
  * ```get_name()```: returns the name of the game (base/advanced)
  * ```get_description()```: returns the description of the game (base)
  * ```get_user_ratings()```: returns user ratings of the game (owned by, difficulty, etc.) (base)
  * ```get_base_info()```: returns platforms, developer, release date and - if provided - franchise, ESRB rating and Metacritic score (base)
  * ```get_full_base_info()```: returns all of the above having a base-tag
  * ```get_title_info()```: returns title info of the game, varies from game to game (advanced) (Example: multiplayers, full genre, Wikipedia link, ...)
  * ```get_versions()```: returns different versions of the game with region, publisher, product ID, barcode, release date and rating (advanced)
  * ```get_dlc()```: returns the names and gamefaqs-links to the games add-ons (advanced)
  * ```get_full_advanced_info()```: returns all of the above having an advanced-tag
  * ```get_full_game_info()```: returns all the information mentioned above
* To close the requests, call the ```close()```-method of the GameFAQs instance. Example: ```gf.close()```
