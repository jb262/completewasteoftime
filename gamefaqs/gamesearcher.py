'''
This module contains functions to perform a search for a game on gamefaqs.
'''

def parse_search_results(bs):
    '''
    Parses a given search result page and returns a list with the first 20 search results.

    :param bs: BeautifulSoup object containing the search page with its results.
    
    :raise StopIteration: If the search page contains an error element, there were no further games found,
    signaling the iterator that calls this method that the end of the Iteration has been reached.
    '''
    search_result = list()

    if bs.find('div', class_='error'):
        raise StopIteration('No further games found.')

    result_titles = bs.find_all('div', class_='sr_title')
    result_details = bs.find_all('div', class_='sr_details')

    for title, details in zip(result_titles, result_details):
        direct_link = title.find(
            'a', class_='sevent', href=True)
        basic_info = title.find('div', class_='sr_info').text.split(',')

        try:
            year = basic_info[-1].strip()
        except IndexError:
            year = None

        try:
            genre = basic_info[-2].strip()
        except IndexError:
            genre = None

        try:
            company = ','.join(basic_info[:-2])
        except IndexError:
            company = None
                
        consoles = list()
        for console in details.find_all('div', class_='sr_product_name'):
            consoles.append(
                {'Name': console.text,
                    'Link': console.contents[0]['href']})
                    
        search_result.append({
            'Name': direct_link.text,
            'Link': direct_link['href'],
            'Genre': genre,
            'Company': company.strip(),
            'Year': year,
            'Consoles': consoles})

    return search_result
