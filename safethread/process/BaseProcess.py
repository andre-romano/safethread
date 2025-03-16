import multiprocessing

from typing import Any, Callable, Iterable, Self

from .ProcessEvent import ProcessEvent

from .. import AbstractParallel, AbstractEvent, AbstractProcess


class BaseProcess(AbstractParallel):
    """
    A base class for managing processes safely.

    This class provides a structure for creating and managing processes using the ``multiprocessing`` module.
    It also ensures that the process's operations are protected by a reentrant lock (_lock) to ensure process safety.
    """

    @staticmethod
    def get_lock():
        """Get a new instance of multiprocessing.RLock (reentrant lock)."""
        return multiprocessing.RLock()

    def _create_process_thread(self, target: Callable, kwargs: dict, daemon: bool) -> AbstractProcess:
        """
        Creates an instance of multiprocessing.Process object.

        :param target: The global function to be invoked by the process. NEEDS TO BE GLOBAL.
        :type target: Callable

        :param kwargs: A dictionary of keyword arguments to pass to the target callable.
        :type kwargs: dict

        :param daemon: Whether the process should be a daemon process.
        :type daemon: bool

        :return: An instance of multiprocessing.Process.
        :rtype: AbstractProcess
        """
        return multiprocessing.Process(
            target=target,
            kwargs=kwargs,
            daemon=daemon,
        )

    def _create_event(self) -> AbstractEvent:
        """
        Create and return a new event instance.

        This method is responsible for creating a new instance of the `ProcessEvent` class,
        which implements the `AbstractEvent` interface.

        :return: A new instance of `ProcessEvent`.
        :rtype: AbstractEvent
        """
        return ProcessEvent()
