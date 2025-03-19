
import logging
from typing import Any, Iterable


from safethread.AbstractLock import AbstractLock
from safethread.datatype.AbstractSafeSet import AbstractSafeSet

from safethread.process.datatype.ProcessSafeList import ProcessSafeList
from safethread.process.datatype.ProcessRLock import ProcessRLock


class ProcessSafeSet(AbstractSafeSet):

    def __eq__(self, other) -> bool:
        if isinstance(other, ProcessSafeSet):
            return set(self._data) == set(other._data)
        return self == ProcessSafeSet(other)

    def __lt__(self, other):
        if isinstance(other, ProcessSafeSet):
            return set(self._data) < set(other._data)
        return self < ProcessSafeSet(other)

    def __gt__(self, other):
        if isinstance(other, ProcessSafeSet):
            return set(self._data) > set(other._data)
        return self > ProcessSafeSet(other)

    def __init__(self, data: set | Iterable | None = None):
        super().__init__(data)
        self._data: ProcessSafeList

    def _create_data(self, data: Any | None) -> Any:
        if isinstance(data, ProcessSafeList):
            return data
        return ProcessSafeList(data or [])

    def _create_lock(self) -> AbstractLock:
        return ProcessRLock()

    def add(self, value):
        """
        Adds an element to the set safely.

        :param value: The element to add to the set.
        :type value: `type of value`
        """
        if value not in self._data:
            self._data.append(value)

    def clear(self):
        """
        Removes all elements from the set safely.
        """
        with self._lock:  # Ensure  safety
            self._data.clear()

    def difference(self, *others):
        """
        Returns a new set with elements in the set but not in the others safely.

        :param others: Sets to subtract from the current set.
        :type others: set or Iterable

        :return: A new set with the difference.
        :rtype: set
        """
        with self._lock:  # Ensure  safety
            return set(self._data).difference(*others)

    def difference_update(self, *others):
        """
        Removes all elements of another set from the current set safely.

        :param others: Sets to subtract from the current set.
        :type others: set or Iterable
        """
        with self._lock:  # Ensure  safety
            # get elements from others sets
            for other_set in others:
                for item in other_set:
                    try:
                        self._data.remove(item)
                    except:
                        pass

    def discard(self, value):
        """
        Removes an element from the set if present safely. Does nothing if not present.

        :param value: The element to remove from the set.
        :type value: `type of value`
        """
        try:
            with self._lock:  # Ensure  safety
                self._data.remove(value)
        except:
            pass

    def intersection(self, *others):
        """
        Returns a new set with elements common to the set and all others safely.

        :param others: Sets to intersect with the current set.
        :type others: set or Iterable

        :return: A new set with the intersection.
        :rtype: set
        """
        with self._lock:  # Ensure  safety
            return set(self._data).intersection(*others)

    def intersection_update(self, *others):
        """
        Updates the set with the intersection of itself and others safely.

        :param others: Sets to intersect with the current set.
        :type others: set or Iterable
        """
        with self._lock:  # Ensure  safety
            new_data = set(self._data)
            new_data.intersection_update(*others)
            self._data.clear()
            self._data.extend(new_data)

    def isdisjoint(self, other):
        """
        Returns True if the set has no elements in common with another set safely.

        :param other: The other set to compare.
        :type other: set

        :return: `True` if the sets are disjoint, otherwise `False`.
        :rtype: bool
        """
        with self._lock:  # Ensure  safety
            return set(self._data).isdisjoint(other)

    def issubset(self, other):
        """
        Returns True if the set is a subset of another set safely.

        :param other: The other set to compare.
        :type other: set

        :return: `True` if the set is a subset, otherwise `False`.
        :rtype: bool
        """
        with self._lock:  # Ensure  safety
            return set(self._data).issubset(other)

    def issuperset(self, other):
        """
        Returns True if the set is a superset of another set safely.

        :param other: The other set to compare.
        :type other: set

        :return: `True` if the set is a superset, otherwise `False`.
        :rtype: bool
        """
        with self._lock:  # Ensure  safety
            return set(self._data).issuperset(other)

    def pop(self):
        """
        Removes and returns an arbitrary element from the set safely.

        :return: An arbitrary element from the set.
        :rtype: `type of element`

        :raises KeyError: If the set is empty.
        """
        with self._lock:  # Ensure  safety
            try:
                return self._data.pop()
            except Exception as e:
                raise KeyError(f"Failed to pop element: {e}")

    def remove(self, value):
        """
        Removes an element from the set safely. Raises KeyError if not present.

        :param value: The element to remove from the set.
        :type value: `type of value`

        :raises KeyError: If the element is not found in the set.
        """
        with self._lock:  # Ensure  safety
            try:
                self._data.remove(value)
            except Exception as e:
                raise KeyError(f"Failed to remove element: {e}")

    def symmetric_difference(self, other):
        """
        Returns a new set with elements in either the set or other but not both safely.

        :param other: The set to compare.
        :type other: set

        :return: A new set with the symmetric difference.
        :rtype: set
        """
        with self._lock:  # Ensure  safety
            return set(self._data).symmetric_difference(other)

    def symmetric_difference_update(self, other):
        """
        Updates the set with the symmetric difference of itself and another set safely.

        :param other: The set to compare.
        :type other: set
        """
        with self._lock:  # Ensure  safety
            new_data = set(self._data)
            new_data.symmetric_difference_update(other)
            self._data.clear()
            self._data.extend(new_data)

    def union(self, *others):
        """
        Returns a new set with all elements from the set and all others safely.

        :param others: Sets to combine with the current set.
        :type others: set or Iterable

        :return: A new set with the union.
        :rtype: set
        """
        with self._lock:  # Ensure  safety
            return set(self._data).union(*others)

    def update(self, *others):
        """
        Updates the set with elements from all others safely.

        :param others: Sets to add to the current set.
        :type others: set or Iterable
        """
        with self._lock:  # Ensure  safety
            new_data = self.union(*others)
            self._data.clear()
            self._data.extend(new_data)
