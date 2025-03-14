
from typing import Iterable

from . import SafeThreadBase


class SafeThreadList(SafeThreadBase):
    def __init__(self, data: list | Iterable | None = None):
        """
        Initializes a shared list with a lock for thread safety.

        :param data: The initial data to populate the list with.
        :type data: list, Iterable, or None
        """
        data = data if isinstance(data, list) else list(data or [])
        super().__init__(data)
        self._data: list

    def append(self, value):
        """
        Adds an item to the list safely.

        :param value: The item to be added to the list.
        :type value: `type of value`
        """
        with self._lock:
            self._data.append(value)

    def clear(self):
        """
        Clears the list safely.
        """
        with self._lock:
            self._data.clear()

    def count(self, value):
        """
        Counts the occurrences of an item in the list.

        :param value: The item whose occurrences to count.
        :type value: `type of value`
        :return: The number of occurrences of the item in the list.
        :rtype: int
        """
        with self._lock:
            return self._data.count(value)

    def extend(self, values):
        """
        Adds multiple items to the list safely.

        :param values: The items to be added to the list.
        :type values: list or Iterable
        """
        with self._lock:
            self._data.extend(values)

    def index(self, value, start=0, end=None):
        """
        Returns the index of the first matching item safely.

        :param value: The item to find in the list.
        :type value: `type of value`
        :param start: The starting index for the search. Defaults to 0.
        :type start: int, optional
        :param end: The ending index for the search. Defaults to None.
        :type end: int, optional
        :return: The index of the first matching item.
        :rtype: int
        :raises ValueError: If the item is not found in the list.
        """
        with self._lock:
            return self._data.index(value, start, end if end is not None else len(self._data))

    def insert(self, index, value):
        """
        Inserts an item at the specified position safely.

        :param index: The index at which to insert the item.
        :type index: int
        :param value: The item to insert.
        :type value: `type of value`
        """
        with self._lock:
            self._data.insert(index, value)

    def pop(self, index=-1):
        """
        Removes and returns an item from the list safely.

        :param index: The index of the item to remove. Defaults to -1 (last item).
        :type index: int, optional
        :return: The removed item.
        :rtype: `type of item`
        :raises IndexError: If the list is empty or the index is out of range.
        """
        with self._lock:
            return self._data.pop(index)

    def remove(self, value):
        """
        Removes an item from the list safely.

        :param value: The item to remove from the list.
        :type value: `type of value`
        :raises ValueError: If the item is not found in the list.
        """
        with self._lock:
            self._data.remove(value)

    def reverse(self):
        """
        Reverses the order of the list safely.
        """
        with self._lock:
            self._data.reverse()

    def sort(self, **kwargs):
        """
        Sorts the list safely.

        :param kwargs: Additional arguments to pass to the sort function.
        :return: None
        :rtype: None
        """
        with self._lock:
            self._data.sort(**kwargs)
