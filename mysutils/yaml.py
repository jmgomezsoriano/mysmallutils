import gzip
from collections import OrderedDict, Hashable
from os import PathLike
from typing import Union, Dict, Any

from mysutils.tar import open_tar_file

try:
    from yaml import add_representer, dump, load, SafeLoader
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('ModuleNotFoundError: No module named \'yaml\'. Please install it with the command:\n\n'
                              'pip install PyYAML~=5.4.1')

from mysutils.file import open_file, force_open


def save_yaml(data: Union[Dict[Hashable, Any], list, None],
              filename: Union[str, PathLike, bytes],
              force: bool = False) -> None:
    """ Save an object as a YAML file preserving the dictionary order.
    :param filename: The path to the output file.
    :param data: The data to save.
    :param force: Force the creation of the path folders if they do not exist.
    """
    add_representer(OrderedDict, representer=lambda self, d: self.represent_mapping('tag:yaml.org,2002:map', d.items()))
    with force_open(filename, 'wt') if force else open_file(filename, 'wt') as file:
        dump(data, file, default_flow_style=False)


def load_yaml(filename: Union[str, PathLike, bytes]) -> Union[Dict[Hashable, Any], list, None]:
    """ Load an object from a YAML file.
    :param filename: The path to the YAML file.
    :return: The loaded object.
    """
    with open_file(filename, 'rt') as file:
        return load(file, SafeLoader)


def load_tar_yaml(tar_file: Union[str, PathLike, bytes], filename: Union[str, PathLike, bytes]) -> Any:
    """ Load an object from a YAML file stored in a tar file.

    :param tar_file: The path to the tar file-.
    :param filename: The path inside of the tar to the file to extract.
    :return: The loaded object.
    """
    with open_tar_file(tar_file, filename) as file:
        if str(filename).lower().endswith('.gz') or str(filename).lower().endswith('.tgz'):
            return load(gzip.open(file))
        return load(file)
