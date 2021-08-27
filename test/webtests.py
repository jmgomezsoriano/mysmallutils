import unittest

from mysutils.request import json_post


class MyTestCase(unittest.TestCase):
    def test_post(self) -> None:
        d = json_post('https://postman-echo.com/post', {"msg": "Hello world!"})
        self.assertDictEqual(d['data'], {'msg': 'Hello world!'})
        self.assertDictEqual(d['json'], {'msg': 'Hello world!'})
        self.assertEqual(d['url'], 'https://postman-echo.com/post')

    def test_something(self):
        # TODO
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
