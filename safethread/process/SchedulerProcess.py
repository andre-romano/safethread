import time

from typing import Callable, Iterable

from . import BaseProcess

from ..utils import is_callable


def _dummy_callback(*args) -> bool:
    """Dummy callback"""
    return False


def _run_scheduler(timeout: float, callback: Callable[..., bool], args: tuple) -> bool:
    """
    The main run loop of the scheduler. This will repeatedly execute the callback at 
    the given interval (timeout) and stop after the first execution if repeat is False.

    If callback() returns False, stop scheduler process.

    This method runs in a separate process and should not be called directly.
    """
    # Wait for timeout before running the callback
    time.sleep(timeout)
    return callback(*args)


class SchedulerProcess(BaseProcess):
    """
    A process scheduler that runs a given callback at regular intervals with an optional repeat option.

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

        :param callback: The global function to execute at each timeout. NEEDS TO BE GLOBAL FUNCTION.
        :type callback: Callable[..., bool]

        :param args: Optional arguments to pass to the callback. Arguments must be pickable (serializable). Defaults to None.
        :type args: Iterable, optional

        :param repeat: Whether the callback should be repeated indefinitely or just once. Defaults to True.
        :type repeat: bool, optional

        :raises TypeError: If 'callback' is not callable.
        """
        # exception handling
        exception: Exception | None = None

        self.__timeout: float = timeout

        self.__args = tuple(args or [])
        self.__callback: Callable[..., bool] = _dummy_callback
        try:
            self.__callback = is_callable(callback)
        except Exception as e:
            exception = e

        super().__init__(
            callback=_run_scheduler,
            args=[
                self.__timeout,
                self.__callback,
                self.__args,
            ],
            repeat=repeat,
        )

        # raise exception if needed
        if exception:
            raise exception

    def get_args(self) -> tuple:
        return self.__args

    def get_timeout(self) -> float:
        """Returns scheduler timeout."""
        return self.__timeout
