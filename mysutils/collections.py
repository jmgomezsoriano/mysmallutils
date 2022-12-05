import collections
from collections import OrderedDict
from typing import Union, List, Any, Callable, Dict, Iterable, Tuple, Optional, Set, Hashable, Sequence
from datetime import datetime


def head(obj: Union[dict, set], top: int = 10) -> Union[dict, set]:
    """ Obtain the first top elements of a dictionary o a set.

    :param obj: A dictionary or a set.
    :param top: The number of elements to return, by default 10.
    :return: The first top elements of the given dictionary or set.
    """
    if isinstance(obj, dict):
        return dh(obj, top)
    if isinstance(obj, set):
        return sh(obj, top)
    raise ValueError('The object must be a dictionary or a set.')


def dh(d: dict, top: int = 10) -> dict:
    """ Obtain the first top elements of a dictionary.

    :param d: The dictionary.
    :param top: The number of dictionary items to return
    :return: A dictionary with the top first items of the given dictionary.
    """
    return {key: value for i, (key, value) in enumerate(d.items()) if i < top}


def sh(d: set, top: int = 10) -> set:
    """ Obtain the first top elements of a set.

    :param d: The set.
    :param top: The number of set items to return
    :return: A set with the top first items of the given set.
    """
    return {value for i, value in enumerate(sorted(d)) if i < top}


def list_union(*lists: list) -> list:
    """ Create a new list with the union of the lists without repeated elements.

    :param lists: The list to union.
    :return: The union of all lists respecting the element order.
    """
    result = []
    for l in lists:
        for e in l:
            if e not in result:
                result.append(e)
    return result


def concat_lists(*lists: list) -> list:
    """ Concatenate a list of lists at once.

    :param lists: The list of lists.
    :return: One new list with the element of all the lists.
    """
    result = []
    for l in lists:
        result.extend(l)
    return result


def del_keys(d: dict, *keys: Any, ignore_errors: bool = True) -> dict:
    """ Remove the dictionary items from their keys and return the modified dictionary.

    :param d: The dictionary.
    :param keys: A key or a list of keys.
    :param ignore_errors: If True, ignore if the key does not exist.
    :return: The modified dictionary.
    """
    for key in keys:
        if not (key not in d and ignore_errors):
            del d[key]

    return d


def add_keys(d: dict, modify: bool = True, **kwargs) -> dict:
    """ Add or change several items into a dictionary and return the modified dictionary.

    :param d: The dictionary.
    :param modify: If True, if a key already exists, then update it, otherwise raise an error.
    :param kwargs: The dictionary key/value pairs.
    :return: The modified dictionary.
    """
    for key, value in kwargs.items():
        if not modify and key in d:
            raise KeyError("Duplicate key")
        d[key] = value

    return d


def mod_key(d: dict, old_key: Any, new_key: Any) -> dict:
    """ Modify the name of a dictionary key without change anything else.

    :param d: The dictionary to modify.
    :param old_key: The old key to replace for.
    :param new_key: The new key to replace with.
    :return: The modified dictionary.
    """
    value = d[old_key]
    del_keys(d, old_key)[new_key] = value
    return d


def mod_keys(d: dict, **kwargs) -> dict:
    """ Modify the names of a dictionary keys without change anything else with just an instruction.

    :param d: The dictionary to modify.
    :param kwargs: The old keys assigned to the name of the new ones.
    :return: The modified dictionary.
    """
    for old_key, new_key in kwargs.items():
        value = d[old_key]
        del_keys(d, old_key)[new_key] = value
    return d


def mod_value(d: dict, key: Any, value: Any) -> dict:
    """ Modify the value of a dictionary item without change anything else and return the modified dictionary.

    :param d: The dictionary to modify.
    :param key: The item key to modify.
    :param value: The value to replace with.
    :return: The modified dictionary.
    """
    d[key] = value
    return d


def mod_values(d: dict, **kwargs) -> dict:
    """ Modify several value of a dictionary items with just an instruction.

    :param d: The dictionary to modify.
    :param kwargs: The keys and their values to modify.
    :return: The modified dictionary.
    """
    for key, value in kwargs.items():
        d[key] = value
    return d


def filter_lst(lst: list, n: int = 0, init: int = 0, filter_func: Callable = None) -> list:
    """ Filter a list.

    :param lst: The list to filter.
    :param n: The maximum number of results. If it is not given, then return all the results.
    :param init: The initial result. Before this position the items are filtered.
    :param filter_func: A filter function to filter.
    :return: The filtered list.
    """
    n = n if n else len(lst)
    lst = lst[init:init + n]
    return [e for e in filter(filter_func, lst)] if filter_func else lst


def first_key_value(dicts: Iterable[Dict[Any, Any]], key: Any = None) -> Any:
    """ From a iterable of dictionaries, return the key value of the first dictionary that contains that key.

    :param dicts: The iterable of dictionaries.
    :param key: The key to search.
    :return: The value of the first dictionary that contains that key.
    :raises KeyError: If any of the dictionaries contains that key.
    """
    for d in dicts:
        if key in d:
            return d[key]
    raise KeyError(f'The key "{key}" does not exist in any of the dictionaries.')


