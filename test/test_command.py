import unittest
from platform import system

from mysutils.command import execute_command, split_arg_string


class MyTestCase(unittest.TestCase):
    def test_success_command(self) -> None:
        out, err = execute_command(['echo', 'This', 'is', 'a', 'test'])
        self.assertEqual(out, 'This is a test\n')
        self.assertEqual(err, '')

    def test_failure_command(self) -> None:
        out, err = execute_command(['ls', '-l', '*.py'])
        if system() == 'Windows':
            self.assertEqual(err, "'ls' is not recognized as an internal or external command,\n"
                                  "operable program or batch file.\n")
        else:
            self.assertEqual(err, 'ls: cannot access \'*.py\': No such file or directory\n')
        self.assertEqual(out, '')

    def test_split_command(self) -> None:
        self.assertListEqual(split_arg_string('echo This is a test'), ['echo', 'This', 'is', 'a', 'test'])
        self.assertListEqual(split_arg_string('echo -n "This is a test"'), ['echo', '-n', 'This is a test'])
        out, err = execute_command('echo This is a test')
        self.assertEqual(out, 'This is a test\n')
        out, err = execute_command('echo -n "This is a test"')
        if system() == 'Windows':
            self.assertEqual(out, '-n "This is a test"\n')
        else:
            self.assertEqual(out, 'This is a test')


if __name__ == '__main__':
    unittest.main()
