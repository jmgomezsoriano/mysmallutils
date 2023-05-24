import unittest

from mysutils.text import clean_text, remove_urls, AnsiCodes, markup, color, bg_color, un_color, replace_urls, get_urls, \
    is_url, has_url


class MyTestCase(unittest.TestCase):
    def test_clean_url(self) -> None:
        text = 'This is a test!\n     Clean punctuation symbols and urls like this: ' \
               'https://example.com/my_space/user?a=b&c=3#first ' \
               'https://example.com/your_space/user#first'
        self.assertEqual(remove_urls(text), 'This is a test!\n     Clean punctuation symbols and urls like this:  ')
        self.assertEqual(remove_urls(text, r'my_space/user\?a=b&c=3#first'),
                         'This is a test!\n     Clean punctuation symbols and urls like this:  '
                         'https://example.com/your_space/user#first')

    def test_replace_url(self) -> None:
        text = 'This is a test!\n     Clean punctuation symbols and urls like this: ' \
               'https://example.com/my_space/user ' \
               'https://example.com/your_space'
        self.assertEqual(replace_urls(text, 'https://hello.com'),
                         'This is a test!\n     Clean punctuation symbols and urls like this: '
                         'https://hello.com https://hello.com')
        self.assertEqual(replace_urls(text, 'https://hello.com', r'my_space/user'),
                         'This is a test!\n     Clean punctuation symbols and urls like this: '
                         'https://hello.com https://example.com/your_space')

    def test_clean_text(self) -> None:
        text = 'This is a test!\n     Clean punctuation symbols and urls like this: ' \
               'https://example.com/my_space/user?a=b&c=3#first ' \
               'https://example.com/my_space/user#first'
        self.assertEqual(clean_text(text), 'this is a test clean punctuation symbols and urls like this')
        self.assertEqual(clean_text(text, False), 'This is a test Clean punctuation symbols and urls like this')
        self.assertEqual(clean_text(text, False, False),
                         'This is a test Clean punctuation symbols and urls like this https example com my space user '
                         'a b c 3 first https example com my space user first')

    def test_get_urls(self) -> None:
        text = 'This is a test!\n     Clean punctuation symbols and urls like this: ' \
               'https://example.com/my_space/user?a=b&c=3#first ' \
               'https://example.com/your_space/user#first\n' \
               'More urls:\n' \
               'https://example.com/my_space/user\n' \
               'https://example.com/your_space\n' \
               '[Markdown](https://pepe@example.com:3306/documents/exportation.pdf?id=3&b=2#1234' \
               ')[)](undefined,) style url.\n' \
               'git+https://github.com/huggingface/peft.git\n' \
               'www.example.com on 10.05.2015'

        self.assertListEqual(get_urls(text), [
            'https://example.com/my_space/user?a=b&c=3#first',
            'https://example.com/your_space/user#first',
            'https://example.com/my_space/user',
            'https://example.com/your_space',
            'https://pepe@example.com:3306/documents/exportation.pdf?id=3&b=2#1234',
            'git+https://github.com/huggingface/peft.git'
        ])

        self.assertListEqual(get_urls(text, protocol=False), [
            'https://example.com/my_space/user?a=b&c=3#first',
            'https://example.com/your_space/user#first',
            'https://example.com/my_space/user',
            'https://example.com/your_space',
            'https://pepe@example.com:3306/documents/exportation.pdf?id=3&b=2#1234',
            'git+https://github.com/huggingface/peft.git',
            'www.example.com',
            '10.05.2015'
        ])

    def test_check_url(self) -> None:
        text = 'This is a test!\n     Clean punctuation symbols and urls like this:'\
               'https://example.com/my_space/user?a=b&c=3#first'\
               'https://example.com/your_space/user#first\n' \
               'More urls:\n' \
               'https://example.com/my_space/user\n' \
               'https://example.com/your_space\n' \
               '[Markdown](https://pepe@example.com:3306/documents/exportation.pdf?id=3&b=2#1234' \
               ')[)](undefined,) style url.\n' \
               'git+https://github.com/huggingface/peft.git'

        self.assertTrue(is_url('https://example.com/my_space/user?a=b&'))
        self.assertFalse(is_url(text))
        self.assertTrue(has_url('https://example.com/my_space/user?'))
        self.assertTrue(has_url(text))
        self.assertFalse(has_url('Another text without urls.'))

    def test_markup(self) -> None:
        text = markup('This is a text with effects', AnsiCodes.YELLOW, AnsiCodes.ITALIC, AnsiCodes.SLOW_BLINK)
        self.assertEqual(text, '\033[33m\033[3m\033[5mThis is a text with effects\033[0m')
        text = markup('This is a text with effects', 'yellow', 'italic', 'SLOW_BLINK')
        self.assertEqual(text, '\033[33m\033[3m\033[5mThis is a text with effects\033[0m')
        self.assertEqual(markup('Hello', color(5, 50, 240)), '\x1b[38;2;5;50;240mHello\x1b[0m')
        self.assertEqual(markup('Hello', bg_color(5, 50, 240)), '\x1b[48;2;5;50;240mHello\x1b[0m')
        self.assertEqual(markup('Hello', AnsiCodes.UNDERLINE, un_color(5, 50, 240)),
                         '\x1b[4m\x1b[58;2;5;50;240mHello\x1b[0m')
        self.assertEqual(markup('Hello', AnsiCodes.UNDERLINE, AnsiCodes.UN_BRIGHT_CYAN),
                         '\x1b[4m\x1b[58;2;85;255;255mHello\x1b[0m')
        self.assertEqual('This is a ' + markup('text', AnsiCodes.UNDERLINE, color(255, 255, 20),
                                               bg_color(60, 60, 60), un_color(80, 80, 255)) + ' with effects.',
                         'This is a \x1b[4m\x1b[38;2;255;255;20m\x1b[48;2;60;60;60m\x1b[58;2;80;80;255mtext\x1b[0m '
                         'with effects.')


if __name__ == '__main__':
    unittest.main()
