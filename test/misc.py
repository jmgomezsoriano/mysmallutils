import unittest

from mysutils.misc import conditional


def my_func(a: int, b: str, **kwargs) -> str:
    return f'Intent {a} of {b} for {kwargs["c"]}'


class MyTestCase(unittest.TestCase):
    def test_conditional(self):
        self.assertEqual(conditional(my_func, 3 > 2, 1, 'apple', c='Lucas'), 'Intent 1 of apple for Lucas')
        self.assertIsNone(conditional(my_func, 3 < 2, 1, 'apple', c='Lucas'), 'Intent 1 of apple for Lucas')


if __name__ == '__main__':
    unittest.main()
