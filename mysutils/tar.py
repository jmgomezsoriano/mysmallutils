import gzip
import json
import pickle
import tarfile
from os import makedirs
from tarfile import TarInfo
from os.path import basename, isdir, join, exists, splitext, dirname, normpath
from typing import List, Any
from shutil import move

from typing.io import IO


from mysutils.file import copy_files, list_dir
from mysutils.tmp import removable_tmp
# Import tqdm if it is installed, otherwise a dummy tqdm function is used.
try:
    from tqdm.auto import tqdm
except ModuleNotFoundError as e:
    def tqdm(obj: Any) -> Any:
        return obj

# Available tar compress methods
COMPRESS_METHODS = {'gz', 'bz2', 'xz'}


def create_tar(filename: str, *files: str, verbose: bool = False, compress_method: str = None) -> str:
    """
    Create a tar file with a given list of files. If the filename has any of these extensions 'gz', 'bz2' or 'xz',
      then the tar file will be compressed with the specify method.
    :param filename: The name of the tar file.
    :param files: The list of file paths to include in the tar file.
    :param verbose: if True, show a bar progress.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: The TAR filename.
    """
    compress_method = compress_method if compress_method else detect_compress_method(filename)
    with tarfile.open(filename, f'w:{compress_method}') as tar:
        for file in tqdm(files, desc='Creating tar file', disable=not verbose):
            tar.add(file, basename(normpath(file)))
    return filename


def add_tar_files(filename: str, *files: str, verbose: bool = False, compress_method: str = None) -> str:
    """ Add files to a previously created tar file.

    :param filename: The TAR file. It may be a compressed one or not.
    :param files: A list of file paths to include in the tar file
    :param verbose: If you want to show a progress bar.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: The TAR filename.
    """
    compress_method = compress_method if compress_method else detect_compress_method(filename)
    if compress_method and exists(filename):
        add_compressed_tar_files(filename, *files, verbose=verbose)
    else:
        with tarfile.open(filename, f'a' if exists(filename) else f'w:{compress_method}') as tar:
            for file in tqdm(files, desc='Adding files to tar', disable=not verbose):
                tar.add(file, basename(normpath(file)))
    return filename


def add_compressed_tar_files(filename: str, *files: str, verbose: bool = False, compress_method: str = None) -> str:
    """ Add files to a previously created tar file.

    :param filename: The TAR file. It has to be a compressed one.
    :param files: A list of file paths to include in the tar file
    :param verbose: If you want to show a progress bar.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: The TAR filename.
    """
    compress_method = compress_method if compress_method else detect_compress_method(filename)
    if compress_method and exists(filename):
        with removable_tmp(True) as tmp_dir:
            extract_tar(filename, tmp_dir, False, verbose)
            copy_files(tmp_dir, *files, force=True)
            with removable_tmp(suffix=f'.{compress_method}') as tmp_file:
                create_tar(tmp_file, *list_dir(tmp_dir), verbose=verbose)
                move(tmp_file, filename)
    else:
        with tarfile.open(filename, f'a' if exists(filename) else f'w:{compress_method}') as tar:
            for file in tqdm(files, desc='Adding files to tar', disable=not verbose):
                tar.add(file, basename(file))
    return filename


def detect_compress_method(filename: str) -> str:
    """ Detecting the compression method based on the extension of the filename.

    :param filename: The file path to the tar file.
    :return: 'gz', 'bz2' or 'xz' if the file is compressed by one of these methods, otherwise an empty string.
    """
    extension = splitext(filename)[1]
    return extension[1:].lower() if extension[1:].lower() in COMPRESS_METHODS else ''


def open_tar_file(tar_file: str, filename: str, compress_method: str = None) -> IO:
    """ Open a tar file and return a IO stream to the file.

    :param tar_file: The path to the tar file-.
    :param filename: The path inside of the tar to the file to extract.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: An IO stream.
    """
    compress_method = compress_method if compress_method else detect_compress_method(tar_file)
    tar = tarfile.open(tar_file, f'r:{compress_method}')
    file = tar.extractfile(filename)
    old_close = file.close

    def close():
        tar.close()
        old_close()

    file.close = close
    return file


