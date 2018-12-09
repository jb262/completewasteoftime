'''
This module contains functions to perform a search for a game on gamefaqs.
'''

def parse_search_results(bs):
    '''
    Parses a given search result page and returns a list with the first 20 search results.

    The result page of displays the next 20 results of the search. It provides the name of the game
    in a div-container with the unique per row class sr-title, its developer/publisher if known,
    its genre and its release year in a div-container with the unique per row class sr-details, delimited
    by commas. For some obsucre titles, the developer can be blank. It is also possible, that a developer/
    publisher has a comma in its name, so it has to be put together again after splitting the string by
    commas. The release year can also be the string value cancelled, making it not possible to convert
    it to an integer value.
    The link to the core platform can be found in the same element as the game title.
    All platforms and the link to the version of the game for this platform are stored in
    elements with the class sr-product-name. As this includes the core platform, there is
    always at least one of these elements found.

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
