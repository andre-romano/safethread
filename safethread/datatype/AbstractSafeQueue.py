

import queue

import multiprocessing
import multiprocessing.queues

from typing import Any, Iterable, Self

from .AbstractSafeBase import AbstractSafeBase


class AbstractSafeQueue(AbstractSafeBase):
    """
    AbstractSafeQueue is a safe queue that can be initialized with a standard queue (for threads), 
    a multiprocessing queue, an integer representing the maximum size, or None for an unlimited size queue.
    """

    def __iter__(self):
        """
        Returns an iterator over the queue's items. Since multiprocessing.Queue is not directly iterable,
        we dequeue items until empty (not thread-safe for concurrent access).

        :return: Generator yielding queue items.
        """
        # Temporarily store all items in a list
        with self._lock:
            temp_items = []
            while not self._data.empty():
                temp_items.append(self._data.get())

            # Re-enqueue the items back into the queue
            for item in temp_items:
                self._data.put(item)

            # Yield items from the temporary list
            yield from temp_items

    def __init__(self, data: queue.Queue | multiprocessing.queues.Queue | int | Iterable | None = None):
        """
        Initialize the safe queue.

        - If a `Queue` is provided, its items are copied into the new queue.
        - If an integer is provided, it sets the maximum size of the queue.
        - If an Iterable is provided, it populates the queue with those items.
        - If no argument is provided, the queue is initialized with an unlimited size.

        :param data: The initial data to populate the queue with, or the maximum size.
        :type data: queue.Queue, multiprocessing.queues.Queue, int, or None
        """
        super().__init__(data)
        self._data: queue.Queue | multiprocessing.queues.Queue

    def _init_with_data(self, instance: queue.Queue | multiprocessing.queues.Queue, data: queue.Queue | multiprocessing.queues.Queue | Iterable):
        """
        Initialize a queue instance with data from another queue or an iterable.

        :param instance: The queue instance to be initialized.
        :type instance: queue.Queue, multiprocessing.queues.Queue

        :param data: The data source to initialize the queue with. It can be another queue or an iterable.
        :type data: queue.Queue, multiprocessing.queues.Queue, Iterable
        """
        if isinstance(data, queue.Queue) or isinstance(data, multiprocessing.queues.Queue):
            while not data.empty():
                instance.put(data.get())
        elif isinstance(data, Iterable):
            for item in data:
                instance.put(item)

    def copy_obj(self) -> Self:
        with self._lock:
            # Temporarily store all items in a list
            temp_items = []
            while not self._data.empty():
                temp_items.append(self._data.get())

            # Re-enqueue the items back into the queue
            for item in temp_items:
                self._data.put(item)
            return self._create_data(temp_items)

    def empty(self) -> bool:
        """
        Return True if the queue is empty, False otherwise (not reliable!).

        This method is likely to be removed at some point. Use qsize() == 0
        as a direct substitute, but be aware that either approach risks a race
        condition where a queue can grow before the result of empty() or
        qsize() can be used.

        To create code that needs to wait for all queued tasks to be
        completed, the preferred technique is to use the join() method
        """
        return self._data.empty()

    def full(self):
        """
        Return True if the queue is full, False otherwise (not reliable!).

        This method is likely to be removed at some point. Use qsize() >= n
        as a direct substitute, but be aware that either approach risks a race
        condition where a queue can shrink before the result of full() or
        qsize() can be used.
        """
        return self._data.full()

    def get_nowait(self) -> Any:
        """
        Retrieve an item from the queue without blocking.
        :raises queue.Empty: If no item is available.
        """
        return self._data.get_nowait()

    def put_nowait(self, item: Any):
        """
        Put an item into the queue without blocking.
        :raises queue.Full: If no free slot is available.
        """
        self._data.put_nowait(item)

    def get(self, block: bool = True, timeout: float | None = None) -> Any:
        """
        Retrieve an item from the queue.

        :param block: If True, block until an item is available. If False, return an item if one is immediately available, else raise the Empty exception. Default is True.
        :type block: bool, optional

        :param timeout: The maximum time to wait for an item. If None, wait indefinitely. If a positive number, block for at most the specified number of seconds. Default is None.
        :type timeout: float, optional

        :return: The item retrieved from the queue.
        :rtype: Any

        :raises queue.Empty: If no item is available and block is False or the timeout expires.
        """
        return self._data.get(block=block, timeout=timeout)

    def put(self, item: Any, block: bool = True, timeout: float | None = None):
        """
        Put an item into the queue.

        :param item: The item to be put into the queue.
        :type item: Any

        :param block: If True, blocks until a free slot is available. If False, raises the Full exception if no free slot is immediately available.
        :type block: bool, optional

        :param timeout: The maximum time to wait for a free slot. If None, waits indefinitely.
        :type timeout: float or None, optional

        :raises queue.Full: If no free slot is available and block is False or the timeout expires.
        """
        self._data.put(item, block=block, timeout=timeout)

    def qsize(self) -> int:
        """
        Return the approximate size of the queue (not reliable!).
        """
        return self._data.qsize()

    def clear(self):
        """
        Clears the queue

        :raises NotImplementedError: Method NOT overloaded.
        """
        raise NotImplementedError("Method NOT overloaded")
