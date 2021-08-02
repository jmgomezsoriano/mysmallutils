import gzip
import tarfile
from os.path import basename


def create_tar(fname: str, *files: str, compress_method: str = 'bz2'):
    """
    Create a tar file with a given list of files.
    :param fname: The name of the tar file.
    :param files: The list of file paths to include in the tar file.
    :param compress_method: The method to use to compress the file. Available methods: "gz", "bz2". By default bz2.
    """
    with tarfile.open(fname, f'w:{compress_method}') as tar:
        for file in files:
            tar.add(file, basename(file))


def gzip_decompress(input_file: str, output_file: str) -> None:
    """ Decompress a file using gzip compression.
    :param input_file: The file to compress.
    :param output_file: The compressed file with all the information of the input file.
    """
    with open(output_file, 'wb') as writer:
        with gzip.open(input_file, 'rb') as reader:
            for chunk in reader:
                writer.write(chunk)


def gzip_compress(input_file: str, output_file: str) -> None:
    """ Compress a file using gzip compression.
    :param input_file: The file to compress.
    :param output_file: The compressed file with all the information of the input file.
    """
    with gzip.open(output_file, 'wb') as writer:
        with open(input_file, 'rb') as reader:
            for chunk in reader:
                writer.write(chunk)
