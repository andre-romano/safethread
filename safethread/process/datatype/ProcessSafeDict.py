
import multiprocessing

from multiprocessing.managers import DictProxy
from typing import Any, Iterable

from ... import AbstractLock
from ...datatype import AbstractSafeDict

from .ProcessRLock import ProcessRLock


class ProcessSafeDict(AbstractSafeDict):
    def __eq__(self, other) -> bool:
        if isinstance(other, ProcessSafeDict):
            return dict(self._data) == dict(other._data)
        return self == ProcessSafeDict(other)

    def __init__(self, data: dict | Iterable | None = None):
        """
        Initialize a process-safe dictionary.

        :param data: Initial data to populate the dictionary. Defaults to None.
        :type data: dict or Iterable, optional
        """
        super().__init__(data)
        self._data: DictProxy

    def _create_data(self, data: Any | None) -> Any:
        if isinstance(data, DictProxy):
            return data
        return multiprocessing.Manager().dict(data or {})

    def _create_lock(self) -> AbstractLock:
        return ProcessRLock()
