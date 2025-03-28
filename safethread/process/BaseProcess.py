import multiprocessing

from typing import Any, Callable, Iterable, Self

from safethread.process.datatype.ProcessRLock import ProcessRLock

from safethread.process.ProcessEvent import ProcessEvent

from safethread.AbstractParallel import AbstractParallel
from safethread.BaseEvent import BaseEvent
from safethread.AbstractProcess import AbstractProcess
from safethread.AbstractLock import AbstractLock


class BaseProcess(AbstractParallel):
    """
    A base class for managing processes safely.

    This class provides a structure for creating and managing processes using the ``multiprocessing`` module.
    It also ensures that the process's operations are protected by a reentrant lock (_lock) to ensure process safety.
    """

    @staticmethod
    def create_lock() -> AbstractLock:
        """Get a new instance of multiprocessing.RLock (reentrant lock)."""
        return ProcessRLock()

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

    def _create_terminate_event(self) -> BaseEvent:
        """
        Create and return a new event instance.

        This method is responsible for creating a new instance of the `ProcessEvent` class,
        which implements the `AbstractEvent` interface.

        :return: A new instance of `ProcessEvent`.
        :rtype: AbstractEvent
        """
        return ProcessEvent()

    def stop(self):
        super().stop()
        try:
            self._process: multiprocessing.Process
            self._process.kill()
        except:
            pass

    def get_exitcode(self) -> int | None:
        """Return exit code of process or ``None`` if it has yet to stop"""
        return self._process.exitcode
