def endpoint(service: str = '') -> str:
    """ Obtain the final URL to the service dynamically from a request.

    :param request: The request to obtain the URL.
    :param service: The path to the services to join with the request base.
    :return: A string with the URL.
    """
    base_url = '<script>document.write(window.location.href.replace(/\\/$/, ""));</script>'
    return base_url + service if service.startswith('/') else base_url + '/' + service
