import gzip
from collections import OrderedDict, Hashable
from os import PathLike
from typing import Union, Dict, Any, Optional

from mysutils.tar import open_tar_file
from mysutils.file import open_file, force_open

try:
    from yaml import add_representer, dump, load, SafeLoader
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('ModuleNotFoundError: No module named \'yaml\'. Please install it with the command:\n\n'
                              'pip install PyYAML~=5.4.1')


def save_yaml(data: Union[Dict[Hashable, Any], list, None],
              filename: Union[str, PathLike, bytes],
              force: bool = False,
              encoding: Optional[str] = None) -> None:
    """ Save an object as a YAML file preserving the dictionary order.
    :param filename: The path to the output file.
    :param data: The data to save.
    :param force: Force the creation of the path folders if they do not exist.
    :param encoding: The file encoding. By default, the system default encoding is used.
    """
    add_representer(OrderedDict, representer=lambda self, d: self.represent_mapping('tag:yaml.org,2002:map', d.items()))
    open_func = force_open if force else open_file
    with open_func(filename, 'wt', encoding=encoding) as file:
        dump(data, file, default_flow_style=False, allow_unicode=encoding is not None)


def load_yaml(filename: Union[str, PathLike, bytes],
              encoding: Optional[str] = None,
              default: Any = None) -> Union[Dict[Hashable, Any], list, None]:
    """ Load an object from a YAML file.
    :param filename: The path to the YAML file.
    :param encoding: The file encoding. By default, the system default encoding is used.
    :param default: The default value if the file does not exist.
    :return: The loaded object.
    """
    try:
        with open_file(filename, 'rt', encoding=encoding) as file:
            return load(file, SafeLoader)
    except FileNotFoundError as e:
        if default is None:
            raise e
        return default


def load_tar_yaml(tar_file: Union[str, PathLike, bytes],
                  filename: Union[str, PathLike, bytes],
                  encoding: Optional[str] = None,
                  default: Any = None) -> Any:
    """ Load an object from a YAML file stored in a tar file.

    :param tar_file: The path to the tar file-.
    :param filename: The path inside of the tar to the file to extract.
    :param encoding: The file encoding. By default, the system default encoding is used.
    :param default: The default value if the file does not exist.
    :return: The loaded object.
    """
    try:
        with open_tar_file(tar_file, filename) as file:
            if str(filename).lower().endswith('.gz') or str(filename).lower().endswith('.tgz'):
                return load(gzip.open(file, encoding=encoding))
            return load(file)
    except FileNotFoundError as e:
        if default:
            return default
        raise e
