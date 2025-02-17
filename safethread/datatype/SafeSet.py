
from typing import Iterable
from .SafeBaseObj import SafeBaseObj


class SafeSet(SafeBaseObj):
    def __init__(self, data: set | Iterable | None = None):
        """Initialize a shared set with a Lock for thread safety."""
        data = data if isinstance(data, set) else set(data or [])
        super().__init__(data)
        self._data: set

    def add(self, value):
        """Adds an element to the set, thread-safe."""
        with self._lock:  # Ensure thread safety
            self._data.add(value)

    def clear(self):
        """Removes all elements from the set, thread-safe."""
        with self._lock:  # Ensure thread safety
            self._data.clear()

    def difference(self, *others):
        """Returns a new set with elements in the set but not in the others, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.difference(*others)

    def difference_update(self, *others):
        """Removes all elements of another set from the current set, thread-safe."""
        with self._lock:  # Ensure thread safety
            self._data.difference_update(*others)

    def discard(self, value):
        """Removes an element from the set if present, thread-safe. Does nothing if not present."""
        with self._lock:  # Ensure thread safety
            self._data.discard(value)

    def intersection(self, *others):
        """Returns a new set with elements common to the set and all others, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.intersection(*others)

    def intersection_update(self, *others):
        """Updates the set with the intersection of itself and others, thread-safe."""
        with self._lock:  # Ensure thread safety
            self._data.intersection_update(*others)

    def isdisjoint(self, other):
        """Returns True if the set has no elements in common with another set, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.isdisjoint(other)

    def issubset(self, other):
        """Returns True if the set is a subset of another set, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.issubset(other)

    def issuperset(self, other):
        """Returns True if the set is a superset of another set, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.issuperset(other)

    def pop(self):
        """Removes and returns an arbitrary element from the set, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.pop()

    def remove(self, value):
        """Removes an element from the set, thread-safe. Raises KeyError if not present."""
        with self._lock:  # Ensure thread safety
            self._data.remove(value)

    def symmetric_difference(self, other):
        """Returns a new set with elements in either the set or other but not both, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.symmetric_difference(other)

    def symmetric_difference_update(self, other):
        """Updates the set with the symmetric difference of itself and another set, thread-safe."""
        with self._lock:  # Ensure thread safety
            self._data.symmetric_difference_update(other)

    def union(self, *others):
        """Returns a new set with all elements from the set and all others, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.union(*others)

    def update(self, *others):
        """Updates the set with elements from all others, thread-safe."""
        with self._lock:  # Ensure thread safety
            self._data.update(*others)