def load_tar_json(tar_file: str, filename: str, compress_method: str = None) -> Any:
    """ Load an object from a JSON file stored in a tar file.

    :param tar_file: The path to the tar file-.
    :param filename: The path inside of the tar to the file to extract.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: The loaded object.
    """
    with open_tar_file(tar_file, filename, compress_method) as file:
        if filename.lower().endswith('.gz'):
            return json.load(gzip.open(file))
        return json.load(file)


def load_tar_pickle(tar_file: str, filename: str, compress_method: str = None) -> Any:
    """ Load an object from a pickle file stored in a tar file.

    :param tar_file: The path to the tar file-.
    :param filename: The path inside of the tar to the file to extract.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: The loaded object.
    """
    with open_tar_file(tar_file, filename, compress_method) as file:
        if filename.lower().endswith('.gz'):
            return pickle.load(gzip.open(file))
        return pickle.load(file)


def list_tar(tar_file: str, compress_method: str = None) -> List[TarInfo]:
    """ Obtain a list with the information of each file or directory of a tar file.

    :param tar_file: The path to the tar file.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: A list of TarInfo instances.
    """
    compress_method = compress_method if compress_method else detect_compress_method(tar_file)
    with tarfile.open(tar_file, f'r:{compress_method}') as tar:
        return tar.getmembers()


def extract_tar_file(tar_file: str, dest: str, filename: str, compress_method: str = None) -> str:
    """ Extract a file inside of a tar archive.

    :param tar_file: The path to the tar file.
    :param dest: The file or folder where the tar archive should be extracted.
    :param filename: The relative path inside of the tar file to extract.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: The TAR filename.
    """
    compress_method = compress_method if compress_method else detect_compress_method(tar_file)
    dest = join(dest, filename) if isdir(dest) else dest
    with tarfile.open(tar_file, f'r:{compress_method}') as tar:
        with tar.extractfile(filename) as reader:
            if dirname(dest) and not exists(dirname(dest)):
                makedirs(dirname(dest))
            with open(dest, 'wb') as writer:
                for chunk in reader:
                    writer.write(chunk)
    return tar_file


def extract_tar_files(tar_file: str, dest: str, *files: str, force: bool = False,
                      verbose: bool = False, compress_method: str = None) -> str:
    """ Extract a file inside of a tar archive.

    :param tar_file: The path to the tar file.
    :param dest: The folder where the tar archive should be extracted.
    :param files: The relative path inside of the tar file to extract.
    :param force: If True, create the destination directory if it doesn't exist.
      If files is not given, then extract all the files.
    :param verbose: If verbose, show the progress bar.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: The TAR filename.
    """
    if not exists(dest) and force:
        makedirs(dest)
    if not isdir(dest):
        raise ValueError(f'The destination is not an existing folder.')
    files = files if files else [file.path for file in list_tar(tar_file)]
    for file in tqdm(files, desc='Extracting files', disable=not verbose):
        extract_tar_file(tar_file, dest, file, compress_method)
    return tar_file


def extract_tar(tar_file: str, dest: str, force: bool = False, verbose: bool = False,
                compress_method: str = None) -> str:
    """ Extract all the files inside of a tar file in the specified directory.

    :param tar_file: The tar file to extract.
    :param dest: The destination directory.
    :param force: If True, create the destination directory if it doesn't exist.
    :param verbose: If verbose, show the progress bar.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: The TAR filename.
    """
    if not exists(dest) and force:
        makedirs(dest)
    if not exists(dest):
        raise FileNotFoundError(f'The folder "{dest}" does not exists. Create it or put the parameter force to True.')

    files = list_tar(tar_file, compress_method)
    for file in tqdm(files, desc='Extracting files', disable=not verbose):
        if file.isdir():
            makedirs(join(dest, file.path))
        else:
            extract_tar_file(tar_file, dest, file.path, compress_method)
    return tar_file


def exist_tar_files(tar_file: str, *files: str, compress_method: str = None) -> bool:
    """ Check if a sequence of files exist.


    :param tar_file: The TAR file.
    :param files: The list of file paths to check.
    :param compress_method: Force the compression or decompression method to use.
       By default, select from the file extension.
    :return: True if all the files exist, otherwise False.
    """
    compress_method = compress_method if compress_method else detect_compress_method(tar_file)
    with tarfile.open(tar_file, f'r:{compress_method}') as tar:
        filenames = tar.getnames()
    for file in files:
        if file not in filenames:
            return False
    return True
