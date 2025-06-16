import functools
from json import dumps, loads
from logging import getLogger
from time import sleep
from typing import Union, Callable
from collections.abc import Container

from deprecation import deprecated

try:
    import requests
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('ModuleNotFoundError: No module named \'requests\'. '
                              'Please install it with the command:\n\n'
                              'pip install requests~=2.25.1')

logger = getLogger(__name__)


@deprecated(deprecated_in='2.0.23', removed_in='2.1.0', current_version='2.0.23')
def json_post(host: str, msg: Union[list, dict, str]) -> Union[list, dict, str]:
    """ Makes a http json post.
    :param host: The host.
    :param msg: Object to send to the server.
    """
    res = requests.post(host, dumps(msg), headers={'content-type': 'application/json'})
    if not res.ok:
        raise requests.RequestException(
            f'Error {res.status_code} connecting with "{host}":\n{res.content.decode("utf-8")}'
        )
    return loads(res.content)


@functools.wraps(requests.get)
def retry_get(
        *args,
        num_tries: int = 5,
        wait_time: float = 30,
        statuses: Container = tuple(),
        exceptions: Exception = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),
        **kwargs
) -> requests.Response:
    """ Wrapper of get request to add tries. The arguments are the same but with the following extra parameters:
    :param num_tries: The number of tries. 0, forever.
    :param wait_time: Time to wait between requests.
    :param statuses: A list of response statuses that force the repetition.
        By default, any status is valid, and it automatically returns the requests.
    :param exceptions: Exceptions that must happen to try again.
    """
    return _retry_request(
        requests.get,
        *args,
        num_tries=num_tries,
        wait_time=wait_time,
        statuses=statuses,
        exceptions=exceptions,
        **kwargs
    )


@functools.wraps(requests.delete)
def retry_delete(
        *args,
        num_tries: int = 5,
        wait_time: float = 30,
        statuses: Container = tuple(),
        exceptions: Exception = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),
        **kwargs
) -> requests.Response:
    """ Wrapper of delete request to add tries. The arguments are the same but with the following extra parameters:
    :param num_tries: The number of tries. 0, forever.
    :param wait_time: Time to wait between requests.
    :param statuses: A list of response statuses that force the repetition.
        By default, any status is valid, and it automatically returns the requests.
    :param exceptions: Exceptions that must happen to try again.
    """
    return _retry_request(
        requests.delete,
        *args,
        num_tries=num_tries,
        wait_time=wait_time,
        statuses=statuses,
        exceptions=exceptions,
        **kwargs
    )


@functools.wraps(requests.post)
def retry_post(
        *args,
        num_tries: int = 5,
        wait_time: float = 30,
        statuses: Container = tuple(),
        exceptions: Exception = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),
        **kwargs
) -> requests.Response:
    """ Wrapper of post request to add tries. The arguments are the same but with the following extra parameters:
    :param num_tries: The number of tries. 0, forever.
    :param wait_time: Time to wait between requests.
    :param statuses: A list of response statuses that force the repetition.
        By default, any status is valid, and it automatically returns the requests.
    :param exceptions: Exceptions that must happen to try again.
    """
    return _retry_request(
        requests.post,
        *args,
        num_tries=num_tries,
        wait_time=wait_time,
        statuses=statuses,
        exceptions=exceptions,
        **kwargs
    )


@functools.wraps(requests.patch)
def retry_patch(
        *args,
        num_tries: int = 5,
        wait_time: float = 30,
        statuses: Container = tuple(),
        exceptions: Exception = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),
        **kwargs
) -> requests.Response:
    """ Wrapper of patch request to add tries. The arguments are the same but with the following extra parameters:
    :param num_tries: The number of tries. 0, forever.
    :param wait_time: Time to wait between requests.
    :param statuses: A list of response statuses that force the repetition.
        By default, any status is valid, and it automatically returns the requests.
    :param exceptions: Exceptions that must happen to try again.
    """
    return _retry_request(
        requests.patch,
        *args,
        num_tries=num_tries,
        wait_time=wait_time,
        statuses=statuses,
        exceptions=exceptions,
        **kwargs
    )


