from queue import Queue

from . import SafeThreadBase


class SafeThreadQueue(Queue, SafeThreadBase):
    def __init__(self, data: Queue | int | None = None):
        """
        Initialize the thread-safe queue.

        If a `Queue` is provided, its items are copied into the new queue.
        If an integer is provided, it sets the maximum size of the queue.
        If no argument is provided, the queue is initialized with an unlimited size.

        :param data: The initial data to populate the queue with, or the maximum size.
        :type data: Queue, int, or None
        """
        maxsize = 0
        if isinstance(data, int):
            maxsize = data
        elif isinstance(data, Queue):
            maxsize = data.maxsize
        super().__init__(maxsize)

        # copy data
        if isinstance(data, Queue):
            while not data.empty():
                self.put(data.get())
