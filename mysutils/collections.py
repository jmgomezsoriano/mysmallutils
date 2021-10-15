from typing import Union, List


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


def del_keys(d: dict, keys: Union[List[str], str] = None, ignore_errors: bool = True) -> dict:
    """ Remove the dictionary items from their keys and return the modified dictionary.

    :param d: The dictionary.
    :param keys: A key or a list of keys.
    :param ignore_errors: If True, ignore if the key does not exist.
    :return: The modified dictionary.
    """
    keys = keys if keys else []
    for key in keys if isinstance(keys, list) else [keys]:
        if key not in d and ignore_errors:
            pass
        else:
            del d[key]

    return d