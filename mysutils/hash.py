import hashlib
from os import PathLike
from typing import Callable, Union


def file_md5(filename: Union[str, PathLike, bytes], hex: bool = True, buffer_size: int = 65536) -> (str | bytes):
    """ Generate a md5 hash from the content of a file.

    :param filename: The file path.
    :param hex: If the result is in hexadecimal format or not.
    :param buffer_size: The buffer size to read the file.
    :return: The file content md5 hash in the specified format.
    """
    return _hash_file(filename, hex, buffer_size, hashlib.md5)


def file_sha1(filename: Union[str, PathLike, bytes], hex: bool = True, buffer_size: int = 65536) -> (str | bytes):
    """ Generate a sha1 hash from the content of a file.

    :param filename: The file path.
    :param hex: If the result is in hexadecimal format or not.
    :param buffer_size: The buffer size to read the file.
    :return: The file content sha1 hash in the specified format.
    """
    return _hash_file(filename, hex, buffer_size, hashlib.sha1)


def file_sha224(filename: Union[str, PathLike, bytes], hex: bool = True, buffer_size: int = 262144) -> (str | bytes):
    """ Generate a sha224 hash from the content of a file.

    :param filename: The file path.
    :param hex: If the result is in hexadecimal format or not.
    :param buffer_size: The buffer size to read the file.
    :return: The file content sha224 hash in the specified format.
    """
    return _hash_file(filename, hex, buffer_size, hashlib.sha224)


def file_sha256(filename: Union[str, PathLike, bytes], hex: bool = True, buffer_size: int = 65536) -> (str | bytes):
    """ Generate a sha256 hash from the content of a file.

    :param filename: The file path.
    :param hex: If the result is in hexadecimal format or not.
    :param buffer_size: The buffer size to read the file.
    :return: The file content sha256 hash in the specified format.
    """
    return _hash_file(filename, hex, buffer_size, hashlib.sha256)


def file_sha384(filename: Union[str, PathLike, bytes], hex: bool = True, buffer_size: int = 262144) -> (str | bytes):
    """ Generate a sha384 hash from the content of a file.

    :param filename: The file path.
    :param hex: If the result is in hexadecimal format or not.
    :param buffer_size: The buffer size to read the file.
    :return: The file content sha384 hash in the specified format.
    """
    return _hash_file(filename, hex, buffer_size, hashlib.sha384)


def file_sha512(filename: Union[str, PathLike, bytes], hex: bool = True, buffer_size: int = 262144) -> (str | bytes):
    """ Generate a sha512 hash from the content of a file.

    :param filename: The file path.
    :param hex: If the result is in hexadecimal format or not.
    :param buffer_size: The buffer size to read the file.
    :return: The file content sha512 hash in the specified format.
    """
    return _hash_file(filename, hex, buffer_size, hashlib.sha512)


def _hash_file(
        filename: Union[str, PathLike, bytes],
        hex: bool = True,
        buffer_size: int = 262144,
        method: Callable = hashlib.md5
) -> (str | bytes):
    """ Generate a hash from the content a file with the specified hash method.

    :param filename: The file path.
    :param hex: If the result is in hexadecimal format or not.
    :param buffer_size: The buffer size to read the file.
    :param method: The hash method, for example, hashlib.md5 or hashlib.sha1 (without parenthesis).

    :return: The file content hash in the specified format.
    """
    # hash_method = method()
    with open(filename, 'rb') as file:
        content_hash = hashlib.file_digest(file, method, _bufsize=buffer_size)
    return content_hash.hexdigest() if hex else content_hash.digest()
