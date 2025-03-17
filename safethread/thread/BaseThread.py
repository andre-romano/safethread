import threading

from typing import Any, Callable, Iterable, Self

from .datatype import ThreadRLock

from .ThreadEvent import ThreadEvent

from .. import AbstractParallel, BaseEvent, AbstractProcess, AbstractLock


class BaseThread(AbstractParallel):
    """
    A base class for managing threads with thread safety.

    This class provides a structure for creating and managing threads using the threading module.
    It also ensures that the thread's operations are protected by a reentrant lock (_lock) to ensure thread safety.
    """

    @staticmethod
    def create_lock() -> AbstractLock:
        """Get a new instance of RLock (reentrant lock)."""
        return ThreadRLock()

    def _create_process_thread(self, target: Callable, kwargs: dict, daemon: bool) -> AbstractProcess:
        """
        Creates an instance of threading.Thread object.

        :param target: The callable (function, lambda, etc) to be invoked by the thread.
        :type target: Callable

        :param kwargs: A dictionary of keyword arguments to pass to the target callable.
        :type kwargs: dict

        :param daemon: Whether the process should be a daemon process.
        :type daemon: bool

        :return: An instance of multiprocessing.Process.
        :rtype: AbstractProcess
        """
        return threading.Thread(
            target=target,
            kwargs=kwargs,
            daemon=daemon,
        )

    def _create_terminate_event(self) -> BaseEvent:
        return ThreadEvent()

    def join(self, timeout: float | None = None):
        """
        Joins the thread, waiting for it to finish.

        :param timeout: The maximum time to wait for the thread to finish. Defaults to None.
        :type timeout: float, optional

        :raises RuntimeError: if an attempt is made to join the current thread, or the join() is called before start()
        """
        super().join(timeout=timeout)

    def stop_join(self, timeout: float | None = None):
        """
        Calls stop() and join() to stop the thread and wait for it to finish.

        :param timeout: The maximum time to wait for thread to finish. Defaults to None.
        :type timeout: float, optional

        :raises RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        super().stop_join(timeout=timeout)
