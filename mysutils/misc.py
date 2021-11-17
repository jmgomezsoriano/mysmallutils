from typing import Callable, Any


def conditional(func: Callable, condition: Any, *args: Any, **kwargs) -> Any:
    """ Call a function with its arguments if the condition is True.

    :param func: The function to execute.
    :param condition: The condition.
    :param args: The function arguments.
    :param kwargs: The function kwargs.
    :return: The same that the function returns.
    """
    if condition:
        return func(*args, **kwargs)