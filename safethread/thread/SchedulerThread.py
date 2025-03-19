

from safethread.AbstractScheduler import AbstractScheduler

from safethread.thread.BaseThread import BaseThread


class SchedulerThread(AbstractScheduler, BaseThread):
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
    pass
