from collections import OrderedDict
from typing import Any


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
