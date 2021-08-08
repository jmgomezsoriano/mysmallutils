import unittest

from mysutils.command import execute_command


class MyTestCase(unittest.TestCase):
    def test_success_command(self):
        out, err = execute_command(['echo', 'This', 'is', 'a', 'test'])
        self.assertEqual(out, 'This is a test\n')
        self.assertEqual(err, '')

    def test_failure_command(self):
        out, err = execute_command(['ls', '-l', '*.py'])
        print(out, err)
        self.assertEqual(err, 'ls: cannot access \'*.py\': No such file or directory\n')
        self.assertEqual(out, '')


if __name__ == '__main__':
    unittest.main()
