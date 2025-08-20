from unittest.mock import patch
import unittest

from mysutils.cli import ask


class MyTestCase(unittest.TestCase):
    @patch('builtins.input', side_effect=['banana', '42', 'Y', '', '', 'yes', 'affirmative', 'Yes', 'yes'])
    def test_ask(self, mock_input) -> None:
        # Normal use
        resp = ask('Do you accept to marry me? [y/n]: ', ['y', 'n'])
        self.assertEqual(resp, 'y')
        # Default yes
        resp = ask('Do you accept to marry me? [Y/n]: ', ['y', 'n'], default='y')
        self.assertEqual(resp, 'y')
        # Default no
        resp = ask('Do you accept to marry me? [y/N]: ', ['y', 'n'], default='n')
        self.assertEqual(resp, 'n')
        # Variant yes
        resp = ask('Do you accept to marry me? [y/N]: ', {'y': ['yes', 'affirmative'], 'n': ['no']})
        self.assertEqual(resp, 'y')
        # Variant affirmative
        resp = ask('Do you accept to marry me? [y/n]: ', {'y': ['yes', 'affirmative'], 'n': ['no']})
        self.assertEqual(resp, 'y')
        # Variant affirmative
        resp = ask(
            'Do you accept to marry me? [y/n]: ',
            {'y': ['yes', 'affirmative'], 'n': ['no']},
            error_msg='Wrong answer! Try again.',
            ignore_case=False
        )
        self.assertEqual(resp, 'y')


if __name__ == '__main__':
    unittest.main()
