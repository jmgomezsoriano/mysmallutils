import tarfile
from os import makedirs
from tarfile import TarInfo
from os.path import basename, isdir, join, exists, splitext
from typing import List, Any
from typing.io import IO

try:
    from tqdm.auto import tqdm
except ModuleNotFoundError as e:
    def tqdm(obj: Any) -> Any:
        return obj

COMPRESS_METHODS = {'gz', 'bz2', 'xz'}


def create_tar(filename: str, *files: str, verbose: bool = False) -> None:
    """
    Create a tar file with a given list of files.
    :param filename: The name of the tar file.
    :param files: The list of file paths to include in the tar file.
    """
    compress_method = detect_compress_method(filename)
    with tarfile.open(filename, f'w:{compress_method}') as tar:
        for file in tqdm(files, desc='Creating tar file', disable=not verbose):
            tar.add(file, basename(file))


def detect_compress_method(filename):
    extension = splitext(filename)[1]
    compress_method = extension[1:].lower() if extension[1:].lower() in COMPRESS_METHODS else ''
    return compress_method


def open_tar_file(tar_file: str, filename: str) -> IO:
    compress_method = detect_compress_method(tar_file)
    with tarfile.open(tar_file, f'r:{compress_method}') as tar:
        return tar.extractfile(filename)


def list_tar(tar_file: str) -> List[TarInfo]:
    compress_method = detect_compress_method(tar_file)
    with tarfile.open(tar_file, f'r:{compress_method}') as tar:
        return tar.getmembers()


def extract_tar_file(tar_file: str, filename: str, dest: str) -> None:
    compress_method = detect_compress_method(tar_file)
    dest = join(dest, filename) if isdir(dest) else dest
    with tarfile.open(tar_file, f'r:{compress_method}') as tar:
        with tar.extractfile(filename) as reader:
            with open(dest, 'wb') as writer:
                for chunk in reader:
                    writer.write(chunk)


def extract_tar(tar_file: str, dest: str, force: bool = False,
                verbose: bool = False) -> None:
    if force:
        makedirs(dest)
    if not exists(dest):
        raise FileNotFoundError(f'The folder "{dest}" does not exists. Create it or put the parameter force to True.')

    files = list_tar(tar_file)
    for file in tqdm(files, desc='Extracting files', disable=not verbose):
        if file.isdir():
            makedirs(join(dest, file.path))
        else:
            extract_tar_file(tar_file, file.path, dest)
