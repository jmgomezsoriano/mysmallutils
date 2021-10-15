import unittest

from mysutils.collections import dh, sh, head, del_keys
from mysutils.collections import list_union


class MyTestCase(unittest.TestCase):
    def test_dh(self) -> None:
        d = {i: chr(97 + i) for i in range(26)}
        d2 = dh(d)
        self.assertEqual(len(d2), 10)
        self.assertDictEqual(d2, {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j'})

    def test_sh(self) -> None:
        s = {chr(97 + i) for i in range(26)}
        s2 = sh(s, 5)
        self.assertEqual(len(s2), 5)
        self.assertSetEqual(s2, {'d', 'b', 'a', 'c', 'e'})

    def test_head(self) -> None:
        dict1 = {i: chr(97 + i) for i in range(26)}
        self.assertDictEqual(head(dict1),
                             {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j'})
        self.assertEqual(len(head(dict1)), 10)
        self.assertDictEqual(head(dict1, 5), {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'})
        self.assertEqual(len(head(dict1, 5)), 5)
        set1 = {chr(97 + i) for i in range(26)}
        self.assertSetEqual(head(set1), {'f', 'd', 'j', 'a', 'b', 'e', 'h', 'i', 'c', 'g'})
        self.assertEqual(len(head(set1)), 10)
        self.assertSetEqual(head(set1, 5), {'d', 'a', 'b', 'e', 'c'})
        self.assertEqual(len(head(set1, 5)), 5)

    def test_list_union(self) -> None:
        l1 = [1, 2, 3]
        l2 = [4, 5, 6, 1]
        l3 = [2, 6, 24]
        self.assertListEqual(list_union(l1, l2, l3), [1, 2, 3, 4, 5, 6, 24])
        self.assertListEqual(list_union(l1, l3, l2), [1, 2, 3, 6, 24, 4, 5])

    def test_del_dict_item(self) -> None:
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assertDictEqual(d, del_keys(d.copy()))
        self.assertDictEqual({'a': 1, 'b': 2}, del_keys(d.copy(), 'c'))
        self.assertDictEqual({'b': 2}, del_keys(d.copy(), ['a', 'c']))
        self.assertDictEqual({}, del_keys(d.copy(), ['a', 'b', 'c']))
        self.assertDictEqual(d, del_keys(d.copy(), 'd'))
        self.assertDictEqual({'a': 1, 'c': 3}, del_keys(d.copy(), ['b', 'd', 'e']))
        with self.assertRaises(KeyError):
            self.assertDictEqual(d, del_keys(d.copy(), 'd', False))
        with self.assertRaises(KeyError):
            self.assertDictEqual({'a': 1, 'c': 3}, del_keys(d.copy(), ['b', 'd', 'e'], False))
        self.assertDictEqual({'a': 1, 'b': 2, 'c': 3}, d)


if __name__ == '__main__':
    unittest.main()
