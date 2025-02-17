
from queue import Queue

from .SafeBaseObj import SafeBaseObj


class SafeQueue(Queue, SafeBaseObj):
    def __init__(self, data: Queue | int | None = None):
        """Initialize the thread-safe queue."""
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
