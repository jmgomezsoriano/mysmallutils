import unittest

from mysutils.collections import dh, sh, head, del_keys, filter_lst, add_keys, mod_key, mod_keys, mod_value, mod_values
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
        self.assertDictEqual({'b': 2}, del_keys(d.copy(), 'a', 'c'))
        self.assertDictEqual({}, del_keys(d.copy(), 'a', 'b', 'c'))
        self.assertDictEqual(d, del_keys(d.copy(), 'd'))
        self.assertDictEqual({'a': 1, 'c': 3}, del_keys(d.copy(), 'b', 'd', 'e'))
        with self.assertRaises(KeyError):
            self.assertDictEqual(d, del_keys(d.copy(), 'd', ignore_errors=False))
        with self.assertRaises(KeyError):
            self.assertDictEqual({'a': 1, 'c': 3}, del_keys(d.copy(), 'b', 'd', 'e', ignore_errors=False))
        self.assertDictEqual({'a': 1, 'b': 2, 'c': 3}, d)

    def test_add_dict_item(self) -> None:
        d = {'b': 2}
        self.assertDictEqual({'a': 1, 'b': 2, 'c': 3}, add_keys(d, a=1, c=3))
        self.assertDictEqual({'a': 1, 'b': 2, 'c': 3}, add_keys(d, a=1, b=2, c=3))
        with self.assertRaises(KeyError):
            self.assertDictEqual({'a': 1, 'b': 2, 'c': 3}, add_keys(d, a=1, b=2, c=3, modify=False))

    def test_filters(self) -> None:
        lst = [i for i in range(1, 20)]
        self.assertListEqual([1, 2, 3, 4], filter_lst(lst, 4))
        self.assertListEqual([2, 3, 4], filter_lst(lst, 3, 1))
        self.assertListEqual([3, 5], filter_lst(lst, 5, 1, lambda x: x % 2 == 1))

    def test_mod_dicts(self) -> None:
        # Modify just one key: name by firstname
        d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
        self.assertDictEqual(mod_key(d, 'name', 'firstname'),
                             {'firstname': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'})
        # Modify several keys: name by firstname and lastname by familyname
        d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
        self.assertDictEqual(mod_keys(d, name='firstname', lastname='familyname'),
                             {'firstname': 'Pablo', 'familyname': 'Escobar', 'email': 'pabloescobar@example.com'})
        # Modify two values concatenating commands
        d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
        self.assertDictEqual(mod_value(mod_value(d, 'name', 'Jhon'), 'lastname', 'Smith'),
                             {'name': 'Jhon', 'lastname': 'Smith', 'email': 'pabloescobar@example.com'})
        # Modify two values with just one sentence
        d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
        self.assertDictEqual(mod_values(d, name='Jhon', lastname='Smith'),
                             {'name': 'Jhon', 'lastname': 'Smith', 'email': 'pabloescobar@example.com'})
        # Add the key 'country', remove 'email', change 'name' by 'firstname' and change the 'lastname' value:
        d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
        self.assertDictEqual(
            mod_value(mod_key(del_keys(add_keys(d, country='Colombia'),
                                       'email'), 'name', 'firstname'), 'lastname', 'Smith'),
            {'firstname': 'Pablo', 'lastname': 'Smith', 'country': 'Colombia'})


if __name__ == '__main__':
    unittest.main()
