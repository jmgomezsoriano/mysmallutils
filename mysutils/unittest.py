import unittest

from mysutils.file import exist_files, not_exist_files, are_dir, not_are_dir


class FileTestCase(unittest.TestCase):
    """ Class for especial file tests. """

    def assertExists(self, *files: str) -> None:
        """ Check if all of the files exist.

        :param files: The list of file paths to check.
        """
        self.assertTrue(exist_files(*files))

    def assertNotExists(self, *files: str) -> None:
        """ Check if any of the files exist.

        :param files: The list of file paths to check.
        """
        self.assertTrue(not_exist_files(*files))

    def assertAreDir(self, *files: str) -> None:
        """ Check if any of the files exist.

        :param files: The list of file paths to check.
        """
        self.assertTrue(are_dir(*files))

    def assertNotAreDir(self, *files: str) -> None:
        """ Check if any of the files exist.

        :param files: The list of file paths to check.
        """
        self.assertTrue(not_are_dir(*files))


def main():
    unittest.main()
