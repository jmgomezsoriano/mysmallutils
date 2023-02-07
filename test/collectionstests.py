import time
import unittest
from datetime import datetime

from mysutils.collections import dh, sh, head, del_keys, filter_lst, add_keys, mod_key, mod_keys, mod_value, mod_values, \
    merge_tuples, merge_dicts, first_key_value, first_item, last_item, item, first_key, last_key, key, first_value, \
    last_value, value, concat_lists, OrderedSet
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

    def test_ordered_set_add(self):
        s = OrderedSet()
        s.add(1)
        self.assertEqual(len(s), 1)
        self.assertTrue(1 in s)
        s = OrderedSet({5, 4, 3})
        s.add(8)
        self.assertSetEqual(s, {8, 5, 4, 3})

    def test_ordered_set_time(self):
        s = OrderedSet()
        s.add(1)
        time.sleep(0.5)
        s.add(8)
        self.assertIsInstance(s[1], datetime)
        self.assertLess(s.time(1), s.time(8))
        self.assertLess(s[1], s[8])
        self.assertGreater(s.time(8), s.time(1))
        time.sleep(0.1)
        t1 = datetime.now()
        for item in {2, 3, 4, 5, 6}:
            s.add(item)
            time.sleep(0.1)
        before_set = s.before(t1)
        self.assertSetEqual(before_set, {8, 1})
        for item in before_set:
            self.assertEqual(s[item], before_set[item])
        after_set = s.after(t1)
        self.assertSetEqual(after_set, {2, 3, 4, 5, 6})
        for item in after_set:
            self.assertEqual(s[item], after_set[item])
        self.assertSetEqual(s.before(s[8]), {1})
        self.assertSetEqual(s.until(s[8]), {1, 8})
        self.assertSetEqual(s.after(s[3]), {4, 5, 6})
        self.assertSetEqual(s.since(s[3]), {3, 4, 5, 6})

    def test_ordered_set_first(self) -> None:
        s = OrderedSet()
        s.add(1)
        self.assertEqual(s.first(), 1)
        s.add(2)
        self.assertEqual(s.first(), 1)
        s.add(3)
        self.assertEqual(s.pop(), 1)
        self.assertEqual(s.first(), 2)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.first(), 3)
        self.assertEqual(s.pop(), 3)
        with self.assertRaises(KeyError):
            s.first()


    def test_ordered_set_remove(self):
        s = OrderedSet([1, 2, 3])
        s.remove(2)
        self.assertEqual(len(s), 2)
        self.assertSetEqual(s, {1, 3})
        time.sleep(0.1)
        s.add(4)
        time.sleep(0.1)
        s.add(5)
        copy_set = s.copy()
        s.remove_before(s[4])
        self.assertSetEqual(s, {4, 5})
        s = copy_set.copy()
        s.remove_after(s[4])
        self.assertSetEqual(s, {1, 3, 4})
        s = copy_set.copy()
        s.remove_until(s[4])
        self.assertSetEqual(s, {5})
        s = copy_set.copy()
        s.remove_since(s[4])
        self.assertSetEqual(s, {1, 3})
        s = OrderedSet([1, 2, 3, 4, 5])
        s.remove_items([2, 3, 4])
        self.assertSetEqual(s, {1, 5})

    def test_ordered_set_discard(self):
        s = OrderedSet([1, 2, 3])
        s.discard(2)
        self.assertEqual(len(s), 2)
        self.assertSetEqual(s, {1, 3})

    def test_ordered_set_pop(self) -> None:
        s = OrderedSet([24, 32, 18, 1, 6])
        self.assertEqual(s.pop(), 24)
        self.assertSetEqual(s, {32, 18, 1, 6})
        self.assertEqual(s.pop(last=True), 6)
        self.assertSetEqual(s, {32, 18, 1})

    def test_ordered_set_update(self) -> None:
        s = OrderedSet([24, 32, 18, 1, 6])
        s.update([1, 2, 3])
        self.assertSetEqual(s, {1, 2, 3, 6, 18, 24, 32})

    def test_ordered_set_clear(self):
        s = OrderedSet([1, 2, 3])
        s.clear()
        self.assertEqual(len(s), 0)
        self.assertSetEqual(s, set())

    def test_ordered_set_copy(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = s1.copy()
        self.assertEqual(len(s1), len(s2))
        self.assertSetEqual(s1, s2)

    def test_ordered_set_difference(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([2, 3, 4])
        s3 = {1, 2, 3}
        s4 = {2, 3, 4}
        diff = s1.difference(s2)
        self.assertEqual(len(diff), 1)
        self.assertSetEqual(diff, {1})
        diff = s1 - s2
        self.assertEqual(len(diff), 1)
        self.assertSetEqual(diff, {1})
        diff = s1 - s4
        self.assertEqual(len(diff), 1)
        self.assertSetEqual(diff, {1})
        diff = s3 - s2
        self.assertEqual(len(diff), 1)
        self.assertSetEqual(diff, {1})

    def test_ordered_set_difference_update(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([2, 3, 4])
        s1.difference_update(s2)
        self.assertEqual(len(s1), 1)
        self.assertSetEqual(s1, {1})
        s1 = OrderedSet([1, 2, 3])
        s1.difference_update({2, 3, 4})
        self.assertEqual(len(s1), 1)
        self.assertSetEqual(s1, {1})
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([2, 3, 4])
        s2.difference_update(s1)
        self.assertEqual(len(s2), 1)
        self.assertSetEqual(s2, {4})
        s1 = OrderedSet([1, 2, 3])
        s2 = {2, 3, 4}
        s2.difference_update(s1)
        self.assertEqual(len(s2), 1)
        self.assertSetEqual(s2, {4})

    def test_ordered_set_intersection(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([2, 3, 4])
        intersect = s1.intersection(s2)
        self.assertEqual(len(intersect), 2)
        self.assertSetEqual(intersect, {2, 3})
        intersect = s1 & s2
        self.assertEqual(len(intersect), 2)
        self.assertSetEqual(intersect, {2, 3})
        intersect = s2 & s1
        self.assertEqual(len(intersect), 2)
        self.assertSetEqual(intersect, {2, 3})
        intersect = s1 & {2, 3, 4}
        self.assertEqual(len(intersect), 2)
        self.assertSetEqual(intersect, {2, 3})
        intersect = {1, 2, 3} & s2
        self.assertEqual(len(intersect), 2)
        self.assertSetEqual(intersect, {2, 3})

    def test_ordered_set_intersection_update(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([2, 3, 4])
        s1.intersection_update(s2)
        self.assertEqual(len(s1), 2)
        self.assertSetEqual(s1, {2, 3})

    def test_ordered_set_union(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([3, 4, 5])
        s3 = set(iter([1, 2, 3]))
        s4 = set(iter([3, 4, 5]))
        union = s1.union(s2)
        self.assertSetEqual(union, {1, 2, 3, 4, 5})
        self.assertTrue(union != {1, 2, 3, 4, 5, 6})
        union = s1 | s2
        self.assertTrue(union == {1, 2, 3, 4, 5})
        self.assertTrue(union != {1, 2, 3, 4, 5, 6})
        union = s1 | s4
        self.assertTrue(union == {1, 2, 3, 4, 5})
        self.assertTrue(union != {1, 2, 3, 4, 5, 6})
        union = s4.union(s1)
        self.assertTrue(union == {1, 2, 3, 4, 5})
        self.assertTrue(union != {1, 2, 3, 4, 5, 6})
        union = s3.union(s4)
        self.assertSetEqual(union, {1, 2, 3, 4, 5})
        self.assertTrue(union != {1, 2, 3, 4, 5, 6})

    def test_ordered_set_issubset(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([1, 2, 3, 4, 5, 6])
        self.assertTrue(s1.issubset(s2))
        self.assertFalse(s2.issubset(s1))
        self.assertTrue(s1 <= s2)
        self.assertFalse(s2 <= s1)

    def test_ordered_set_issuperset(self):
        s1 = OrderedSet([1, 2, 3, 4, 5, 6])
        s2 = OrderedSet([1, 2, 3])
        self.assertTrue(s1.issuperset(s2))
        self.assertFalse(s2.issuperset(s1))
        self.assertTrue(s1 >= s2)
        self.assertFalse(s2 >= s1)

    def test_ordered_set_isdisjoint(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([4, 5, 6])
        s3 = OrderedSet([1, 5, 6])
        self.assertTrue(s1.isdisjoint(s2))
        self.assertFalse(s3.isdisjoint(s2))

    def test_ordered_set_symmetric_difference(self):
        s1 = OrderedSet([1, 2, 3])
        s2 = OrderedSet([3, 4, 5])
        s3 = set(iter([1, 2, 3]))
        s4 = set(iter([3, 4, 5]))
        symmetric_diff = s1.symmetric_difference(s2)
        self.assertSetEqual(symmetric_diff, {1, 2, 4, 5})
        symmetric_diff = s1 ^ s2
        self.assertSetEqual(symmetric_diff, {1, 2, 4, 5})
        symmetric_diff = s1 ^ s4
        self.assertSetEqual(symmetric_diff, {1, 2, 4, 5})
        symmetric_diff = s3 ^ s2
        self.assertSetEqual(symmetric_diff, {1, 2, 4, 5})
        symmetric_diff = s3.symmetric_difference(s4)
        self.assertSetEqual(symmetric_diff, {1, 2, 4, 5})


if __name__ == '__main__':
    unittest.main()
