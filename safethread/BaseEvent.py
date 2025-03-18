import multiprocessing.synchronize
import threading


class BaseEvent:
    """
    Base class for event handling.

    This class defines the interface for event objects, which can be set, cleared, or checked if they are set.
    It wraps a threading or multiprocessing event object and provides a consistent interface for both.
    """

    def __init__(self, event: threading.Event | multiprocessing.synchronize.Event) -> None:
        """
        Initialize the BaseEvent instance.

        :param event: The underlying event object to wrap.
        :type event: threading.Event | multiprocessing.synchronize.Event
        """
        super().__init__()

        self.__event = event

    def is_set(self) -> bool:
        """
        Check if the event is set.

        :return: True if the event is set, False otherwise.
        :rtype: bool
        """
        return self.__event.is_set()

    def set(self) -> None:
        """
        Set the event.

        This method sets the event, waking up any threads or processes waiting for it.
        Once set, calls to `wait` will return immediately until the event is cleared.
        """
        self.__event.set()

    def clear(self) -> None:
        """
        Clear the event.

        This method resets the event to the unset state.
        After clearing, calls to `wait` will block until the event is set again.
        """
        self.__event.clear()

    def wait(self, timeout: float | None = None) -> bool:
        """
        Wait for the event to be set.

        This method blocks until the event is set or the timeout expires.

        :param timeout: Maximum time to wait in seconds. If None, wait indefinitely.
        :type timeout: float, optional

        :return: True if the event is set, False if the timeout expired.
        :rtype: bool
        """
        return self.__event.wait(timeout)
