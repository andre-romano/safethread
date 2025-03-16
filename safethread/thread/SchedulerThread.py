import time

from typing import Callable, Iterable

from . import BaseThread

from ..utils import *


def _dummy_callback(*args) -> bool:
    """Dummy callback"""
    return False


class SchedulerThread(BaseThread):
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

    def __init__(self, timeout: float, callback: Callable[..., bool], args: Iterable | None = None, repeat: bool = True):
        """
        Initializes the scheduler with the given parameters.

        :param timeout: Time interval in seconds between each callback execution.
        :type timeout: float

        :param callback: The function (or callable) to execute at each timeout.
        :type callback: Callable[..., bool]

        :param args: Optional arguments to pass to the callback. Defaults to None.
        :type args: list, optional

        :param repeat: Whether the callback should be repeated indefinitely or just once. Defaults to True.
        :type repeat: bool, optional

        :raises TypeError: If 'callback' is not callable.
        """
        super().__init__(
            callback=self._run_scheduler,
            repeat=repeat,
        )

        # Default to empty list if args is None
        self.__timeout: float = timeout

        self.__callback: Callable[..., bool] = _dummy_callback
        self.__callback = is_callable(callback)

        self.__args = tuple(args or [])

    def _run_scheduler(self) -> bool:
        """
        The main run loop of the scheduler. This will repeatedly execute the callback at 
        the given interval (timeout) and stop after the first execution if repeat is False.

        If callback() returns False, stop scheduler thread.

        This method runs in a separate thread and should not be called directly.
        """
        # Wait for timeout before running the callback
        time.sleep(self.__timeout)
        return self.__callback(*self.__args)

    def get_args(self) -> tuple:
        return self.__args

    def get_timeout(self) -> float:
        """Returns scheduler timeout."""
        return self.__timeout
