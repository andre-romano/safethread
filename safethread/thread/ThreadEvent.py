
import threading

from .. import AbstractEvent


class ThreadEvent(AbstractEvent):
    """
    A thread-safe class to handle events using threading.
    """

    def __init__(self) -> None:
        """
        Initializes the ProcessEvent instance.
        """
        self.__event = 0
        self.__lock = threading.RLock()

    def is_set(self) -> bool:
        """Checks if event is set"""
        return self.__event == 1

    def set(self):
        """Sets event"""
        with self.__lock:
            self.__event = 1
