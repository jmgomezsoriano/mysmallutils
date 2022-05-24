import unittest

from mysutils.service import replace_endpoint
from mysutils.fastapi import gen_service_help

from mysutils.file import read_file


class MyTestCase(unittest.TestCase):
    def test_replace_urls(self) -> None:
        body_html = ''.join(read_file('test/data/test_replace_url.html', True))
        replaced_html_1 = ''.join(read_file('test/data/test_replaced_url_01.html', True))
        self.assertEqual(replace_endpoint(body_html, '/api/replace'), replaced_html_1)
        replaced_html_2 = ''.join(read_file('test/data/test_replaced_url_02.html', True))
        self.assertEqual(replace_endpoint(body_html, '/api/delete'), replaced_html_2)
        replaced_html_3 = ''.join(read_file('test/data/test_replaced_url_03.html', True))
        self.assertEqual(replace_endpoint(body_html, '/help'), replaced_html_3)

    def test_gen_service_help(self) -> None:
        body_html = gen_service_help('Generate service help', 'test/data/test_replace_url.md', '', '/api/replace', '/api/delete',
                         '/help')
        replaced_html = ''.join(read_file('test/data/test_replaced_url_04.html', True))
        self.assertEqual(body_html, replaced_html)


if __name__ == '__main__':
    unittest.main()
