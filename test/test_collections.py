import unittest

from mysutils.collections import (
    dh, sh, head, del_keys, filter_lst, add_keys, mod_key, mod_keys, mod_value, mod_values, merge_tuples, merge_dicts,
    first_key_value, first_item, last_item, item, first_key, last_key, key, first_value, last_value, value,
    concat_lists, LRUDict
)
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

    def test_concat_lists(self) -> None:
        l1 = [1, 2, 3]
        l2 = [4, 5, 6, 1]
        l3 = [2, 6, 24]
        self.assertListEqual(concat_lists(l1, l2, l3), [1, 2, 3, 4, 5, 6, 1, 2, 6, 24])
        self.assertListEqual(concat_lists(l2, l3, l1), [4, 5, 6, 1, 2, 6, 24, 1, 2, 3])

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

    def test_merge_dict(self) -> None:
        lst = [{'a': 1, 'b': 10}, {'a': 2, 'b': 11}, {'a': 3, 'b': 12}]
        self.assertDictEqual(merge_dicts(lst), {'a': [1, 2, 3], 'b': [10, 11, 12]})

    def test_merge_tuples(self) -> None:
        lst = [(1, 10), (2, 11), (3, 12)]
        self.assertListEqual(merge_tuples(lst)[0], [1, 2, 3])
        self.assertListEqual(merge_tuples(lst)[1], [10, 11, 12])

    def test_dict_item(self) -> None:
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(first_item(d), ('a', 1))
        self.assertEqual(last_item(d), ('c', 3))
        self.assertEqual(first_key(d), 'a')
        self.assertEqual(last_key(d), 'c')
        self.assertEqual(first_value(d), 1)
        self.assertEqual(last_value(d), 3)
        self.assertEqual(item(d, 0), ('a', 1))
        self.assertEqual(item(d, 1), ('b', 2))
        self.assertEqual(item(d, 2), ('c', 3))
        with self.assertRaises(KeyError):
            item(d, -1)
        with self.assertRaises(KeyError):
            item(d, 3)
        self.assertEqual(key(d, 0), 'a')
        self.assertEqual(key(d, 1), 'b')
        self.assertEqual(key(d, 2), 'c')
        with self.assertRaises(KeyError):
            key(d, -1)
        with self.assertRaises(KeyError):
            key(d, 3)
        self.assertEqual(value(d, 0), 1)
        self.assertEqual(value(d, 1), 2)
        self.assertEqual(value(d, 2), 3)
        with self.assertRaises(KeyError):
            value(d, -1)
        with self.assertRaises(KeyError):
            value(d, 3)

    def test_search_key(self) -> None:
        lst = [{'a': 1, 'b': 2}, {'a': 10, 'c': 3}, {'a': 100, 'c': 30}]
        self.assertEqual(first_key_value(lst, 'a'), 1)
        self.assertEqual(first_key_value(lst, 'b'), 2)
        self.assertEqual(first_key_value(lst, 'c'), 3)
        with self.assertRaises(KeyError):
            first_key_value(lst, 'd')

    def test_convert_tuple_values(self) -> None:
        from mysutils.collections import convert_tuple_values

        row = ('5', '9.99', 'USB device')

        # Convert the first element in integer, the second in float and the third in string
        quantity, price, item = convert_tuple_values(row, int, float, str)
        self.assertEqual(quantity, 5)
        self.assertIsInstance(quantity, int)
        self.assertEqual(price, 9.99)
        self.assertIsInstance(price, float)
        self.assertEqual(item, 'USB device')
        self.assertIsInstance(item, str)
        with self.assertRaises(ValueError) as e:
            convert_tuple_values(row, int, float)
        self.assertEqual(str(e.exception), 'The tuple size must be as long as the list of types: 3 vs 2')
        with self.assertRaises(ValueError) as e:
            convert_tuple_values(row, int, float, str, float)
        self.assertEqual(str(e.exception), 'The tuple size must be as long as the list of types: 3 vs 4')

    def test_insertion_and_eviction(self):
        lru_dict = LRUDict(max_size=3)
        lru_dict['a'] = 1
        lru_dict['b'] = 2
        lru_dict['c'] = 3
        self.assertEqual(list(lru_dict.items()), [('a', 1), ('b', 2), ('c', 3)])

        lru_dict['d'] = 4
        self.assertEqual(list(lru_dict.items()), [('b', 2), ('c', 3), ('d', 4)])

    def test_access_order_update(self):
        lru_dict = LRUDict(max_size=3)
        lru_dict['a'] = 1
        lru_dict['b'] = 2
        lru_dict['c'] = 3

        _ = lru_dict['a']
        self.assertEqual(list(lru_dict.items()), [('b', 2), ('c', 3), ('a', 1)])

        lru_dict['d'] = 4
        self.assertEqual(list(lru_dict.items()), [('c', 3), ('a', 1), ('d', 4)])

    def test_update_existing_key(self):
        lru_dict = LRUDict(max_size=3)
        lru_dict['a'] = 1
        lru_dict['b'] = 2
        lru_dict['c'] = 3

        lru_dict['b'] = 20
        self.assertEqual(list(lru_dict.items()), [('a', 1), ('c', 3), ('b', 20)])

        lru_dict['d'] = 4
        self.assertEqual(list(lru_dict.items()), [('c', 3), ('b', 20), ('d', 4)])

    def test_eviction_order(self):
        lru_dict = LRUDict(max_size=2)
        lru_dict['a'] = 1
        lru_dict['b'] = 2

        lru_dict['a'] = 10
        self.assertEqual(list(lru_dict.items()), [('b', 2), ('a', 10)])

        lru_dict['c'] = 3
        self.assertEqual(list(lru_dict.items()), [('a', 10), ('c', 3)])

    def test_access_order_update_without_limit(self):
        lru_dict = LRUDict()
        lru_dict['a'] = 1
        lru_dict['b'] = 2
        lru_dict['c'] = 3

        _ = lru_dict['a']
        self.assertEqual(list(lru_dict.items()), [('b', 2), ('c', 3), ('a', 1)])

        lru_dict['d'] = 4
        self.assertEqual(list(lru_dict.items()), [('b', 2), ('c', 3), ('a', 1), ('d', 4)])

    def test_dict_update(self):
        lru_dict = LRUDict(3)
        lru_dict.update({'a': 1, 'b': 2, 'c': 3, 'd': 4})

        self.assertEqual(list(lru_dict.items()), [('b', 2), ('c', 3), ('d', 4)])


if __name__ == '__main__':
    unittest.main()
