
from typing import Any, Iterable

from safethread.AbstractLock import AbstractLock

from safethread.datatype.AbstractSafeDict import AbstractSafeDict

from safethread.thread.datatype.ThreadRLock import ThreadRLock


class ThreadSafeDict(AbstractSafeDict):
    def __init__(self, data: dict | Iterable | None = None):
        """
        Initialize a shared dictionary with a Lock for thread safety.

        :param data: Initial data to populate the dictionary. Defaults to None.
        :type data: dict or Iterable, optional
        """
        super().__init__(data)
        self._data: dict

    def _create_data(self, data: Any | None) -> Any:
        if isinstance(data, dict):
            return data
        return dict(data or {})

    def _create_lock(self) -> AbstractLock:
        return ThreadRLock()

    def fromkeys(self, iterable: Iterable, value: Any | None = None):
        """
        Create a new dictionary with keys from an iterable and values set to a specified value.

        :param iterable: Iterable containing the keys for the new dictionary.
        :type iterable: Iterable
        :param value: Value assigned to each key. Defaults to None.
        :type value: Any, optional

        :return: A new dictionary with the specified keys and values.
        :rtype: dict
        """
        with self._lock:
            return self._data.fromkeys(iterable, value)
