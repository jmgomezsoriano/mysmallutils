import gzip
import json
import pickle
import tarfile
from os import makedirs
from tarfile import TarInfo
from os.path import basename, isdir, join, exists, splitext, dirname
from typing import List, Any

from typing.io import IO

# Import tqdm if it is installed, otherwise a dummy tqdm function is used.
try:
    from tqdm.auto import tqdm
except ModuleNotFoundError as e:
    def tqdm(obj: Any) -> Any:
        return obj

# Available tar compress methods
COMPRESS_METHODS = {'gz', 'bz2', 'xz'}


def create_tar(filename: str, *files: str, verbose: bool = False) -> None:
    """
    Create a tar file with a given list of files. If the filename has any of these extensions 'gz', 'bz2' or 'xz',
      then the tar file will be compressed with the specify method.
    :param filename: The name of the tar file.
    :param files: The list of file paths to include in the tar file.
    :param verbose: if True, show a bar progress.
    """
    compress_method = detect_compress_method(filename)
    with tarfile.open(filename, f'w:{compress_method}') as tar:
        for file in tqdm(files, desc='Creating tar file', disable=not verbose):
            tar.add(file, basename(file))


def detect_compress_method(filename: str) -> str:
    """ Detecting the compression method based on the extension of the filename.

    :param filename: The file path to the tar file.
    :return: 'gz', 'bz2' or 'xz' if the file is compressed by one of these methods, otherwise an empty string.
    """
    extension = splitext(filename)[1]
    return extension[1:].lower() if extension[1:].lower() in COMPRESS_METHODS else ''


def open_tar_file(tar_file: str, filename: str) -> IO:
    """ Open a tar file and return a IO stream to the file.

    :param tar_file: The path to the tar file-.
    :param filename: The path inside of the tar to the file to extract.
    :return: An IO stream.
    """
    compress_method = detect_compress_method(tar_file)
    tar = tarfile.open(tar_file, f'r:{compress_method}')
    file = tar.extractfile(filename)
    old_close = file.close

    def close():
        tar.close()
        old_close()

    file.close = close
    return file


def load_tar_json(tar_file: str, filename: str) -> Any:
    """ Load an object from a JSON file stored in a tar file.

    :param tar_file: The path to the tar file-.
    :param filename: The path inside of the tar to the file to extract.
    :return: The loaded object.
    """
    with open_tar_file(tar_file, filename) as file:
        if filename.lower().endswith('.gz'):
            return json.load(gzip.open(file))
        return json.load(file)


def load_tar_pickle(tar_file: str, filename: str) -> Any:
    """ Load an object from a pickle file stored in a tar file.

    :param tar_file: The path to the tar file-.
    :param filename: The path inside of the tar to the file to extract.
    :return: The loaded object.
    """
    with open_tar_file(tar_file, filename) as file:
        if filename.lower().endswith('.gz'):
            return pickle.load(gzip.open(file))
        return pickle.load(file)


def list_tar(tar_file: str) -> List[TarInfo]:
    """ Obtain a list with the information of each file or directory of a tar file.

    :param tar_file: The path to the tar file.
    :return: A list of TarInfo instances.
    """
    compress_method = detect_compress_method(tar_file)
    with tarfile.open(tar_file, f'r:{compress_method}') as tar:
        return tar.getmembers()


def extract_tar_file(tar_file: str, dest: str, filename: str) -> None:
    """ Extract a file inside of a tar archive.

    :param tar_file: The path to the tar file.
    :param dest: The file or folder where the tar archive should be extracted.
    :param filename: The relative path inside of the tar file to extract.
    """
    compress_method = detect_compress_method(tar_file)
    dest = join(dest, filename) if isdir(dest) else dest
    with tarfile.open(tar_file, f'r:{compress_method}') as tar:
        with tar.extractfile(filename) as reader:
            if not exists(dirname(dest)):
                makedirs(dirname(dest))
            with open(dest, 'wb') as writer:
                for chunk in reader:
                    writer.write(chunk)


def extract_tar_files(tar_file: str, dest: str, *files: str, force: bool = False) -> None:
    """ Extract a file inside of a tar archive.

    :param tar_file: The path to the tar file.
    :param dest: The folder where the tar archive should be extracted.
    :param files: The relative path inside of the tar file to extract.
    :param force: If True, create the destination directory if it doesn't exist.
      If files is not given, then extract all the files.
    """
    if not exists(dest) and force:
        makedirs(dest)
    if not isdir(dest):
        raise ValueError(f'The destination is not an existing folder.')
    files = files if files else [file.path for file in list_tar(tar_file)]
    for file in files:
        extract_tar_file(tar_file, dest, file)


def extract_tar(tar_file: str, dest: str, force: bool = False, verbose: bool = False) -> None:
    """ Extract all the files inside of a tar file in the specified directory.

    :param tar_file: The tar file to extract.
    :param dest: The destination directory.
    :param force: If True, create the destination directory if it doesn't exist.
    :param verbose: If verbose, show the progress bar.
    """
    if not exists(dest) and force:
        makedirs(dest)
    if not exists(dest):
        raise FileNotFoundError(f'The folder "{dest}" does not exists. Create it or put the parameter force to True.')

    files = list_tar(tar_file)
    for file in tqdm(files, desc='Extracting files', disable=not verbose):
        if file.isdir():
            makedirs(join(dest, file.path))
        else:
            extract_tar_file(tar_file, file.path, dest)
