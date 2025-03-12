import time

from typing import Callable, Iterable

from .ThreadBase import ThreadBase


class Scheduler(ThreadBase):
    """
    A thread scheduler that runs a given callback at regular intervals with an optional repeat option.

    :param timeout: Time interval in seconds between each callback execution.
    :type timeout: float
    :param callback: The function (or callable) to execute at each timeout.
    :type callback: Callable
    :param args: Optional arguments to pass to the callback. Defaults to None.
    :type args: Iterable, optional
    :param repeat: Whether the callback should be repeated indefinitely or just once. Defaults to True.
    :type repeat: bool, optional

    <img src="../../../img/thread/Scheduler.svg" alt="" width="100%">
    """

    def __init__(self, timeout: float, callback: Callable, args: Iterable | None = None, repeat: bool = True):
        """
        Initializes the scheduler with the given parameters.

        :param timeout: Time interval in seconds between each callback execution.
        :type timeout: float
        :param callback: The function (or callable) to execute at each timeout.
        :type callback: Callable
        :param args: Optional arguments to pass to the callback. Defaults to None.
        :type args: list, optional
        :param repeat: Whether the callback should be repeated indefinitely or just once. Defaults to True.
        :type repeat: bool, optional

        :raises ThreadBase.CallableException: If 'callback' is not callable.
        """
        super().__init__(
            callback=self.__run_scheduler,
            repeat=repeat
        )

        self.__callback: Callable = self.is_callable(callback)
        # Default to empty list if args is None
        self.__args = tuple(args or [])
        self.__timeout = timeout

    def __run_scheduler(self):
        """
        The main run loop of the scheduler. This will repeatedly execute the callback at 
        the given interval (timeout) and stop after the first execution if repeat is False.

        This method runs in a separate thread and should not be called directly.
        """
        # Wait for timeout before running the callback
        time.sleep(self.__timeout)
        self.__callback(*self.__args)

    def get_timeout(self) -> float:
        """Returns scheduler timeout."""
        return self.__timeout
