'''
This module contains all necessary functions to scrape
both base info (description, release date, etc.) and
advanced info (versions, add-ons, etc.) for a video game
provided a BeautifulSoup object containing the corresponding
base/advance data page.
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

    The user ratings are stored in a fieldset having the class mygames_section.
    The title of the single categories is stored in div-containers, conveniently having the class
    subsection-title. Besides the category title, this element also stores the rating itself.
    The votes on which the rating is based is stored in a separate paragraph with the class rate.
    The owned-statistic is the only entry without a corresponding votes-statistic, thus resulting
    in an error, if the text-attribute is accessed. This case is caught by assigning None to the
    votes in this case. There is also a disabled element, which can be accessed by signed in users.
    This element is skipped as it does not contain any relevant info.

    :param base_info_page: BeautifulSoup object containing the base info page.
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
                category, rating = subsection.text.split(':')
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

    This data is stored in a div container at the upper right corner, having the class
    pod_gameinfo. Inside this container is an unordered list. The list itself has a very heterogenic
    structure: The core platform, ESRB rating and Metacritic score have their own unique classes,
    while the other list items do not. The developing/publishing company and, if provided, the number
    of DLCs/Add-Ons do not even have a label in contrast to release date, other platforms and franchise,
    resulting in this long if-elif-statement.
    In case of the ESRB-rating and the Metacritic score, the obtained result sets are passed to dedicated
    parsing methods.

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

    This method simply calls all available operations on the base info page
    and stores the results in a dictionary.

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

    This method simply calls all available perations on the advanced info page
    and stores the results in a dictionary.

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
    The retrieved data can differ from game to game given the data provided.

    Example: Tales of Berseria: Genre, Developer, Local Players, Online Players, Wiki
    The Sims: Genre, Developer, ESRB-Descriptors, Wiki

    The title data is stored in description list, which itself is nested into a
    div-container with the unique class pod-titledata.
    The tags and contents are parsed separately and stored as keys and values in
    a dictionary.

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
    Returns all published versions of the game (region, publisher, product ID, barcode, rating).

    The data is stored in a table without any unique identifiers or classes. The cells in a single
    table row all have unique classes corresponding to their contents, except for the product ID and
    barcode cells sharing the same class. This can be bypassed by the simple rule that all elements
    in the result set with an even index are product IDs and all elements with an odd index are
    barcodes. This rule is valid since, even if there is no product ID or barcode provided,
    parsing returns None as their values, guaranteeing elements at all indexes.

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

    The DLC section is very incomplete. A lot of extensions to the games are missing (example:
    The Sims actually having at least 3,013,553 purchasable add-ons, while only having two according
    to gamefaqs). The data itself is stored in a table with the ID dlc, making the parsing straightforward.

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


def get_questions(questions_page):
    '''
    Returns all asked questions either from the answered questions page or the unresolved questions page including
    link and answer count.

    Both answered and unresolved questions pages have the same structure: The information is stored in a container,
    which holds the questions, the links to the questions and the answer count in tables with the classes qna_table
    separated by topic (e.g. Enemy/Boss Help, Technical Help, etc.). The parsing is then straighforward.

    If one of these sections does not have a header (i.e. a description for the topic), the section is skipped.
    This line of code was only added for the sake of completeness, as this situation should not ever occur.
    '''

    result = list()
    questions = questions_page.find_all('table', class_='qna_table')

    if questions:
        for topics in questions:
            try:
                topic = topics.find('th', class_='question').text
            except AttributeError:
                continue

            topic_dict = {
                'Topic': topic,
                'Questions': list()}

            questions_texts = topics.find_all('a', href=True)
            answer_count = topics.find_all('td', class_='count')

            for question, count in zip(questions_texts, answer_count):
                topic_dict['Questions'].append({
                    'Question': question.text,
                    'Link': question['href'],
                    'Count': int(count.text)})
             
            result.append(topic_dict)

    return result


def get_question_details(details_page):
    '''
    Returns question details (i.e. the full question text) and, if any, its answers including up- and downvotes.

    The container with the left span of the main content has to be selected first, otherwise the aside element
    will be parsed as well, leading to nonsensical results.
    Both questions and answers are stored in containers with the class friend_info. There is no strict separation
    between the question and its answers in the container´s body, both are stored in spans with the class name. The only
    way to distinguish them is to check, if there are any up- or downvotes stored in the container as well.
    '''

    result = dict()
    main_content = details_page.find('div', class_='main_content').find('div', class_='span8')
    details = main_content.find_all('div', class_='friend_info')

    if details:
        answers = list()

        for detail in details:
            full_text = detail.find('span', class_='name').text
            upvotes = detail.find('span', class_='up')
            downvotes = detail.find('span', class_='down')

            if not upvotes or not downvotes:
                result['Full-Question'] = full_text
            else:
                answers.append({
                    'Answer': full_text,
                    'Upvotes': int(upvotes.text),
                    'Downvotes': int(downvotes.text)})

        result['Answers'] = answers

    return result

def __get_metacritic_score(base_info_pod):
    '''
    Returns the average metacritic score and the number of reviews.

    The score itself is stored in a div-container with the unique class score.
    The total count of reviews needs to be retrieved from a link text below, from which
    the actual number has to be extracted using a regular expression.

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

    The ESRB info is stored in a list entry (of the unordered list of base information) with the
    unique class esrb. While hidden behind the logo on the visible website, the actual rating and
    its rating can easily be retrieved by a splitting its content on a -.

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