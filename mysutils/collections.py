from typing import List


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
