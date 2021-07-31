import logging
from typing import List, Tuple, Union

LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_log_levels() -> List[Tuple[str, int]]:
    """ Obtain the defined log level names and its integer representation.
    :return: A list of tuples with the official level name and its integer value.
    """
    return [(k, v) for k, v in logging._nameToLevel.items()]


def get_log_level_names(low_case: bool = True) -> List[str]:
    """ Obtain a list with the level names.
    :param low_case: If convert the level names into lower case.
    :return: A list of level names.
    """
    return [k.lower() if low_case else k for k in logging._nameToLevel]


def get_log_level(name: str) -> int:
    """ Return the number representation of a level from its name.

    :param name: The level name.
    :return: Its integer value.
    """
    return logging._nameToLevel[name.upper()]


def config_log(level: Union[str, int], filename: str = None) -> None:
    """  Configure easily the logging using a default log and date format.

    :param level: The level name or number.
    :param filename: The file name to store the logs. By default, the standard error output is used.
    """
    level = level.upper() if isinstance(level, str) else level
    if filename:
        logging.basicConfig(level=level, filename=filename, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    else:
        logging.basicConfig(level=level, format=LOG_FORMAT, datefmt=DATE_FORMAT)
