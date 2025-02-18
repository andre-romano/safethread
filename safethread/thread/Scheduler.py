
import time

from typing import Any, Callable

from .ThreadBase import ThreadBase


class Scheduler(ThreadBase):
    """
    A thread scheduler that runs a given callback at regular intervals with an optional repeat option.

    Args:

        timeout (float): Time interval in seconds between each callback execution.

        callback (Callable): The function (or callable) to execute at each timeout.

        args (list, optional): Optional arguments to pass to the callback. Defaults to None.

        repeat (bool, optional): Whether the callback should be repeated indefinitely or just once. Defaults to True.
    """

    def __init__(self, timeout: float, callback: Callable, args: list | None = None, repeat: bool = True):
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
        super().__init__(args=[])  # Assuming ThreadBase expects args to be passed this way
        self.check_callable(callback)

        self._timeout = timeout
        self._callback: Callable = callback
        self._args = args or []  # Default to empty list if args is None
        self._repeat = repeat
        self._terminate = False

    def _run(self):
        """
        The main run loop of the scheduler. This will repeatedly execute the callback at 
        the given interval (timeout) and stop after the first execution if repeat is False.

        This method runs in a separate thread and should not be called directly.
        """
        while not self._terminate:
            # Wait for timeout before running the callback
            time.sleep(self._timeout)
            self._callback(*self._args)
            # Terminate thread if not repeating
            if not self._repeat:
                self.stop()

    def stop(self):
        """
        Stops the scheduler thread.

        This will stop the thread loop in the scheduler and prevent further callback executions.
        """
        self._terminate = True

    def get_timeout(self) -> float:
        """"Returns scheduler timeout"""
        return self._timeout

    def is_repeatable(self) -> bool:
        """"Returns True if scheduler executes callback repeatedly (until .stop() is called)"""
        return self._repeat
