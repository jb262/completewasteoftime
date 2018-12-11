'''
This module contains decorators.
'''

from bs4 import BeautifulSoup


def gameinfodecorator(info_page):
    '''
    Decorator to validate the request and perform data retrieval on the base and advanced info pages.

    The wrapper simply checks, if the request executed successfully (status code 200). If so, a BeautifulSoup
    instance for its response is created and the actual get-method executed. If not, an error is raised.
    If the request for the respective info page is None, it also raises an error.

    :param info_page: Specifies, if the base or the advanced info page shall be used for the request.

    :raise RuntimeError: If there is no request for the specified info page or the request failed, a RuntimeError will be raised.
    '''
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