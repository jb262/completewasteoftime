'''
This module contains all necessary functions to scrape
both base info (description, release date, etc.) and
advanced info (versions, add-ons, etc.) for a video game
provided a BeautifulSoup object containing the corresponding
main respectively data page.
'''

import re


def get_name(info_page):
    '''
    Returns the title of the game from both base and advanced info page.

    :param info_page: BeautifulSoup object containing the base/advanced info page
    '''
    return info_page.find('h1', class_='page-title').text


def get_description(base_info_page):
    '''
    Returns the description of the game from the base info page.

    :param base_info_page: BeautifulSoup object containing the baseinfo page
    '''
    return base_info_page.find('div', class_='desc').text


def get_user_ratings(base_info_page):
    '''
    Returns the user ratings (owned, rating, difficulty, length, completed) from the base info page.

    :param base_info_page: BeautifulSoup object containing the base info page
    '''
    result = dict()
    user_ratings_fieldsets = base_info_page.find_all('fieldset', class_='mygames_section')

    if user_ratings_fieldsets:
        categories = list()
        ratings = list()
        votes = list()

        for user_rating_fieldset in user_ratings_fieldsets:
            if not 'disabled' in user_rating_fieldset.attrs:
                subsection = user_rating_fieldset.find('div', class_='subsection-title')
                category, _ = subsection.text.split(':')
                rating = subsection.find('div', class_='rating').text
                try:
                    vote = subsection.find('p', 'rate').text
                except AttributeError:
                    vote = None

                categories.append(category)
                ratings.append(rating)
                votes.append(vote)

        for category, rating, vote in zip(categories, ratings, votes):
            result[category] = {
                'Rating': rating,
                'Votes': vote}

    return result


def get_base_info(base_info_page):
    '''
    Returns the basic info on the game provided on the base info page
    (platforms, developer, release date, genre, franchise, metacritic score, ESRB rating).
    Franchise, ESRB rating and metacritic score can be missing, the latter two especially
    when data of older games is scraped.

    :param base_info_page: BeautifulSoup object containing the base info page
    '''
    result = dict()
    base_info = base_info_page.find('div', class_='pod_gameinfo').find('ul')
        
    if base_info:
        categories = list()
        values = list()

        for info in base_info.find_all('li'):
            if not 'class' in info.attrs:
                contents = info.find('b')
                if contents:
                    category = re.sub(r'\s', '-', contents.text[:-1])
                    value = [val.text for val in info.find_all('a')]
                    if len(value) == 1:
                        value = value[0]
                else:
                    if re.search(r'#dlc', info.find('a')['href']):
                        category = 'DLC'
                    elif re.search(r'/company/', info.find('a')['href']):
                        category = 'Company'
                    value = info.text
                categories.append(category)
            elif 'core-platform' in info['class']:
                categories.append('Core-Platform')
                value = info.text
            elif 'boxshot' in info['class']:
                continue
            elif 'esrb' in info['class']:
                result['ESRB'] = __get_esrb_rating(info)
                continue
            elif 'metacritic' in info['class']:
                result['Metacritic'] = __get_metacritic_score(info)
                continue
            else:
                base_data = info.text.split(':')
                categories.append(base_data[0].strip())
                value = base_data[1].strip()

            values.append(value)

        for category, value in zip(categories, values):
            result[category] = value

    return result


def get_full_base_info(base_info_page):
    '''
    Returns the full base info on the game provided on the base info page
    (base info, description, user ratings, name).

    :param base_info_page: BeautifulSoup object containing the base info page
    '''
    result = get_base_info(base_info_page)
    result['Description'] = get_description(base_info_page)
    result['User-Ratings'] = get_user_ratings(base_info_page)
    result['Name'] = get_name(base_info_page)

    return result


def get_advanced_info(advanced_info_page):
    '''
    Returns the full info on the game provided on the advanced info page.
    (title data, versions, add-ons)

    :param advanced_info_page: BeautifulSoup object containing the advanced info page
    '''
    result = dict()
    
    result['Title-Data'] = get_title_data(advanced_info_page)
    result['Versions'] = get_versions(advanced_info_page)
    result['DLC'] = get_dlc(advanced_info_page)

    return result


