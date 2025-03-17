
import multiprocessing

from multiprocessing.managers import ListProxy
from typing import Any, Iterable

from ... import AbstractLock
from ...datatype import AbstractSafeList

from .ProcessRLock import ProcessRLock


class ProcessSafeList(AbstractSafeList):

    def __eq__(self, other) -> bool:
        if isinstance(other, ProcessSafeList):
            return list(self._data) == list(other._data)
        return self == ProcessSafeList(other)

    def __lt__(self, other):
        if isinstance(other, ProcessSafeList):
            return list(self._data) < list(other._data)
        return self < ProcessSafeList(other)

    def __gt__(self, other):
        if isinstance(other, ProcessSafeList):
            return list(self._data) > list(other._data)
        return self > ProcessSafeList(other)

    def __init__(self, data: list | Iterable | None = None):
        """
        Initialize a process-safe list.

        :param data: Initial data to populate the list. Defaults to None.
        :type data: list or Iterable, optional
        """
        super().__init__(data)
        self._data: ListProxy

    def _create_data(self, data: Any | None) -> Any:
        if isinstance(data, ListProxy):
            return data
        return multiprocessing.Manager().list(data or [])

    def _create_lock(self) -> AbstractLock:
        return ProcessRLock()

    def clear(self):
        """
        Clears the list safely.

        **Complexity:** O(N)
        """
        with self._lock:
            while len(self._data) > 0:
                self._data.pop()
