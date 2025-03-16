
from multiprocessing.managers import DictProxy

from typing import Any, Iterable

from .. import AbstractLock

from . import AbstractSafeBase


class AbstractSafeDict(AbstractSafeBase):
    def __init__(self, data: dict | Iterable | DictProxy | None = None):
        """
        Initialize a dictionary with a Lock for safety.

        :param data: Initial data to populate the dictionary. Defaults to None.
        :type data: dict or Iterable or DictProxy, optional
        """
        super().__init__(data)
        self._lock: AbstractLock
        self._data: dict | DictProxy

    def clear(self):
        """
        Safely clear the dictionary.
        """
        with self._lock:
            self._data.clear()

    def get(self, key, default=None):
        """
        Safely retrieve a value from the dictionary.

        :param key: The key to look up.
        :type key: Any
        :param default: The default value if the key is not found. Defaults to None.
        :type default: Any, optional

        :return: The value associated with the key, or the default value.
        :rtype: Any
        """
        with self._lock:
            return self._data.get(key, default)

    def items(self):
        """
        Return a set-like view of dictionary items (key-value pairs).

        :return: A view object displaying the dictionary's items.
        :rtype: dict_items
        """
        with self._lock:
            return self._data.items()

    def keys(self):
        """
        Return a set-like view of dictionary keys.

        :return: A view object displaying the dictionary's keys.
        :rtype: dict_keys
        """
        with self._lock:
            return self._data.keys()

    def pop(self, key, default=None):
        """
        Remove the specified key and return the corresponding value.

        :param key: The key to remove.
        :type key: Any
        :param default: The default value to return if the key is not found. Defaults to None.
        :type default: Any, optional

        :raises KeyError: If the key is not found and no default value is provided.

        :return: The value associated with the key, or the default value.
        :rtype: Any
        """
        with self._lock:
            return self._data.pop(key, default)

    def popitem(self):
        """
        Remove and return the last key-value pair from the dictionary in a process-safe manner.

        :raises KeyError: If the dictionary is empty.

        :return: The last key-value pair removed from the dictionary.
        :rtype: tuple
        """
        with self._lock:
            return self._data.popitem()

    def setdefault(self, key, default=None):
        """
        Retrieve the value for a given key if it exists; otherwise, insert the key with the provided default value.

        :param key: The key to look up in the dictionary.
        :type key: Any
        :param default: The value to set if the key is not found. Defaults to None.
        :type default: Any, optional

        :return: The value associated with the key if it exists; otherwise, the default value that was set.
        :rtype: Any
        """
        with self._lock:
            return self._data.setdefault(key, default)

    def update(self, m: Iterable | None = None, **kwargs):
        """
        Update the dictionary with key-value pairs from another dictionary or iterable of key-value pairs.

        :param m: A dictionary or an iterable of key-value pairs (e.g., list of tuples) to update the dictionary with.
        :type m: dict or Iterable, optional
        :param kwargs: Additional key-value pairs to update the dictionary.
        :type kwargs: dict

        **Example:**

        ```python
        safe_dict.update({'a': 1, 'b': 2})
        safe_dict.update(a=3, c=4)
        ```
        """
        with self._lock:
            if m:
                self._data.update(m, **kwargs)
            else:
                self._data.update(**kwargs)

    def values(self):
        """
        Return a set-like view of dictionary values.

        :return: A view object displaying the dictionary's values.
        :rtype: dict_values
        """
        with self._lock:
            return self._data.values()
