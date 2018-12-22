'''
This modules parses critic reviews aggregated on http://www.gamerankings.ocm
'''

def get_rankings(page):
    '''
    Returns critic ratings of a game, including the reviewing site, review date, site specific rating,
    standardized rating (i.e. site specific rating scaled to percent according to the reviewing site´s
    rating range) and link to the review.

    The information is store in the body of a regular table, which makes parsing straightforward.
    '''

    result = list()
    review_table = page.find('table', class_='release').find('tbody')

    if review_table:
        articles = review_table.find_all('tr')
        if articles:
            for article in articles:
                rows = article.find_all('td')
                link = rows[2].find('a', href=True)
                result.append({
                    'Site': rows[0].text,
                    'Date': rows[1].text,
                    'Link': link['href'] if link else None,
                    'Site-Rating': link.text if link else rows[2].text,
                    'Ratio': rows[3]})
    return result