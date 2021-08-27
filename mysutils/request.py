from json import dumps, loads
from typing import Union

try:
    from requests import post, RequestException
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('ModuleNotFoundError: No module named \'requests\'. '
                              'Please install it with the command:\n\n'
                              'pip install requests~=2.25.1')


def json_post(host: str, msg: Union[list, dict, str]) -> Union[list, dict, str]:
    """ Makes a http json post.
    :param host: The host.
    :param msg: Object to send to the server.
    """
    res = post(host, dumps(msg), headers={'content-type': 'application/json'})
    if not res.ok:
        raise RequestException(f'Error {res.status_code} connecting with "{host}":\n{res.content.decode("utf-8")}')
    return loads(res.content)
