from os import PathLike
from tempfile import mkdtemp, mktemp
from typing import Tuple, Union, Iterator

from mysutils.file import remove_files


class Removable(object):
    """ Class to include enter and exit methods for removable files. """
    @property
    def files(self) -> Tuple[Union[str, PathLike, bytes]]:
        """
        :return: The list of files to remove.
        """
        return self.__files

    @property
    def ignore_errors(self) -> bool:
        """
        :return: Ignore the error if the file does not exist.
        """
        return self.__ignore_errors

    @property
    def recursive(self) -> bool:
        """
        :return: If True, remove the folders recursively, otherwise False.
        """
        return self.__recursive

    def __init__(self, *files: Union[PathLike, str, bytes], recursive: bool = False,
                 ignore_errors: bool = True) -> None:
        """ Constructor.

        :param files: The files to remove.
        :param ignore_errors: If True, if a file does not exist, then ignore the error.
        :param recursive: If True, remove the folders recursively.
        """
        self.__files = files
        self.__ignore_errors = ignore_errors
        self.__recursive = recursive

    def __enter__(self) -> object:
        """
        :return: return self.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """ Remove all the removable files.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        """
        remove_files(*self.__files, ignore_errors=self.__ignore_errors, recursive=self.__recursive)

    def __repr__(self) -> str:
        """
        :return: A string representation of this object.
        """
        return str(self.__files)

    def __getitem__(self, item: int) -> Union[PathLike, str, bytes]:
        """ Obtain an path of the removable files.
        :param item: The index of the file to retrieve.
        :return: The path to the removable file of the index item.
        """
        return self.__files[item]

    def __iter__(self) -> Iterator:
        """
        :return: The iterator of the removable files.
        """
        return iter(self.__files)


def removable_files(*files: Union[PathLike, str, bytes], recursive: bool = False, ignore_errors: bool = True) -> object:
    """ This function is used with "with" python command. As following:

    .. code-block:: python

        from mysutils.file import exist_files
        from mysutils.tmp import removable_files
        # These files will be removed when the with ends
        with removable_files('test2.json', 'data/test1.json', 'data/'):
            exist_files('test2.json', 'data/test1.json', 'data/')  # Returns True
        exist_files('test2.json', 'data/test1.json', 'data/')  # Returns False

    :param files: The files to remove al the end.
    :param recursive: If True, remove the folders recursively.
    :param ignore_errors: If True, ignore the errors, for example the file not found error.
    :return: A object with enter and exit methods.
    """
    return Removable(*files, recursive=recursive, ignore_errors=ignore_errors)


class RemovableTemp(Removable, PathLike):
    """ Create a removable temporal file. """
    def __init__(self, is_folder: bool = False, suffix: str = '', prefix: str = ''):
        """ Constructor.

        :param is_folder:
        :param suffix: The temporal file suffix.
        :param prefix: The temporal file prefix.
        """
        self.__tmp = mkdtemp(suffix=suffix, prefix=prefix) if is_folder else mktemp(suffix=suffix, prefix=prefix)
        Removable.__init__(self, self.__tmp, recursive=is_folder, ignore_errors=True)

    def __fspath__(self) -> str:
        """
        :return: The path to the temporal path.
        """
        return self.__tmp

    def __enter__(self) -> object:
        """
        :return: return self.
        """
        return self[0]


def removable_tmp(is_folder: bool = False, suffix: str = '', prefix: str = '') -> PathLike:
    """ This function is used with "with" python command. As following:

    .. code-block:: python

        from mysutils.file import exist_files
        from mysutils.tmp import removable_files
        # These files will be removed when the with ends
        with removable_tmp() as tmp:
            exist_files(tmp)  # Returns True
        exist_files(tmp)  # Returns False

    :param is_folder: True if the temporal file should be a folder.
    :param suffix: The temporal file suffix.
    :param prefix: The temporal file prefix.

    :return: A object with enter and exit methods.
    """
    return RemovableTemp(is_folder, suffix, prefix)


class RemovableTemps(Removable):
    """ Create removable temporal files. """
    def __init__(self, num: int = 1, are_folders: bool = False, suffix: str = '', prefix: str = ''):
        """ Constructor.

        :param num: The number of temporal files.
        :param are_folders: If the temporal files should be folders.
        :param suffix: The temporal file suffixes.
        :param prefix: The temporal file prefixes.
        """
        mktmp = mkdtemp if are_folders else mktemp
        self.__tmps = [mktmp(suffix=suffix, prefix=prefix) for _ in range(num)]
        Removable.__init__(self, *self.__tmps, recursive=are_folders, ignore_errors=True)


def removable_tmps(num: int = 1, is_folder: bool = False, suffix: str = '', prefix: str = '') -> object:
    """ This function is used with "with" python command. As following:

    .. code-block:: python

        from mysutils.file import removable_files, exist_files
        # These files will be removed when the with ends
        with removable_tmps(2) as (tmp1, tmp2):
            exist_files(tmp1, tmp2)  # Returns True
        exist_files(tmp1, tmp2)  # Returns False

    :param num: The number of temporal files.
    :param is_folder: True if the temporal files should be folders.
    :param suffix: The temporal file suffixes.
    :param prefix: The temporal file prefixes.

    :return: A object with enter and exit methods.
    """
    return RemovableTemps(num, is_folder, suffix, prefix)