def first_item(d: dict) -> Optional[Tuple[Any, Any]]:
    """ From a dictionary, return the first item.

    :param d: The dictionary.
    :return: The first item of the dictionary if the dictionary has an item, otherwise None.
    """
    for item in d.items():
        return item
    return None


def last_item(d: dict) -> Optional[Tuple[Any, Any]]:
    """ From a dictionary, return the first item.

    :param d: The dictionary.
    :return: The last item of the dictionary if the dictionary has an item, otherwise None.
    """
    item = None
    for item in d.items():
        pass
    return item


def first_key(d: dict) -> Any:
    """ From a dictionary, return the first key.

    :param d: The dictionary.
    :return: The first key of the dictionary if the dictionary as a item, otherwise None.
    """
    item = first_item(d)
    return None if item is None else item[0]


def last_key(d: dict) -> Any:
    """ From a dictionary, return the last key.

    :param d: The dictionary.
    :return: The last key of the dictionary if the dictionary as an item, otherwise None.
    """
    item = last_item(d)
    return None if item is None else item[0]


def first_value(d: dict) -> Any:
    """ From a dictionary, return the first value.

    :param d: The dictionary.
    :return: The first value of the dictionary if the dictionary as an item, otherwise None.
    """
    item = first_item(d)
    return None if item is None else item[1]


def last_value(d: dict) -> Any:
    """ From a dictionary, return the last value.

    :param d: The dictionary.
    :return: The last value of the dictionary if the dictionary as an item, otherwise None.
    """
    item = last_item(d)
    return None if item is None else item[1]


def item(d: dict, i: int) -> Optional[Tuple[Any, Any]]:
    """ Return the item of the position i in the dictionary.

    :param d: The dictionary.
    :param i: The index position.
    :return: The dictionary item which the position is i.
    :raises KeyError: If i is out of index.
    """
    if i < 0 or i >= len(d):
        raise KeyError(f'The given dictionary only have index from 0 to {len(d) - 1}, your index is out of index: {i}')
    for idx, item in enumerate(d.items()):
        if i == idx:
            return item


def key(d: dict, i: int) -> Optional[Tuple[Any, Any]]:
    """ Return the key of the position i in the dictionary.

    :param d: The dictionary.
    :param i: The index position.
    :return: The dictionary key which the position is i.
    :raises KeyError: If i is out of index.
    """
    return item(d, i)[0]


def value(d: dict, i: int) -> Optional[Tuple[Any, Any]]:
    """ Return the value of the position i in the dictionary.

    :param d: The dictionary.
    :param i: The index position.
    :return: The dictionary value which the position is i.
    :raises KeyError: If i is out of index.
    """
    return item(d, i)[1]


def merge_dicts(dicts: Iterable[Dict[Any, Any]]) -> Dict[Any, List[Any]]:
    """ Convert a list of dictionaries with the same keys in a dictionary which each key contain the list of values.

    :param dicts: The list of dictionaries to merge.
    :return: The dictionary with merged values.
    """
    values = {}
    for d in dicts:
        for key, value in d.items():
            values[key] = values[key] if key in values else []
            values[key].append(value)
    return values


def merge_tuples(tuples: Iterable[tuple]) -> tuple:
    """ Convert a list of dictionaries with the same keys in a dictionary which each key contain the list of values.
       All the tuples has to have the same length.

    :param tuples: The list of tuples to merge.
    :return: The tuple with merged values, in which each element contain a list with the values.
    """
    result = tuple([] for _ in list(tuples)[0]) if tuples else ()
    for t in tuples:
        for i, e in enumerate(t):
            result[i].append(e)
    return result


