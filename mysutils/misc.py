import functools
import sys
import time
from typing import TypeVar, Callable, Type, Tuple, Union, Any, TextIO, Optional
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def retry(
    retries: int,
    delay: float = 1.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = (Exception,),
    msg: str = '',
    file: TextIO = sys.stdout,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to retry a function call if specific exceptions occur.

    :param retries: Maximum number of attempts.
    :param delay: Time in seconds to wait between retries.
    :param exceptions: An exception class or a tuple of exception classes to catch.
                       Defaults to (Exception,).
    :param msg: The message to print for each attempt.
                You can use {attempts} to include el number of attempts in the message.
    :param file: The file to write the exception message in. By default, it writes to standard out.
    :raises: The last exception encountered if all retry attempts fail,
             or any exception not included in the 'exceptions' parameter.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == retries:
                        raise e
                    if msg:
                        print(msg.format(attempts=attempts), file=file)
                    time.sleep(delay)

        return wrapper

    return decorator


def conditional(func: Callable, condition: Any, *args: Any, **kwargs) -> Optional[Any]:
    """ Call a function with its arguments if the condition is True.

    :param func: The function to execute.
    :param condition: The condition.
    :param args: The function arguments.
    :param kwargs: The function kwargs.
    :return: The same that the function returns.
    """
    if condition:
        return func(*args, **kwargs)