def get_title_data(advanced_info_page):
    '''
    Returns the title data of the game provided on the advanced info page
    (developer, genres, ESRB-descriptors, Wikipedia (EN) link, multiplayers, etc. ).
    The retreived data can differ from game to game given on the data provided.

    Example: Tales of Berseria: Genre, Developer, Local Players, Online Players, Wiki
    The Sims: Genre, Developer, ESRB-Descriptors, Wiki

    :param advanced_info_page: BeautifulSoup object containing the advanced info page
    '''
    result = dict()
    title_data = advanced_info_page.find('div', 'pod_titledata')

    if title_data:
        categories = title_data.find_all('dt')
        values = title_data.find_all('dd')

        for category, value in zip(categories, values):
            key = re.sub(r'\s', '-', re.sub(r'[()]', '', category.text))
            value = re.sub(r' >', ',', value.text).split(',')
            if len(value) > 1:
                value = [val.strip() for val in value]
                    
            result[key[:-1]] = value

    return result


def get_versions(advanced_info_page):
    '''
    Returns all published versions of the game (region, publisher, product id, barcode, rating)

    :param advanced_info_page: BeautifulSoup object containing the advanced info page
    '''
    result = list()

    regions = advanced_info_page.find_all('td', class_='cregion')
    publishers = advanced_info_page.find_all('td', class_='datacompany')
    ids = advanced_info_page.find_all('td', class_='datapid')
    product_ids = ids[::2]
    barcodes = ids[1::2]
    release_dates = advanced_info_page.find_all('td', class_='cdate')
    ratings = advanced_info_page.find_all('td', class_='datarating')

    if regions and publishers and product_ids and barcodes and release_dates and ratings:
        for (region, publisher, product_id, barcode, release_date, rating) in zip(
                    regions, publishers, product_ids, barcodes, release_dates, ratings):
            result.append(
                {'Region': region.text.strip(),
                'Publisher': publisher.text.strip(),
                'Product-Id': product_id.text.strip(),
                'Barcode': barcode.text.strip(),
                'Release-Date': release_date.text.strip(),
                'Rating': rating.text.strip()})

    return result


def get_dlc(advance_info_page):
    '''
    Returns all released add-ons/DLCs of the game (name, gamefaqs-link).

    :param advanced_info_page: BeautifulSoup object containing the advanced info page
    '''
    result = list()
    dlcs = advance_info_page.find('div', id='dlc')

    if dlcs:
        for dlc in dlcs.find_all('a', href=True):
            result.append({
                'Name': dlc.text,
                'Link': dlc['href']})
    return result


def __get_metacritic_score(base_info_pod):
    '''
    Returns the average metacritic score and the number of reviews.

    :param base_info_pod: BeautifulSoup object containing the base info box provided in the upper
    right of the base info page.
    '''
    result = dict()
    metacritic = base_info_pod.find('div', class_='review_link')

    if metacritic:
        metacritic_reviews = metacritic.text
           
        try:
            numbers = re.compile(r'\d+')
            metacritic_review_count = int(numbers.findall(metacritic_reviews)[0])
        except IndexError:
            metacritic_review_count = None

        result['Reviews'] = metacritic_review_count

        try:
            metacritic_score = int(base_info_pod.find('div', class_='score').text)
        except AttributeError:
            metacritic_score = None

        result['Score'] = metacritic_score

    return result


def __get_esrb_rating(base_info_pod):
    '''
    Returns the ESRB rating and the description of the rating.

    :param base_info_pod: BeautifulSoup object containing the base info box provided in the upper
    right of the base info page.
    '''
    result = dict()

    if base_info_pod:
        rating, description = base_info_pod.text.split("-")
        rating, description = rating.strip(), description.strip()
        result['Rating'] = rating
        result['Description'] = description

    return result