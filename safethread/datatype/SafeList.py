
from typing import Iterable
from .SafeBaseObj import SafeBaseObj


class SafeList(SafeBaseObj):
    def __init__(self, data: list | Iterable | None = None):
        """Initializes a shared list with a lock for thread safety."""
        data = data if isinstance(data, list) else list(data or [])
        super().__init__(data)
        self._data: list

    def append(self, value):
        """Adds an item to the list safely."""
        with self._lock:
            self._data.append(value)

    def clear(self):
        """Clears the list safely."""
        with self._lock:
            self._data.clear()

    def count(self, value):
        """Counts the occurrences of an item in the list."""
        with self._lock:
            return self._data.count(value)

    def extend(self, values):
        """Adds multiple items to the list safely."""
        with self._lock:
            self._data.extend(values)

    def index(self, value, start=0, end=None):
        """Returns the index of the first matching item safely."""
        with self._lock:
            return self._data.index(value, start, end if end is not None else len(self._data))

    def insert(self, index, value):
        """Inserts an item at the specified position safely."""
        with self._lock:
            self._data.insert(index, value)

    def pop(self, index=-1):
        """Removes and returns an item from the list safely."""
        with self._lock:
            return self._data.pop(index)

    def remove(self, value):
        """Removes an item from the list safely."""
        with self._lock:
            self._data.remove(value)

    def reverse(self):
        """Reverses the order of the list safely."""
        with self._lock:
            self._data.reverse()

    def sort(self, **kwargs):
        """Sorts the list safely."""
        with self._lock:
            self._data.sort(**kwargs)
