from urllib.parse import urlparse
from flask import Request


def request_base(request: Request, service: str = '') -> str:
    """ Obtain the final URL to the service dynamically from a request.

    :param request: The request to obtain the URL.
    :param service: The path to the services to join with the request base.
    :return: A string with the URL.
    """
    uri = urlparse(request.base_url)
    path = request.environ['HTTP_X_ENVOY_ORIGINAL_PATH'] if 'HTTP_X_ENVOY_ORIGINAL_PATH' in request.environ else ''
    if path.endswith('/') and service.startswith('/'):
        path += service[1:]
    elif not path.endswith('/') and not service.startswith('/'):
        path += '/' + service
    else:
        path += service
    return f'{uri.scheme}://{uri.hostname}' + (f':{uri.port}' if uri.port else '') + f'{path}'
