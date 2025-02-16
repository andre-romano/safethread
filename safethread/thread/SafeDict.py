
from typing import Any, Iterable
from .SafeBaseObj import SafeBaseObj


class SafeDict(SafeBaseObj):
    def __init__(self, dictObj: dict | None = None):
        """Initialize a shared dictionary with a Lock for thread safety."""
        super().__init__(dictObj or {})
        self._data: dict

    def clear(self):
        """Safely clear the dictionary."""
        with self._lock:
            self._data.clear()

    def fromkeys(self, iterable: Iterable, value: Any | None = None):
        """Create a new dictionary with keys from iterable and values set to value."""
        with self._lock:
            return self._data.fromkeys(iterable, value)

    def get(self, key, default=None):
        """Safely retrieve a value from the dictionary."""
        with self._lock:
            return self._data.get(key, default)

    def items(self):
        """Return a set-like of dictionary items (key-value pairs)."""
        with self._lock:
            return self._data.items()

    def keys(self):
        """Return a set-like of dictionary keys."""
        with self._lock:
            return self._data.keys()

    def pop(self, key, default=None):
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.

        If the key is not found, return the default if given; otherwise,
        raise a KeyError.
        """
        with self._lock:
            return self._data.pop(key, default)

    def popitem(self):
        """
        Removes and returns the last key-value pair from the dictionary in a thread-safe manner.
        Returns:
            tuple: The last key-value pair removed from the dictionary.

        Raises:
            KeyError: If the dictionary is empty.
        """
        with self._lock:
            return self._data.popitem()

    def setdefault(self, key, default=None):
        """
        Retrieves the value for a given key if it exists; otherwise, inserts the key with the provided default value 
        in a thread-safe manner.

        Args:
            key: The key to look up in the dictionary.
            default (optional): The value to set if the key is not found. Defaults to None.

        Returns:
            The value associated with the key if it exists; otherwise, the default value that was set.
        """
        with self._lock:
            return self._data.setdefault(key, default)

    def update(self, m: Iterable | None = None, **kwargs):
        """
        Updates the dictionary with key-value pairs from another dictionary or iterable of key-value pairs, 
        in a thread-safe manner.

        Args:
            m: A dictionary or an iterable of key-value pairs (e.g., list of tuples) to update the dictionary with.
            **kwargs: Additional key-value pairs to update the dictionary.

        Example:
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
        """Return a set-like of dictionary values."""
        with self._lock:
            return self._data.values()
