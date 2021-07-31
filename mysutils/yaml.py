import gzip
from collections import OrderedDict, Hashable
from typing import Union, Dict, Any

from yaml import add_representer, dump, load, SafeLoader

from mysutils.file import open_file, force_open


def save_yaml(data: Any, fname: str, force: bool = False) -> None:
    """ Save a dict as a YAML file preserving the dictionary order.
    :param fname: The path to the output file.
    :param data: The data to save.
    """
    add_representer(OrderedDict, representer=lambda self, d: self.represent_mapping('tag:yaml.org,2002:map', d.items()))
    with force_open(fname, 'wt') if force else open_file(fname, 'wt') as file:
        dump(data, file, default_flow_style=False)


def load_yaml(fname: str) -> Union[Dict[Hashable, Any], list, None]:
    """ Load a dictionary from a YAML file.
    :param fname: The path to the YAML file.
    :return: The loaded object.
    """
    with open_file(fname, 'rt') as file:
        return load(file, SafeLoader)
