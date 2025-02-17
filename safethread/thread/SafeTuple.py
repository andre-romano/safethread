
import sys

from .SafeBaseObj import SafeBaseObj


class SafeTuple(SafeBaseObj):
    def __init__(self, data: tuple | None = None):
        """Initialize a shared tuple with a Lock for thread safety."""
        super().__init__(data or {})
        self._data: tuple

    def count(self, value):
        """Returns the number of occurrences of value in the tuple, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.count(value)

    def index(self, value, start: int = 0, end: int = sys.maxsize):
        """Returns the index of the first occurrence of value, thread-safe."""
        with self._lock:  # Ensure thread safety
            return self._data.index(value, start, end)
