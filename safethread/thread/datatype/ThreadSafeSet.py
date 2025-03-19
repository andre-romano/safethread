from typing import Any, Iterable

from safethread.thread.datatype.ThreadRLock import ThreadRLock

from safethread.AbstractLock import AbstractLock

from safethread.datatype.AbstractSafeSet import AbstractSafeSet


class ThreadSafeSet(AbstractSafeSet):
    def __init__(self, data: set | Iterable | None = None):
        """
        Initialize a shared set with a Lock for thread safety.

        :param data: The initial data to populate the set with.
        :type data: set, Iterable, or None
        """
        super().__init__(data)
        self._data: set

    def _create_data(self, data: Any | None) -> Any:
        if isinstance(data, set):
            return data
        return set(data or [])

    def _create_lock(self) -> AbstractLock:
        return ThreadRLock()
