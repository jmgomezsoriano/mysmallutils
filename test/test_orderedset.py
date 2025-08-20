import time
import unittest
from datetime import datetime

from mysutils.collections import OrderedSet


class MyTestCase(unittest.TestCase):
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
        time.sleep(0.1)
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
