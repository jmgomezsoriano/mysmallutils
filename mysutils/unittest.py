import unittest
from os import PathLike
from typing import Union

from mysutils.file import exist_files, not_exist_files, are_dir, not_are_dir, has_encoding


class FileTestCase(unittest.TestCase):
    """ Class for especial file tests. """

    def assertExists(self, *files: Union[str, PathLike, bytes]) -> None:
        """ Check if all of the files exist.

        :param files: The list of file paths to check.
        """
        self.assertTrue(exist_files(*files))

    def assertNotExists(self, *files: Union[str, PathLike, bytes]) -> None:
        """ Check if any of the files exist.

        :param files: The list of file paths to check.
        """
        self.assertTrue(not_exist_files(*files))

    def assertAreDir(self, *files: Union[str, PathLike, bytes]) -> None:
        """ Check if any of the files exist.

        :param files: The list of file paths to check.
        """
        self.assertTrue(are_dir(*files))

    def assertNotAreDir(self, *files: Union[str, PathLike, bytes]) -> None:
        """ Check if any of the files exist.

        :param files: The list of file paths to check.
        """
        self.assertTrue(not_are_dir(*files))

    def assertEncoding(self, *files: Union[str, PathLike, bytes], encoding: str) -> None:
        """ Check if all the files have that encoding.

        :param encoding: The file encoding.
        :param files: The list of file paths to check.
        """
        for file in files:
            self.assertTrue(has_encoding(file, encoding))

    def assertNotEncoding(self, *files: Union[str, PathLike, bytes], encoding: str) -> None:
        """ Check if all the files do not have that encoding.

        :param encoding: The file encoding to avoid.
        :param files: The list of file paths to check.
        """
        for file in files:
            self.assertFalse(has_encoding(file, encoding))


def main():
    unittest.main()
