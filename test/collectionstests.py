import unittest

from mysutils.collections import dh, sh


class MyTestCase(unittest.TestCase):
    def test_dh(self):
        d = {i: chr(97 + i) for i in range(26)}
        d2 = dh(d)
        self.assertEqual(len(d2), 10)
        self.assertDictEqual(d2, {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j'})  # add assertion here
        s = {chr(97 + i) for i in range(26)}
        s2 = sh(s, 5)
        self.assertEqual(len(s2), 5)
        self.assertSetEqual(s2, {'d', 'b', 'a', 'c', 'e'})


if __name__ == '__main__':
    unittest.main()
