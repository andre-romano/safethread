
import multiprocessing

from .. import AbstractEvent


class ProcessEvent(AbstractEvent):
    """
    A process-safe class to handle events using multiprocessing.
    """

    def __init__(self) -> None:
        """
        Initializes the ProcessEvent instance.
        """
        self.__event = multiprocessing.Value('i', 0)

    def is_set(self) -> bool:
        """Checks if event is set"""
        return self.__event.value == 1

    def set(self):
        """Sets event"""
        with self.__event.get_lock():
            self.__event.value = 1
