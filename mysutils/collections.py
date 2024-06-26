from collections import OrderedDict
from collections.abc import Set
from typing import Union, List, Any, Callable, Dict, Iterable, Tuple, Optional, Hashable
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
    for lst in lists:
        for e in lst:
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


class OrderedSet(Set, Iterable):
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

    def __setitem__(self, item: Hashable, date: datetime) -> None:
        """ Set the time of an element in the set.

        :param item: The item to modify its introduction date.
        :param date: The date to modify.
        """
        self.set_time(item, date)

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

    def pop(self, last: bool = False) -> Any:
        """ Pop an element from the set. By default, it pops the first element introduced,
          but also it is possible to pop the last.

        :param last: If True, the last element introduced will be removed, otherwise the first one.
        :return: The last element from the set.
        """
        return self.items.popitem(last)[0]

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

    def clear(self) -> None:
        """ Remove all elements from the set. """
        self.items.clear()

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
        return OrderedSet(self.items.keys() - set(other))

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

    def union(self, other: set) -> 'OrderedSet':
        """ Return the union of two sets as a new `OrderedSet`.

        :param other: The other set to union with.
        :return: The union of the two sets as a new `OrderedSet`.
        """
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


def convert_tuple_values(t: tuple, *types: Union[Callable, type]) -> tuple:
    """ Convert the values of a tuple using conversion functions.
    For example:

        ```python
        row = ('5', '9.99', 'USB device')
        # Convert the first element in integer, the second in float and the third in string
        quantity, price, item = convert_tuple_values(row, int, float, str)
        ```

    :param t: The tuple.
    :param t: The types or conversion functions.
    """
    if len(t) != len(types):
        raise ValueError(f'The tuple size must be as long as the list of types: {len(t)} vs {len(types)}')
    return tuple(types[i](val) for i, val in enumerate(t))


class LRUDict(OrderedDict):
    def __init__(self, max_size: int = 0) -> None:
        """
        A dictionary with a maximum capacity.
        When it is reached, the first element added or acceded is removed to be able to add the new ones.
        If max_size is 0, then, no limit.

        :param max_size: The maximum number of items the dictionary can hold.
        """
        if max_size < 0:
            raise ValueError(f'The maximum size of the dict should be 0 and over. Defined value: {max_size}')
        self.max_size = max_size
        super().__init__()

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Add an item to the dictionary.
        If the key already exists, move the item to the end to be removed.
        If the dictionary exceeds the maximum size, remove the least recently used item.

        :param key: The key of the item.
        :param value: The value of the item.
        """
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if self.max_size != 0 and len(self) > self.max_size:
            oldest = next(iter(self))
            del self[oldest]

    def __getitem__(self, key: Any) -> None:
        """
        Get the value associated with the key in the dictionary and move the item to the end
        to mark it as the most recently used.

        :param key: The key of the item to retrieve.
        :return: The value associated with the key.
        """
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def update(self, *args, **kwargs) -> None:
        """
        Update the dictionary with the key/value pairs from other, overwriting existing keys.
        Move each updated item to the end to mark it as the most recently used.

        :param args: Other dictionaries or iterable of key-value pairs.
        :param kwargs: Key-value pairs.
        """
        if args:
            if len(args) > 1:
                raise TypeError(f"update expected at most 1 argument, got {len(args)}")
            other = args[0]
            if isinstance(other, dict):
                for key, value in other.items():
                    self[key] = value
            elif hasattr(other, "__iter__"):
                for key, value in other:
                    self[key] = value
            else:
                raise TypeError("update() argument must be a dict or an iterable of key/value pairs")

        for key, value in kwargs.items():
            self[key] = value
