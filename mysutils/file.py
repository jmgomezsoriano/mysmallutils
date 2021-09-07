import gzip
import pickle
import os
import re
from datetime import datetime
from io import DEFAULT_BUFFER_SIZE
from json import dump, load
from os import makedirs, remove, rmdir, scandir, PathLike
from os.path import exists, dirname, join, basename, isdir
from shutil import copyfile, rmtree
from sys import stdout
from shutil import move
from typing import Union, Optional, TextIO, Any, List, Tuple

from typing.io import IO


def open_file(filename: Union[PathLike, str, bytes],
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


def force_open(filename: Union[PathLike, str, bytes],
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


def copy_files(dest: Union[PathLike, str, bytes], *files: Union[PathLike, str, bytes], force: bool = True) -> None:
    """ Copy a list of files into destination folder.
    :param dest: The destination folder.
    :param files: The list of files to copy.
    :param force: Force the creation of the path folders if they do not exist.
    """
    if not exists(dest) and force:
        makedirs(dest)
    for file in files:
        copyfile(file, join(dest, basename(file)))


def save_json(obj: Any, filename: Union[PathLike, str, bytes], force: bool = False) -> None:
    """ Save an object into a json file.
    :param obj: The object to save.
    :param filename: The path to the output file.
    :param force: Force the creation of the path folders if they do not exist.
    """
    with force_open(filename, 'wt') if force else open_file(filename, 'wt') as file:
        dump(obj, file, indent=2)


def load_json(filename: Union[PathLike, str, bytes]) -> Any:
    """ Load a json file and return a object with its data.
    :param filename: The json file.
    :return: An object with the json data.
    """
    with open_file(filename, 'rt') as file:
        return load(file)


def save_pickle(obj: object, filename: Union[PathLike, str, bytes], force: bool = False) -> None:
    """ Save an object into a pickle file.
    :param obj: The object to save.
    :param filename: The path to the output file.
    :param force: Force the creation of the path folders if they do not exist.
    """
    with force_open(filename, 'wb') if force else open_file(filename, 'wb') as file:
        pickle.dump(obj, file)


def load_pickle(filename: Union[PathLike, str, bytes]) -> Any:
    """ Load an object from pickle file.
    :param filename: The pickle file path.
    :return: An object with the pickle file data.
    """
    with open_file(filename, 'rb') as file:
        return pickle.load(file)


def gzip_decompress(input_file: Union[PathLike, str, bytes], output_file: Union[PathLike, str, bytes]) -> None:
    """ Decompress a file using gzip compression.
    :param input_file: The file to compress.
    :param output_file: The compressed file with all the information of the input file.
    """
    if input_file == output_file:
        raise ValueError('The input file and the output file must be different.')
    with open(output_file, 'wb') as writer:
        with gzip.open(input_file, 'rb') as reader:
            for chunk in reader:
                writer.write(chunk)


def gzip_compress(input_file: Union[PathLike, str, bytes], output_file: Union[PathLike, str, bytes]) -> None:
    """ Compress a file using gzip compression.
    :param input_file: The file to compress.
    :param output_file: The compressed file with all the information of the input file.
    """
    if input_file == output_file:
        raise ValueError('The input file and the output file must be different.')
    with gzip.open(output_file, 'wb') as writer:
        with open(input_file, 'rb') as reader:
            for chunk in reader:
                writer.write(chunk)


def remove_files(*files: Union[PathLike, str, bytes], ignore_errors: bool = False, recursive: bool = False) -> None:
    """ Remove several files and empty directories at once.

    :param files: The list of files or empty directories to remove. To remove directories with files or subdirectories,
      please, use shutil.rmtree().
    :param ignore_errors: If True, ignore the error if the file or directory does not exist.
    """
    for file in files:
        if isdir(file):
            if recursive:
                rmtree(file)
            else:
                rmdir(file)
        elif not ignore_errors or exists(file):
            remove(file)


def first_line(filename: Union[PathLike, str, bytes]) -> str:
    """ Read the first line of a file removing the final \n if it exists.

    :param filename: The filename to read.
    :return: A string with the first line.
    """
    with open_file(filename) as file:
        line = file.readline()
        return line[:-1] if line.endswith('\n') else line


def exist_files(*files: Union[PathLike, str, bytes]) -> bool:
    """ Check if a sequence of files exist.

    :param files: The list of file paths to check.
    :return: True if all the files exist, otherwise False.
    """
    for file in files:
        if not exists(file):
            return False
    return True


def not_exist_files(*files: Union[PathLike, str, bytes]) -> bool:
    """ Check if any of the files exist.

    :param files: The list of file paths to check.
    :return: True if any of the files exist. If exists at least one, then False.
    """
    for file in files:
        if exists(file):
            return False
    return True


def are_dir(*files: Union[PathLike, str, bytes]) -> bool:
    """ Check if a sequence of files are directories.

    :param files: The list of file paths to check.
    :return: True if all of the files are directories, otherwise False.
    """
    for file in files:
        if not isdir(file):
            return False
    return True


def not_are_dir(*files: Union[PathLike, str, bytes]) -> bool:
    """ Check if any of a sequence of files are directories.

    :param files: The list of file paths to check.
    :return: True if any of the files exist, otherwise False.
    """
    for file in files:
        if isdir(file):
            return False
    return True


def count_lines(filename: Union[PathLike, str, bytes]) -> int:
    """ Calculate the number of lines in a file.

    :param filename: The filename to calculate its size.
    :return: The number of lines of the file.
    """
    count = 0
    with open_file(filename) as file:
        for _ in file:
            count += 1
    return count


def touch(*files: Union[PathLike, str, bytes]) -> Tuple[Union[PathLike, str, bytes]]:
    """ Create several empty files.

    :param files: The list of file paths to create.
    :return: The list of created files.
    """
    for file in files:
        open(file, 'w').close()
    return files


def cat(filename: Union[PathLike, str, bytes], output: TextIO = stdout) -> None:
    """ Print a file content.

    :param filename: The path to the file. If the file name ends with ".gz", this function decompressed it to print.
    :param output: The stream to print. By default, the standard output.
    """
    with open_file(filename, 'rt') as file:
        for line in file:
            print(line, end='', file=output)


def read_file(filename: Union[PathLike, str, bytes], line_break: bool = True) -> List[str]:
    """ Read a file (compressed with gzip or not) and return in a list its content, each line in a list element.

    :param filename: The path to the file. If the file name ends with ".gz", this function decompressed it first.
    :param line_break: If True, the newline character is conserved, otherwise is removed.
    :return: An array with the contents of the file.
    """
    with open_file(filename, 'rt') as file:
        return [line[:-1] if not line_break and line[-1] == '\n' else line for line in file]


def mkdirs(*paths: Union[PathLike, str, bytes], mode: int = 0o777,
           dir_fd: int = None) -> Tuple[Union[PathLike, str, bytes]]:
    """ Create one or several directories ignoring the error if the file or folder already exists.
    :param paths: The list of path to the directories.
    :param mode: The mode argument is ignored on Windows. By default, 0o777.
    :param dir_fd: If dir_fd is not None, it should be a file descriptor open to a directory,
        and path should be relative; path will then be relative to that directory.
        dir_fd may not be implemented on your platform.
        If it is unavailable, using it will raise a NotImplementedError.
    :return: The list of created directories.
    """
    for path in paths:
        if not exists(path):
            os.mkdir(path, mode, dir_fd=dir_fd)
    return paths


def move_files(dest: Union[PathLike, str, bytes], *files: Union[PathLike, str, bytes],
               force: bool = False, replace: bool = False) -> None:
    """ Move several files at once.

    :param dest: The destination folder.
    :param files: The files to move.
    :param force: If True, create the folder if it doesn't exist.
    :param replace: if any of the files exist, replace them.
    """
    if force:
        mkdirs(dest)
    for file in files:
        if exists(join(dest, file)) and replace:
            remove(join(dest, file))
        move(file, dest)


def list_dir(folder: Union[PathLike, str, bytes] = '.', filter: str = None, reverse: bool = False) -> List[str]:
    """ List a directory and return a list with all file path of that directory that satisfy the given filter,
        ordered alphabetically.

    :param folder: The folder to list.
    :param filter: The filter to apply.
    :param reverse: If True, the list is inverted sorted. By default, False.
    :return: The list with the path to each directory.
    """
    return sorted([
        join(folder, file.name) for file in scandir(folder) if not filter or re.match(filter, file.name)
    ], reverse=reverse)


def first_file(folder: Union[PathLike, str, bytes] = '.', filter: str = None) -> str:
    """ Obtain the first file name ordered alphabetically from a folder. By default, it uses the current folder.
    :param folder: The folder path with the files.
    :param filter: A regular expression pattern to filter the files. By default, all files are taking into account.
    :return: The first file name.
    """
    files = list_dir(folder, filter)
    return files[0] if files else None


def last_file(folder: Union[PathLike, str, bytes] = '.', filter: str = None) -> str:
    """ Obtain the last file name ordered alphabetically from a folder. By default, it uses the current folder.
    :param folder: The folder path with the files. By default, all files are taking into account.
    :param filter: A regular expression pattern to filter the files.
    :return: The last file name.
    """
    files = list_dir(folder, filter, True)
    return files[0] if files else None


def output_file_path(folder: Union[PathLike, str, bytes] = '.', suffix: str = '', timestamp: bool = True, **kwargs) -> str:
    """ Build a file path in the specified folder based on the current timestamp and several attributes.
    :param folder: The directory where the file will be located.
    :param timestamp: If you want to add the timestamp to the file name.
    :param suffix: If suffix file name.
    :param kwargs: Extra arguments to form the name. If it is a str, float or int value, then the value will be add to
      the name. If it is a bool value and it is True, then the name of the argument is add to the file name.
    :return: The full path to the file to create.
    """
    name = []
    if timestamp:
        name.append(datetime.now().strftime('%Y%m%d-%H%M%S'))
    for param, value in kwargs.items():
        if isinstance(value, bool):
            name += [param] if value else []
        elif value:
            name.append(str(value))

    return join(folder, f'{"-".join(name)}{suffix}')
