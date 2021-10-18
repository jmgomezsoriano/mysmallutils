from typing import Union, List, Any, Callable


def head(obj: Union[dict, set], top: int = 10) -> Union[dict, set]:
    """ Obtain the first top elements of a dictionary o a set.

    :param obj: A dictionary or a set.
    :param top: The number of elements to return, by default 10.
    :return: The first top elements of the given dictionary or set.
    """
    if isinstance(obj, dict):
        return dh(obj, top)
    if isinstance(obj, set):
        return sh(obj, top)
    raise ValueError('The object must be a dictionary or a set.')


def dh(d: dict, top: int = 10) -> dict:
    """ Obtain the first top elements of a dictionary.

    :param d: The dictionary.
    :param top: The number of dictionary items to return
    :return: A dictionary with the top first items of the given dictionary.
    """
    return {key: value for i, (key, value) in enumerate(d.items()) if i < top}


def sh(d: set, top: int = 10) -> set:
    """ Obtain the first top elements of a set.

    :param d: The set.
    :param top: The number of set items to return
    :return: A set with the top first items of the given set.
    """
    return {value for i, value in enumerate(sorted(d)) if i < top}


def list_union(*lists: list) -> list:
    """ Create a new list with the union of the lists without repeated elements.

    :param lists: The list to union.
    :return: The union of all lists respecting the element order.
    """
    result = []
    for l in lists:
        for e in l:
            if e not in result:
                result.append(e)
    return result


def del_keys(d: dict, *keys: Any, ignore_errors: bool = True) -> dict:
    """ Remove the dictionary items from their keys and return the modified dictionary.

    :param d: The dictionary.
    :param keys: A key or a list of keys.
    :param ignore_errors: If True, ignore if the key does not exist.
    :return: The modified dictionary.
    """
    for key in keys:
        if not (key not in d and ignore_errors):
            del d[key]

    return d


def add_keys(d: dict, modify: bool = True, **kwargs) -> dict:
    """ Add or change several items into a dictionary and return the modified dictionary.

    :param d: The dictionary.
    :param modify: If True, if a key already exists, then update it, otherwise raise an error.
    :param kwargs: The dictionary key/value pairs.
    :return: The modified dictionary.
    """
    for key, value in kwargs.items():
        if not modify and key in d:
            raise KeyError("Duplicate key")
        d[key] = value

    return d


def filter_lst(lst: list, n: int = 0, init: int = 0, filter_func: Callable = None) -> list:
    """ Filter a list.

    :param lst: The list to filter.
    :param n: The maximum number of results. If it is not given, then return all the results.
    :param init: The initial result. Before this position the items are filtered.
    :param filter_func: A filter function to filter.
    :return: The filtered list.
    """
    n = n if n else len(lst)
    lst = lst[init:init + n]
    return [e for e in filter(filter_func, lst)] if filter_func else lst