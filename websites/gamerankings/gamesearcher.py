'''
This module contains methods to search for games on gamerankings.com.
'''

import re


def parse_search_results(page):
    '''
    Returns a list of the next 50 search results of a search on gamerankings.com, including platform,
    name, company, year of release, average rating and number of reviews.

    The search results are stored in a table. Unfortunately, no unique ids, classes, etc. are provided,
    there are a lot of manual line breaks and whitespaces. In some single columns there are different
    kinds of information crammed together, e.g. the thir column has the name of the game, the link to
    its page, the developer/publisher and the release year. These pieces of information are separated
    by line breaks and tabs, which makes this much stripping and checking for empty strings neccessary.

    :param page: Search page to parse.

    :raise StopIteration: If no (further) games are found, the page shows a container with the unique class pod,
    storing an error string. If this happens, the generator that class this method is told, that the end of the
    iteration has been reached.
    '''

    results = list()

    error_pod = page.find('div', class_='pod')
    if error_pod:
        if error_pod.text == 'No results were found for your search.':
            raise StopIteration('No further games found.')

    search_results = page.find_all('tr')
    reviews_re = re.compile(r'(\d{1,3}.\d{2}%|n\\a)(\d+)')

    if search_results:
        for search_result in search_results:
            link = search_result.find('a', href=True)
            if link:
                link_text = link['href']

            information = list()
            columns = search_result.find_all('td')
            if columns:
                for column in columns:
                    text = column.text.strip().split('\n')
                    if len(text) > 0:
                        information += [txt.strip() for txt in text if txt.strip() != '']

            console = information[0]
            name = information[1]
            company = information[2][:-6]
            year = information[2][-4:]
            reviews = reviews_re.match(information[3])

            results.append({
                'Name': name,
                'Console': console,
                'Link': link_text,
                'Year': year,
                'Company': company,
                'Rating': reviews.group(1),
                'Reviews': reviews.group(2)})

    return results
