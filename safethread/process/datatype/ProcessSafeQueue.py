
import multiprocessing
import multiprocessing.queues

from typing import Any, Iterable, Self


from ... import AbstractLock
from ...datatype import AbstractSafeQueue

from . import ProcessRLock


class ProcessSafeQueue(AbstractSafeQueue):

    def __eq__(self, other) -> bool:
        """
        Method NOT implemented.

        :raises NotImplementedError: Always (Method NOT implemented - cannot compare multiprocessing.Queue's)
        """
        raise NotImplementedError("Cannot compare multiprocessing.Queue")

    def __init__(self, data: multiprocessing.queues.Queue | int | Iterable | None = None):
        self.__maxsize: int = 0
        self._data: multiprocessing.queues.Queue

        super().__init__(data)

    def _create_data(self, data: Any | None) -> Any:
        if not data:
            self.__maxsize = 0
        elif isinstance(data, int):
            self.__maxsize = data
        elif isinstance(data, multiprocessing.queues.Queue):
            self.__maxsize = 0
        elif not isinstance(data, Iterable) or isinstance(data, str):
            raise TypeError(
                "Queue create failed, provided argument is not int | multiprocessing.queues.Queue")

        # create queue
        instance = multiprocessing.Queue(maxsize=self.maxsize)

        # initialize queue with provided data
        if (isinstance(data, multiprocessing.queues.Queue) or
                isinstance(data, Iterable)):
            self._init_with_data(instance, data)
        return instance

    def _create_lock(self) -> AbstractLock:
        return ProcessRLock()

    def shutdown(self):
        """
        Shut-down the queue.

        Will block until queue is properly finished.
        """
        self._data.close()
        self._data.join_thread()

    def clear(self):
        """Clears the queue"""
        with self._lock:
            while not self._data.empty():
                self._data.get()

    @property
    def maxsize(self) -> int:
        """Get queue maximum size"""
        return self.__maxsize
