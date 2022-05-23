def endpoint(service: str = '', embedded: bool = False) -> str:
    """ Obtain the final URL to the service dynamically from a request.

    :param service: The path to the services to join with the request base.
    :param embedded: True if the URL is embedded in a html attribute, otherwise False.
    :return: A string with the URL.
    """
    if embedded:
        return f'javascript:window.location.href.replace(/\\/(#.*)?$/, \'{service}\'));'
    return f'<script>document.write(window.location.href.replace(/\\/(#.*)?$/, \'{service}\'));</script>'
