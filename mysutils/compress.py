import gzip
import tarfile
from typing import List
from os.path import basename


def create_tar(fname: str, files: List[str], compress_method: str = 'bz2'):
    """
    Create a tar file with a given list of files.
    :param fname: The name of the tar file.
    :param files: The list of file paths to include in the tar file.
    :param compress_method: The method to use to compress the file. Available methods: gz, bz2. By default bz2.
    """
    with tarfile.open(fname, f'w:{compress_method}') as tar:
        for file in files:
            tar.add(file, basename(file))


def gzip_decompress(input_file: str, output_file: str) -> None:
    with open(output_file, 'wb') as writer:
        with gzip.open(input_file, 'rb') as reader:
            for chunk in reader:
                writer.write(chunk)
