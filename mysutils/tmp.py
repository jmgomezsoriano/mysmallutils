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

        from mysutils.file import removable_files, exist_files
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
    def __init__(self, folder: bool = False, suffix: str = '', prefix: str = ''):
        """

        :param folder:
        :param suffix:
        :param prefix:
        """
        self.__tmp = mkdtemp(suffix=suffix, prefix=prefix) if folder else mktemp(suffix=suffix, prefix=prefix)
        Removable.__init__(self, self.__tmp, recursive=folder, ignore_errors=True)

    def __fspath__(self) -> str:
        """
        :return: The path to the temporal path.
        """
        return self.__tmp


def removable_tmp(folder: bool = False, suffix: str = '', prefix: str = '') -> PathLike:
    """ This function is used with "with" python command. As following:

    .. code-block:: python

        from mysutils.file import removable_files, exist_files
        # These files will be removed when the with ends
        with removable_tmp() as tmp:
            exist_files(tmp.files[0])  # Returns True
        exist_files('test2.json', 'data/test1.json', 'data/')  # Returns False

    :return: A object with enter and exit methods.
    """
    return RemovableTemp(folder, suffix, prefix)