class OrderedSet(collections.Set, Iterable):
    """ An ordered set with pop() method, which can be extracted using FIFO or LIFO. """

    def __init__(self, items: Iterable = iter([])) -> None:
        """ Initialize the OrderedSet with an empty dictionary or a list of elements.

        :param items: The elements to add.
        """
        self.items = OrderedDict()
        self.update(items)

    def update(self, items: Iterable) -> None:
        """ Update the OrderedSet with a list of elements.

        :param items: The elements to add.
        """
        for item in items:
            self.add(item)

    def add(self, item: Hashable) -> None:
        """ Add an element to the set.

        :param item: The element to add.
        """
        if item not in self.items:
            self.items[item] = datetime.now()

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

    def __setitem__(self, key: Hashable, value: datetime) -> None:
        """ Set the time of an element in the set.

        :param item: The item to modify its introduction date.
        :param date: The date to modify.
        """
        self.set_time(key, value)

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
        """ Get a copy of the OrderedSet with items were introduced util the given date, including the same date.

        :param date: The date to search the set.
        :return: A copy of the OrderedSet with items added until the given date.
        """
        items = OrderedSet()
        for item in [i for i in self.items if self[i] <= date]:
            items[item] = self.items[item]
        return items

    def after(self, date: datetime) -> 'OrderedSet':
        """ Get a copy of the OrderedSet with items were introduced before the given date.

        :param date: The date to search the set.
        :return: A copy of the OrderedSet with items added before the given date.
        """
        items = OrderedSet()
        for item in [i for i in self.items if self[i] > date]:
            items[item] = self.items[item]
        return items

    def since(self, date: datetime) -> 'OrderedSet':
        """ Get a copy of the OrderedSet with items were introduced since the given date, including the same date).

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

    def pop(self, last: bool = False) -> Any:
        """ Pop an element from the set. By default, it pops the first element introduced,
          but also it is possible to pop the last.

        :param last: If True, the last element introduced will be removed, otherwise the first one.
        :return: The last element from the set.
        """
        return self.items.popitem(last)[0]

    def discard(self, item: Hashable) -> None:
        """ Remove an element from the set.

        :param item: The element to remove.
        """
        del self.items[item]

    def clear(self) -> None:
        """ Remove all elements from the set. """
        self.items.clear()

    def copy(self) -> 'OrderedSet':
        """ Return a copy of the OrderedSet."""
        return OrderedSet([k for k in self.items.keys()])

    def difference(self, other: collections.Set) -> 'OrderedSet':
        """ Get the elements in the set which are not present in the other set.

        :param other: The other set.
        :return: The elements which are not present in the other set.
        """
        return OrderedSet(self.items.keys() - set(other))

    def __sub__(self, other: collections.Set) -> 'OrderedSet':
        """ Get the elements in the set which are not present in the other set.

        :param other: The other set.
        :return: The elements which are not present in the other set.
        """
        return self.difference(other)

    def difference_update(self, other: collections.Set) -> None:
        """ Remove the elements in the set which are not present in the other set.

        :param other: The other set.
        """
        items = self.items.keys() - set(other)
        self.items = OrderedDict()
        self.update(items)

    def intersection(self, other: collections.Set) -> 'OrderedSet':
        """ Get the elements in the set which are present in the other set.

        :param other: The other set.
        :return: The elements which are present in the other set.
        """
        return OrderedSet(self.items.keys() & set(other))

    def __and__(self, other: collections.Set) -> 'OrderedSet':
        """ Get the elements in the set which are present in the other set.

        :param other: The other set.
        :return: The elements which are present in the other set.
        """
        return self.intersection(other)

    def intersection_update(self, other: collections.Set) -> None:
        """ Remove the elements in the set which are not present in the other set.

        :param other: The other set.
        """
        items = self.items.keys() & set(other)
        self.items = OrderedDict()
        self.update(items)

    def union(self, other: collections.Set) -> 'OrderedSet':
        """ Return the union of two sets as a new `OrderedSet`.

        :param other: The other set to union with.
        :return: The union of the two sets as a new `OrderedSet`.
        """
        return OrderedSet(self.items.keys() | set(other))

    def __or__(self, other: collections.Set) -> 'OrderedSet':
        """ Return the union of two sets as a new `OrderedSet`.

        :param other: The other set to union with.
        :return: The union of the two sets as a new `OrderedSet`.
        """
        return self.union(other)

    def isdisjoint(self, other: collections.Set) -> bool:
        """ Check if the set is disjoint from the other set.

        :param other: The other set.
        :return: True if the set is disjoint from the other set, False otherwise.
        """
        return not bool(self.items.keys() & set(other))

    def issubset(self, other: collections.Set) -> bool:
        """ Check if the set is a subset of the other set.

        :param other: The other set.
        :return: True if the set is a subset of the other set, False otherwise.
        """
        return self.items.keys() <= set(other)

    def __le__(self, other: collections.Set) -> bool:
        """ Check if the set is a subset of the other set.

        :param other: The other set.
        :return: True if the set is a subset of the other set, False otherwise.
        """
        return self.issubset(other)

    def issuperset(self, other: collections.Set) -> bool:
        """ Check if the set is a superset of the other set.

        :param other: The other set.
        :return: True if the set is a superset of the other set, False otherwise.
        """
        return self.items.keys() >= set(other)

    def __ge__(self, other: collections.Set) -> bool:
        """ Check if the set is a superset of the other set.

        :param other: The other set.
        :return: True if the set is a superset of the other set, False otherwise.
        """
        return self.issuperset(other)

    def symmetric_difference(self, other: collections.Set) -> 'OrderedSet':
        """ Return the symmetric difference of two sets as a new `OrderedSet`.

        :param other: The other set to take the symmetric difference with.
        :return: The symmetric difference of the two sets as a new `OrderedSet`.
        """
        return OrderedSet(self.items.keys() ^ set(other))

    def __pow__(self, other: collections.Set) -> 'OrderedSet':
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

    def __eq__(self, other: collections.Set) -> bool:
        """ Check if the set is equal to the other set.

        :param other: The other set.
        :return: True if the set is equal to the other set, False otherwise.
        """
        return set(self.items.keys()) == set(other)

    def __neq__(self, other: collections.Set) -> bool:
        """ Check if the set is not equal to the other set.

        :param other: The other set.
        :return: True if the set is not equal to the other set, False otherwise.
        """
        return set(self.items.keys()) != set(other)

    def __repr__(self):
        """ Get the string representation of the set. """
        return repr(set(self.items.keys()))
