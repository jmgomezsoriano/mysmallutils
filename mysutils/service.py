import re
from mysutils.text import URL_PATTERN


def endpoint(service: str = '', embedded: bool = False) -> str:
    """ Obtain the final URL to the service dynamically from a request.

    :param service: The path to the services to join with the request base.
    :param embedded: True if the URL is embedded in a html attribute, otherwise False.
    :return: A string with the URL.
    """
    if embedded:
        return f'javascript:window.location.href = window.location.href.replace(/\\/[^\\/]*$/, \'{service}\');'
    return f'<script>document.write(window.location.href.replace(/\\/[^\\/]*$/, \'{service}\'));</script>'


def is_embedded_url(text: str, start: int, end: int) -> bool:
    """ Detect if a URL is embedded in a HTML tag attribute or not.

    :param text: A text that represents the HTML file.
    :param start: The initial start position of the URL.
    :param end: The final end position of the URL.
    :return: True if the URL is embedded in a HTML tag attribute, otherwise False.
    """
    if start == 0 or end >= len(text) - 2:
        return False
    return bool(re.match(r'.*<[^>]+ [\w]+="$', text[:start], re.DOTALL)) and text[end] == '"' or \
        bool(re.match(r'.*<[^>]+ [\w]+=\'$', text[:start], re.DOTALL)) and text[end] == '\''


def replace_endpoint(text: str, path: str) -> str:
    """ Replace an endpoint.

    :param text: The text that represents the HTML content.
    :param path: The endpoint path.
    :return: Returns the same HTML content but with the URL replaced with the real URL.
    """
    matches = list(re.finditer(URL_PATTERN + path, text))
    matches.reverse()
    for match in matches:
        start, end = match.span()[0], match.span()[1]
        text = text[:start] + endpoint(path, is_embedded_url(text, start, end))  + text[end:]
    return text
