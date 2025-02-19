
import time

from typing import Any, Callable, Iterable

from .ThreadBase import ThreadBase


class Scheduler(ThreadBase):
    """
    A thread scheduler that runs a given callback at regular intervals with an optional repeat option.

    Args:

        timeout (float): Time interval in seconds between each callback execution.

        callback (Callable): The function (or callable) to execute at each timeout.

        args (Iterable, optional): Optional arguments to pass to the callback. Defaults to None.

        repeat (bool, optional): Whether the callback should be repeated indefinitely or just once. Defaults to True.
    """

    def __init__(self, timeout: float, callback: Callable, args: Iterable | None = None, repeat: bool = True):
        """
        Initializes the scheduler with the given parameters.

        Args:

            timeout (float): Time interval in seconds between each callback execution.

            callback (Callable): The function (or callable) to execute at each timeout.

            args (list, optional): Optional arguments to pass to the callback. Defaults to None.

            repeat (bool, optional): Whether the callback should be repeated indefinitely or just once. Defaults to True.

        Raises:

            ThreadBase.CallableException: If 'callback' is not callable.
        """
        super().__init__(
            callback=self.__run_scheduler,
            repeat=repeat
        )

        self.__callback: Callable = self.check_callable(callback)
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
        """Returns scheduler timeout"""
        return self.__timeout
