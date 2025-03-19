
from typing import Any, Iterable

from safethread.AbstractLock import AbstractLock
from safethread.datatype.AbstractSafeList import AbstractSafeList

from safethread.thread.datatype.ThreadRLock import ThreadRLock


class ThreadSafeList(AbstractSafeList):

    def __init__(self, data: list | Iterable | None = None):
        super().__init__(data)
        self._data: list

    def _create_data(self, data: Any | None) -> Any:
        if isinstance(data, list):
            return data
        return list(data or [])

    def _create_lock(self) -> AbstractLock:
        return ThreadRLock()
