import gzip
import pickle
from io import DEFAULT_BUFFER_SIZE
from json import dump, load
from os import makedirs
from os.path import exists, dirname, join, basename
from shutil import copyfile
from typing import Union, Optional, TextIO, Any

from typing.io import IO


def open_file(filename: Union[str, bytes, int],
              mode: str = 'rt',
              buffering: int = DEFAULT_BUFFER_SIZE,
              encoding: Optional[str] = None,
              errors: Optional[str] = None,
              newline: Optional[str] = None,
              close_fd: bool = True,
              opener: Optional = None) -> Union[IO, TextIO]:
    """ Open file and return a stream. Raise OSError upon failure.
    This function is the same as open() but it is able to open a gzip file automatically only taking into account the
    file extension. That means, if the file ends with a .gz extension, then this function will open a gzip file instead
    the normal one.

    :param filename: is either a text or byte string giving the name (and the path if the file isn't in the current
      working directory) of the file to be opened or an integer file descriptor of the file to be wrapped.
      See the open() function documentation for more information.
    :param mode: s an optional string that specifies the mode in which the file is opened. It defaults to 'r' which
      means open for reading in text mode. Other common values are 'w' for writing (truncating the file if it already
      exists), 'x' for creating and writing to a new file, and 'a' for appending (which on some Unix systems, means that
      all writes append to the end of the file regardless of the current seek position).
      See open() function for more information.
    :param buffering: this parameter is ignored for gzip files. It is an optional integer used to set the buffering
      policy. See open() function for more information.
    :param encoding: is the name of the encoding used to decode or encode the file. This should only be used in text
      mode. The default encoding is platform dependent, but any encoding supported by Python can be passed. See the
      codecs module for the list of supported encodings.
    :param errors: errors is an optional string that specifies how encoding errors are to be handled—this argument
      should not be used in binary mode. Pass 'strict' to raise a ValueError exception if there is an encoding error
      (the default of None has the same effect), or pass 'ignore' to ignore errors. (Note that ignoring encoding errors
      can lead to data loss.) See the documentation for codecs.register or run 'help(codecs.Codec)' for a list of the
      permitted encoding error strings.
    :param newline: newline controls how universal newlines works (it only applies to text mode).
      See open() function for more information.
    :param close_fd: If close_fd is False, the underlying file descriptor will be kept open when the file is closed.
      This does not work when a file name is given and must be True in that case.
    :param opener: A custom opener can be used by passing a callable as opener. The underlying file descriptor for the
      file object is then obtained by calling opener with (file, flags). opener must return an open file descriptor
      (passing os.open as opener results in functionality similar to passing None).
      See open() function for more information.
    :return: The opened stream.
    """
    if filename.lower().endswith('.gz'):
        return gzip.open(filename, mode, encoding=encoding, errors=errors, newline=newline)
    return open(filename, mode, buffering, encoding, errors, newline, close_fd, opener)


def force_open(filename: Union[str, bytes, int],
               mode: str = 'rt',
               buffering: int = DEFAULT_BUFFER_SIZE,
               encoding: Optional[str] = None,
               errors: Optional[str] = None,
               newline: Optional[str] = None,
               close_fd: bool = True,
               opener: Optional = None) -> Union[IO, TextIO]:
    """ Open file and return a stream. Raise OSError upon failure.
    This function is the same as open_file() but if the file folder does not exist, then create all the necessary
    folders before opening the file.

    :param filename: is either a text or byte string giving the name (and the path if the file isn't in the current
      working directory) of the file to be opened or an integer file descriptor of the file to be wrapped.
      See the open() function documentation for more information.
    :param mode: s an optional string that specifies the mode in which the file is opened. It defaults to 'r' which
      means open for reading in text mode. Other common values are 'w' for writing (truncating the file if it already
      exists), 'x' for creating and writing to a new file, and 'a' for appending (which on some Unix systems, means that
      all writes append to the end of the file regardless of the current seek position).
      See open() function for more information.
    :param buffering: this parameter is ignored for gzip files. It is an optional integer used to set the buffering
      policy. See open() function for more information.
    :param encoding: is the name of the encoding used to decode or encode the file. This should only be used in text
      mode. The default encoding is platform dependent, but any encoding supported by Python can be passed. See the
      codecs module for the list of supported encodings.
    :param errors: errors is an optional string that specifies how encoding errors are to be handled—this argument
      should not be used in binary mode. Pass 'strict' to raise a ValueError exception if there is an encoding error
      (the default of None has the same effect), or pass 'ignore' to ignore errors. (Note that ignoring encoding errors
      can lead to data loss.) See the documentation for codecs.register or run 'help(codecs.Codec)' for a list of the
      permitted encoding error strings.
    :param newline: newline controls how universal newlines works (it only applies to text mode).
      See open() function for more information.
    :param close_fd: If close_fd is False, the underlying file descriptor will be kept open when the file is closed.
      This does not work when a file name is given and must be True in that case.
    :param opener: A custom opener can be used by passing a callable as opener. The underlying file descriptor for the
      file object is then obtained by calling opener with (file, flags). opener must return an open file descriptor
      (passing os.open as opener results in functionality similar to passing None).
      See open() function for more information.
    :return: The opened stream.
    """
    if not exists(dirname(filename)):
        makedirs(dirname(filename))
    return open_file(filename, mode, buffering, encoding, errors, newline, close_fd, opener=opener)


def copy_files(dest: str, *files, force: bool = True) -> None:
    """ Copy a list of files into destination folder.
    :param dest: The destination folder.
    :param files: The list of files to copy.
    :param force: Force the creation of the path folders if they do not exist.
    """
    if not exists(dest) and force:
        makedirs(dest)
    for file in files:
        copyfile(file, join(dest, basename(file)))


def save_json(obj: Any, filename: str, force: bool = False) -> None:
    """ Save an object into a json file.
    :param obj: The object to save.
    :param filename: The path to the output file.
    :param force: Force the creation of the path folders if they do not exist.
    """
    with force_open(filename, 'wt') if force else open_file(filename, 'wt') as file:
        dump(obj, file, indent=2)


def load_json(filename: str) -> Any:
    """ Load a json file and return a object with its data.
    :param filename: The json file.
    :return: An object with the json data.
    """
    with open_file(filename, 'rt') as file:
        return load(file)


def save_pickle(obj: object, filename: str, force: bool = False) -> None:
    """ Save an object into a pickle file.
    :param obj: The object to save.
    :param filename: The path to the output file.
    :param force: Force the creation of the path folders if they do not exist.
    """
    with force_open(filename, 'wb') if force else open_file(filename, 'wb') as file:
        pickle.dump(obj, file)


def load_pickle(filename: str) -> Any:
    """ Load an object from pickle file.
    :param filename: The pickle file path.
    :return: An object with the pickle file data.
    """
    with open_file(filename, 'rb') as file:
        return pickle.load(file)
