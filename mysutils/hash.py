import hashlib
from json import dumps
from os import PathLike
from typing import Callable, Union


def file_digest(fileobj, digest, /, *, _bufsize=2**18):
    """Hash the contents of a file-like object. Returns a digest object.

    *fileobj* must be a file-like object opened for reading in binary mode.
    It accepts file objects from open(), io.BytesIO(), and SocketIO objects.
    The function may bypass Python's I/O and use the file descriptor *fileno*
    directly.

    *digest* must either be a hash algorithm name as a *str*, a hash
    constructor, or a callable that returns a hash object.
    """
    # On Linux we could use AF_ALG sockets and sendfile() to archive zero-copy
    # hashing with hardware acceleration.
    digest = digest()

    # binary file, socket.SocketIO object
    # Note: socket I/O uses different syscalls than file I/O.
    buf = bytearray(_bufsize)  # Reusable buffer to reduce allocations.
    view = memoryview(buf)
    while True:
        size = fileobj.readinto(buf)
        if size == 0:
            break  # EOF
        digest.update(view[:size])

    return digest


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
        content_hash = file_digest(file, method, _bufsize=buffer_size)
    return content_hash.hexdigest() if hex else content_hash.digest()
