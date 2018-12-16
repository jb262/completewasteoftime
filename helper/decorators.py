'''
This module contains decorators and a parameter class to choose the correct response for the decorator.
'''

from bs4 import BeautifulSoup


def gameinfodecorator(page):
    '''
    Decorator to validate the request and perform data retrieval on the base and advanced info pages.

    The wrapper simply checks, if the request executed successfully (status code 200). If so, a BeautifulSoup
    instance for its response is created and the actual get-method executed. If not, an error is raised.
    If the request for the respective info page is None, it also raises an error.

    :param page: Specifies, which request is to be used.

    :raise RuntimeError: If there is no request for the specified info page or the request failed, a RuntimeError will be raised.
    '''
    def get_infodecorator(func):
        def wrapper(*args):
            result = dict()
            response = getattr(args[0], page)

            if not response:
                raise RuntimeError(f'No response from the {page.lower()} info request received.')

            if response.status_code == 200:
                bs = BeautifulSoup(response.text, 'html.parser')
                result = func(*args)(bs)
            else:
                response.close()
                raise RuntimeError(f'Cannot access {page.lower()} info page. The request failed with status code {response.status_code}')

            return result
        return wrapper
    return get_infodecorator


class Parameters:
    class GameFAQs:
        BASE = 'response_base'
        ADVANCED = 'response_advanced'
        QUESTIONS_ANSWERED = 'response_questions_answered'
        QUESTIONS_UNRESOLVED = 'response_questions_unresolved'
        ANSWERS = 'response_answers'