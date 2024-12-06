from collections import OrderedDict
from typing import Set, Iterable, Hashable, Any
from datetime import datetime


class OrderedSet(Set, Iterable):
    """ An ordered set with pop() method, which can be extracted using FIFO or LIFO. """

    def __init__(self, items: Iterable = iter([])) -> None:
        """ Initialize the OrderedSet with an empty dictionary or a list of elements.

        :param items: The elements to add.
        """
        super().__init__(items)
        self.items = OrderedDict()
        self.update(items)

    def update(self, items: Iterable) -> None:
        """ Update the OrderedSet with a list of elements.

        :param items: The elements to add.
        """
        for item in items:
            self.add(item)
        super().update(items)

    def add(self, item: Hashable) -> None:
        """ Add an element to the set.

        :param item: The element to add.
        """
        if item not in self.items:
            self.items[item] = datetime.now()
            super().add(item)

    def time(self, item: Hashable) -> datetime:
        """ Get the time when an element was added.

        :param item: The item to search the time.
        :return: A datetime object with the time where the object was introduced in the set.
        """
        return self.items[item]

    def __getitem__(self, item: Hashable) -> datetime:
        """ Get the time when an element was added.

        :param item: The item to search the time.
        :return: A datetime object with the time when the object was introduced in the set.
        """
        return self.time(item)

    def set_time(self, item: Hashable, date: datetime) -> None:
        """ Set the time of an element in the set.

        :param item: The item to modify its introduction date.
        :param date: The date to modify.
        """
        self.items[item] = date
        super().add(item)

    def __setitem__(self, item: Hashable, date: datetime) -> None:
        """ Set the time of an element in the set.

        :param item: The item to modify its introduction date.
        :param date: The date to modify.
        """
        self.set_time(item, date)
        super().add(item)

    def before(self, date: datetime) -> 'OrderedSet':
        """ Get a copy of the OrderedSet with items were introduced before the given date.

        :param date: The date to search the set.
        :return: A copy of the OrderedSet with items added before the given date.
        """
        items = OrderedSet()
        for item in [i for i in self.items if self[i] < date]:
            items[item] = self.items[item]
        return items

    def until(self, date: datetime) -> 'OrderedSet':
        """ Get a copy of the OrderedSet with items were introduced until the given date, including the same date.

        :param date: The date to search the set.
        :return: A copy of the OrderedSet with items added until the given date.
        """
        items = OrderedSet()
        for item in [i for i in self.items if self[i] <= date]:
            items[item] = self.items[item]
        return items

    def after(self, date: datetime) -> 'OrderedSet':
        """ Get a copy of the OrderedSet with items were introduced after the given date.

        :param date: The date to search the set.
        :return: A copy of the OrderedSet with items added before the given date.
        """
        items = OrderedSet()
        for item in [i for i in self.items if self[i] > date]:
            items[item] = self.items[item]
        return items

    def since(self, date: datetime) -> 'OrderedSet':
        """ Get a copy of the OrderedSet with items were introduced since the given date, including the same date.

        :param date: The date to search the set.
        :return: A copy of the OrderedSet with items added since the given date.
        """
        items = OrderedSet()
        for item in [i for i in self.items if self[i] >= date]:
            items[item] = self.items[item]
        return items

    def remove(self, item: Hashable) -> None:
        """ Remove an element from the set.

        :param item: The element to remove.
        """
        if item in self.items:
            del self.items[item]
            super().remove(item)

    def pop(self, last: bool = False) -> Any:
        """ Pop an element from the set. By default, it pops the first element introduced,
          but also it is possible to pop the last.

        :param last: If True, the last element introduced will be removed, otherwise the first one.
        :return: The last element from the set.
        """
        item = self.items.popitem(last)[0]
        super().remove(item)
        return item

    def remove_items(self, items: Iterable[Hashable], discard: bool = False) -> None:
        """ Remove the given items from the set.

        :param items: The items to remove.
        :param discard: If True, do not raise a KeyError if the item is not found.
        """
        for item in items:
            if discard:
                self.discard(item)
            else:
                self.remove(item)

    def remove_before(self, date: datetime, discard: bool = False) -> None:
        """ Remove all the introduced items before the given date.

        :param date: The date to search the set.
        :param discard: If True, do not raise a KeyError if the item is not found.
        """
        self.remove_items([i for i in self.items if self[i] < date], discard)

    def remove_until(self, date: datetime, discard: bool = False) -> None:
        """ Remove all the introduced items  until the given date, including the same date.

        :param date: The date to search the set.
        :param discard: If True, do not raise a KeyError if the item is not found.
        """
        self.remove_items([i for i in self.items if self[i] <= date], discard)

    def remove_after(self, date: datetime, discard: bool = False) -> None:
        """ Remove all the introduced items after the given date.

        :param date: The date to search the set.
        :param discard: If True, do not raise a KeyError if the item is not found.
        """
        self.remove_items([i for i in self.items if self[i] > date], discard)

    def remove_since(self, date: datetime, discard: bool = False) -> None:
        """ Remove all the introduced items since the given date, including the same date.

        :param date: The date to search the set.
        :param discard: If True, do not raise a KeyError if the item is not found.
        """
        self.remove_items([i for i in self.items if self[i] >= date])

    def first(self) -> 'Hashable':
        """ Get the first element of the OrderedDict without removing it.

        :return: The first element of the set.
        """
        if self.items:
            return next(iter(self.items))
        else:
            raise KeyError('set is empty.')

    def discard(self, item: Hashable) -> None:
        """ Remove an element from the set.

        :param item: The element to remove.
        """
        del self.items[item]
        super().discard(item)

    def clear(self) -> None:
        """ Remove all elements from the set. """
        self.items.clear()
        super().clear()

    def copy(self) -> 'OrderedSet':
        """ Return a copy of the OrderedSet."""
        items = OrderedSet([k for k in self.items.keys()])
        for item in items:
            items[item] = self.items[item]
        return items

    def difference(self, other: set) -> 'OrderedSet':
        """ Get the elements in the set which are not present in the other set.

        :param other: The other set.
        :return: The elements which are not present in the other set.
        """
        return OrderedSet(set(self.items.keys()) - set(other))

    def __set__(self):
        return set(self.items.keys())

    def __sub__(self, other: set) -> 'OrderedSet':
        """ Get the elements in the set which are not present in the other set.

        :param other: The other set.
        :return: The elements which are not present in the other set.
        """
        return self.difference(other)

    def difference_update(self, other: set) -> None:
        """ Remove the elements in the set which are not present in the other set.

        :param other: The other set.
        """
        items = self.items.keys() - set(other)
        self.items = OrderedDict()
        self.update(items)
        super().difference_update(other)

    def intersection(self, other: set) -> 'OrderedSet':
        """ Get the elements in the set which are present in the other set.

        :param other: The other set.
        :return: The elements which are present in the other set.
        """
        return OrderedSet(self.items.keys() & set(other))

    def __and__(self, other: set) -> 'OrderedSet':
        """ Get the elements in the set which are present in the other set.

        :param other: The other set.
        :return: The elements which are present in the other set.
        """
        return self.intersection(other)

    def intersection_update(self, other: set) -> None:
        """ Remove the elements in the set which are not present in the other set.

        :param other: The other set.
        """
        items = self.items.keys() & set(other)
        self.items = OrderedDict()
        self.update(items)
        super().update(items)

    def union(self, other: set) -> 'OrderedSet':
        """ Return the union of two sets as a new `OrderedSet`.

        :param other: The other set to union with.
        :return: The union of the two sets as a new `OrderedSet`.
        """
        super().union(other)
        return OrderedSet(self.items.keys() | set(other))

    def __or__(self, other: set) -> 'OrderedSet':
        """ Return the union of two sets as a new `OrderedSet`.

        :param other: The other set to union with.
        :return: The union of the two sets as a new `OrderedSet`.
        """
        return self.union(other)

    def isdisjoint(self, other: set) -> bool:
        """ Check if the set is disjoint from the other set.

        :param other: The other set.
        :return: True if the set is disjoint from the other set, False otherwise.
        """
        return not bool(self.items.keys() & set(other))

    def issubset(self, other: set) -> bool:
        """ Check if the set is a subset of the other set.

        :param other: The other set.
        :return: True if the set is a subset of the other set, False otherwise.
        """
        return self.items.keys() <= set(other)

    def __le__(self, other: set) -> bool:
        """ Check if the set is a subset of the other set.

        :param other: The other set.
        :return: True if the set is a subset of the other set, False otherwise.
        """
        return self.issubset(other)

    def issuperset(self, other: set) -> bool:
        """ Check if the set is a superset of the other set.

        :param other: The other set.
        :return: True if the set is a superset of the other set, False otherwise.
        """
        return self.items.keys() >= set(other)

    def __ge__(self, other: set) -> bool:
        """ Check if the set is a superset of the other set.

        :param other: The other set.
        :return: True if the set is a superset of the other set, False otherwise.
        """
        return self.issuperset(other)

    def symmetric_difference(self, other: set) -> 'OrderedSet':
        """ Return the symmetric difference of two sets as a new `OrderedSet`.

        :param other: The other set to take the symmetric difference with.
        :return: The symmetric difference of the two sets as a new `OrderedSet`.
        """
        return OrderedSet(self.items.keys() ^ set(other))

    def __pow__(self, other: set) -> 'OrderedSet':
        """ Return the symmetric difference of two sets as a new `OrderedSet`.

        :param other: The other set to take the symmetric difference with.
        :return: The symmetric difference of the two sets as a new `OrderedSet`.
        """
        return self.symmetric_difference(other)

    def __len__(self):
        """ Get the number of elements in the set. """
        return len(self.items)

    def __contains__(self, item):
        """ Check if the set contains an element. """
        return item in self.items

    def __iter__(self):
        """ Iterate over the elements in the set. """
        return iter(self.items.keys())

    def __list__(self):
        """ Get the elements in the set. """
        return list(self.items.keys())

    def __eq__(self, other: set) -> bool:
        """ Check if the set is equal to the other set.

        :param other: The other set.
        :return: True if the set is equal to the other set, False otherwise.
        """
        return set(self.items.keys()) == set(other)

    def __neq__(self, other: set) -> bool:
        """ Check if the set is not equal to the other set.

        :param other: The other set.
        :return: True if the set is not equal to the other set, False otherwise.
        """
        return set(self.items.keys()) != set(other)

    def __repr__(self):
        """ Get the string representation of the set. """
        return repr(set(self.items.keys()))

    def __rsub__(self, s: set): # real signature unknown
        """ Return value-self. """
        return s - set(self.items.keys())
