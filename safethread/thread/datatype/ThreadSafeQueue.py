
import queue

from threading import Condition
from typing import Any

from .ThreadRLock import ThreadRLock

from ... import AbstractLock

from ...datatype import AbstractSafeQueue


class ThreadSafeQueue(AbstractSafeQueue):
    def __init__(self, data: queue.Queue | int | None = None):
        """
        Initialize the thread-safe queue.

        If a `Queue` is provided, its items are copied into the new queue.
        If an integer is provided, it sets the maximum size of the queue.
        If no argument is provided, the queue is initialized with an unlimited size.

        :param data: The initial data to populate the queue with, or the maximum size.
        :type data: Queue, int, or None
        """
        super().__init__(data)
        self._data: queue.Queue

    def _create_data(self, data: Any | None) -> Any:
        maxsize = 0
        if not data:
            maxsize = 0
        elif isinstance(data, int):
            maxsize = data
        elif isinstance(data, queue.Queue):
            maxsize = data.maxsize
        else:
            raise TypeError(
                "Queue create failed, provided argument is not int | queue.Queue")

        # create queue
        queue_instance = queue.Queue(maxsize)

        # copy data
        if isinstance(data, queue.Queue):
            while not data.empty():
                queue_instance.put(data.get())
        return queue_instance

    def _create_lock(self) -> AbstractLock:
        return ThreadRLock()

    def join(self):
        """
        Blocks until all items in the Queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer thread calls task_done()
        to indicate the item was retrieved and all work on it is complete.

        When the count of unfinished tasks drops to zero, join() unblocks.
        """
        self._data.join()

    def shutdown(self, immediate: bool = False):
        """
        Shut-down the queue, making queue gets and puts raise ShutDown.

        By default, gets will only raise once the queue is empty. Set
        'immediate' to True to make gets raise immediately instead.

        All blocked callers of put() and get() will be unblocked. If
        'immediate', a task is marked as done for each item remaining in
        the queue, which may unblock callers of join().
        """

        self._data.shutdown(immediate=immediate)

    def qsize(self) -> int:
        """
        Return the approximate size of the queue (not reliable!).
        """
        return self._data.qsize()

    def task_done(self):
        """
        This method should be used by consumer threads of the queue. For each `get()` used to fetch a task, a subsequent call to `task_done()` 
        informs the queue that the processing on the task is complete.

        If a `join()` is currently blocking, it will resume when all items have been processed, meaning that a `task_done()` call was received 
        for every item that had been put into the queue.

        The `shutdown(immediate=True)` method calls `task_done()` for each remaining item in the queue.

        :raises ValueError: If called more times than there were items placed in the queue.
        """
        return self._data.task_done()

    def clear(self):
        """Clears the queue"""
        self._data.queue.clear()

    @property
    def unfinished_tasks(self) -> int:
        return self._data.unfinished_tasks

    @property
    def all_tasks_done(self) -> Condition:
        return self._data.all_tasks_done

    @property
    def is_shutdown(self) -> bool:
        """True if queue has been shutdown, False otherwise"""
        return self._data.is_shutdown

    @property
    def maxsize(self) -> int:
        """Get queue maximum size"""
        return self._data.maxsize

    @maxsize.setter
    def maxsize(self, value: int):
        """Set queue maximum size"""
        self._data.maxsize = value