@functools.wraps(requests.put)
def retry_put(
        *args,
        num_tries: int = 5,
        wait_time: float = 30,
        statuses: Container = tuple(),
        exceptions: Exception = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),
        **kwargs
) -> requests.Response:
    """ Wrapper of put request to add tries. The arguments are the same but with the following extra parameters:
    :param num_tries: The number of tries. 0, forever.
    :param wait_time: Time to wait between requests.
    :param statuses: A list of response statuses that force the repetition.
        By default, any status is valid, and it automatically returns the requests.
    :param exceptions: Exceptions that must happen to try again.
    """
    return _retry_request(
        requests.put,
        *args,
        num_tries=num_tries,
        wait_time=wait_time,
        statuses=statuses,
        exceptions=exceptions,
        **kwargs
    )


@functools.wraps(requests.head)
def retry_head(
        *args,
        num_tries: int = 5,
        wait_time: float = 30,
        statuses: Container = tuple(),
        exceptions: Exception = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),
        **kwargs
) -> requests.Response:
    """ Wrapper of head request to add tries. The arguments are the same but with the following extra parameters:
    :param num_tries: The number of tries. 0, forever.
    :param wait_time: Time to wait between requests.
    :param statuses: A list of response statuses that force the repetition.
        By default, any status is valid, and it automatically returns the requests.
    :param exceptions: Exceptions that must happen to try again.
    """
    return _retry_request(
        requests.head,
        *args,
        num_tries=num_tries,
        wait_time=wait_time,
        statuses=statuses,
        exceptions=exceptions,
        **kwargs
    )


@functools.wraps(requests.options)
def retry_options(
        *args,
        num_tries: int = 5,
        wait_time: float = 30,
        statuses: Container = tuple(),
        exceptions: Exception = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),
        **kwargs
) -> requests.Response:
    """ Wrapper of options request to add tries. The arguments are the same but with the following extra parameters:
    :param num_tries: The number of tries. 0, forever.
    :param wait_time: Time to wait between requests.
    :param statuses: A list of response statuses that force the repetition.
        By default, any status is valid, and it automatically returns the requests.
    :param exceptions: Exceptions that must happen to try again.
    """
    return _retry_request(
        requests.options,
        *args,
        num_tries=num_tries,
        wait_time=wait_time,
        statuses=statuses,
        exceptions=exceptions,
        **kwargs
    )


class ServiceError(Exception):
    @property
    def status_code(self) -> int:
        return self._status_code

    def __init__(self, status_code: int, *args, **kwargs) -> None:
        self._status_code = status_code


def _retry_request(
        func: Callable,
        *args,
        num_tries: int = 5,
        wait_time: float = 30,
        statuses: Container = tuple(),
        exceptions: Exception = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout),
        **kwargs
) -> requests.Response:
    """ Try to make the request several times whether it is any error.

    :param num_tries: The number of tries. 0, forever.
    :param wait_time: Time to wait between requests.
    :param statuses: A list of response statuses that force the repetition.
        By default, any status is valid, and it automatically returns the requests.
    :param exceptions: Exceptions that must happen to try again.
        """
    resp = None
    details = ''
    num_try = 0
    while num_tries == 0 or num_try < num_tries:
        try:
            resp = func(*args, **kwargs)
            if resp.status_code not in statuses:
                return resp
            details = (
                f'Response with error {str(resp.status_code)} calling the function "{func.__name__}()": '
                f'{str(resp.text)}\n'
                f'Trying in {wait_time} seconds...'
            )
            logger.warning(details)
        except exceptions as ex:
            details = (
                f'Unexpected error calling the function "{func.__name__}()": {str(ex)}\n'
                f'Trying in {wait_time} seconds...'
            )
            logger.warning(details)
        num_try += 1
        sleep(wait_time)

    raise ServiceError(resp.status_code if resp else 500, details)
