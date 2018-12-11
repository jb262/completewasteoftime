'''
This module conatins helper functions for recurring tasks in the main module.
'''

import requests


def get_response(url, headers=None):
    '''
    Performs a request for a given URL with headers if specified.

    :param url: URL to perform the request on.
    :param headers: Header of the request. If none is specified, the standard requests header will be used.
    In this case, the requests will end wit status code 403.
    '''
    if headers:
        return requests.get(url, headers=headers)
    else:
        return requests.get(url)