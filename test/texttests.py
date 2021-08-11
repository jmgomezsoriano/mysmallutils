import unittest

from mysutils.text import clean_text, remove_urls


class MyTestCase(unittest.TestCase):
    def test_clean_url(self) -> None:
        text = 'This is a test!\n     Clean punctuation symbols and urls like this: ' \
               'https://example.com/my_space/user?a=b&c=3#first ' \
               'https://example.com/my_space/user#first'
        self.assertEqual(remove_urls(text), 'This is a test!\n     Clean punctuation symbols and urls like this:  ')

    def test_clean_text(self):
        text = 'This is a test!\n     Clean punctuation symbols and urls like this: ' \
               'https://example.com/my_space/user?a=b&c=3#first ' \
               'https://example.com/my_space/user#first'
        self.assertEqual(clean_text(text), 'this is a test clean punctuation symbols and urls like this')
        self.assertEqual(clean_text(text, False), 'This is a test Clean punctuation symbols and urls like this')
        self.assertEqual(clean_text(text, False, False),
                         'This is a test Clean punctuation symbols and urls like this https example com my space user '
                         'a b c 3 first https example com my space user first')


if __name__ == '__main__':
    unittest.main()
