import requests
from bs4 import BeautifulSoup

def get_response(url, headers=None):
    if headers:
        return requests.get(url, headers=headers)
    else:
        return requests.get(url)

def gameinfodecorator(info_page):
    def get_infodecorator(func):
        def wrapper(*args):
            result = dict()
            if info_page.lower() == 'base':
                response = args[0].response_base
            elif info_page.lower() == 'advanced':
                response = args[0].response_advanced
            else:
                response = None

            if not response:
                raise RuntimeError(f'No response from the {info_page.lower()} info request received.')

            if response.status_code == 200:
                bs = BeautifulSoup(response.text, 'html.parser')
                result = func(*args)(bs)
            else:
                response.close()
                raise RuntimeError(f'Cannot access {info_page.lower()} info page. The request failed with status code {response.status_code}')

            return result
        return wrapper
    return get_infodecorator