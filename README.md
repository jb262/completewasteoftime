# completewasteoftime
A basic parser/API for http://www.gamefaqs.com and http://www.gamerankings.com

## Required Python packages
* bs4
* requests

## Purpose
This parser is only meant to perform human-like searches and requests on http://www.gamefaqs.com and http://www.gamerankings.com for retrieving information about your favourite video games.
Its intent is to scrape basic information of a video game from http://www.gamefaqs.com or http://www.gamerankings.com, including description, release date, genre, developer, Metacritic score, and more. Furthermore, it's possible to retrieve the asked questions and, if any, their answers.

## Usage
After including the files into your project, two base operations can be executed:
* Search a game by its name.
* Parse provided information about the game, given the link to its base info page.

To do so, following steps must be executed:
* Instantiate an object of the type GameFAQs. For the following requests to succeed, a header dictionary with the key 'User-Agent' must be specified. Example: ```gf = GameFAQs(headers={'User-Agent': 'The Spanish Inquisition'})```
* To perform a search, a generator must be created by assigning the instantiated object's ```search_game(name)```-method to it. Example ```search_generator = gf.search_game('Monty Python\s Complete Waste of Time')```.
* To retrieve the next max. 20 search results, access the generators next items. Example: ```search_result = next(search_generator)```.
* The ```search_result```contains a list of those max. 20 search results, which themselves are dictionaries with the keys ```'Name', 'Link', 'Genre', 'Company', 'Year', 'Consoles'```. The ```'Consoles'``` item itself is a dictionary with the keys ```'Name', 'Link'```, containing the name of the system the game is on and the direct link to the system's version of the game.
* By providing a link, ideally retrieved from the ```search_result```, the game information can be accessed. Before doing so, the requests for the base and/or advanced info page must be prepared and executed. This is the job of the ```gamesession(link, base, advanced, questions)```-method of the GameFAQs-instance. By setting the base, advanced or questions parameter(s) to False, the base/advanced/questions info page(s) won't be requested and cannot be parsed afterwards. Example: ```gf.gamesession(link, base=True, advanced=True, questions=False)```
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
  * ```get_answered_questions()```: returns answered questions, ordered by topic, including answer count and link to their details pages (questions_answered)
  * ```get_unresolved_questions()```: returns unresolved questions, ordered by topic, including answer count and link to their details pages (questions_unresolved)
  * ```get_all_questions()```: returns all questions, ordered by topic, including answer count and link to their details pages (questions_answered and questions_unresolved)
  * ```get_answers(link)```: returns the full question text and, if any, its answers including up- and downvotes (none required)
  
* To close the requests, call the ```close()```-method of the GameFAQs instance. Example: ```gf.close()```

The steps are completely analogous for http://www.gamerankings.com. The only available method after creating an instance and establishing a gamesession is ```get_reviews()``` which returns all reviewing media, the date of the review, the medium's specific rating, a standardized rating in the range [0%, 100%] and a link to the review.
