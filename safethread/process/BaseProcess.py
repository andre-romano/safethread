import multiprocessing

from multiprocessing.sharedctypes import Synchronized

from typing import Any, Callable, Iterable, Self

from ..utils import *


def _run_process(
        callback: Callable[..., bool],
        args: tuple,
        repeat: bool,
        stop: Synchronized,
        on_end: Callable,
):
    """
    The main run loop of the process. This will repeatedly execute the callback at 
    the given interval (timeout) and stop after the first execution if repeat is False.

    This method runs in a separate process and should not be called directly.
    """
    try:
        while stop.value == 0:
            res = callback(*args)
            if isinstance(res, bool) and res == False:
                break
            if not repeat:
                break
        on_end(None)
    except Exception as e:
        on_end(e)


def _on_end(e: Exception | None):
    """
    Called when the process terminates

    :param e: Exception if process terminated with error, None otherwise.
    :type e: Exception | None
    """
    pass


class BaseProcess:
    """
    A base class for managing processes safely.

    This class provides a structure for creating and managing processes using the ``multiprocessing`` module.
    It also ensures that the process's operations are protected by a reentrant lock (_lock) to ensure process safety.
    """

    @staticmethod
    def get_lock():
        """Get a new instance of multiprocessing.RLock (reentrant lock)."""
        return multiprocessing.RLock()

    def __init__(
        self,
        callback: Callable[..., bool],
        args: Iterable | None = None,
        daemon: bool = True,
        repeat: bool = False,
        on_end: Callable[[Exception | None], Any] = _on_end
    ):
        """
        Initializes the process.

        :param callback: The Callable to check. If callback returns False, it calls .stop() to finish the process loop. Format: result = callback(*args)
        :type callback: Callable[..., bool]

        :param args: The arguments to pass to the callback() method when the process starts.
        :type args: Iterable, optional

        :param daemon: If True, the process will be daemonized. Defaults to True.
        :type daemon: bool, optional

        :param repeat: If True, the process will repeat the execution of callback until .stop() is called. Defaults to False.
        :type repeat: bool, optional

        :param on_end: The callback to be called when the process ends. NEEDS TO BE A GLOBAL FUNCTION.
        :type on_end: Callable[[], None], optional
        """
        self.__on_end: Callable = is_callable(on_end)

        self.__callback: Callable[..., bool] = is_callable(callback)
        self.__args = tuple(args or [])

        self.__repeat = repeat
        self.__daemon = daemon

        self.__process_started = False
        self.__process_terminate = multiprocessing.Value('i', 0)

        self.__process = multiprocessing.Process(
            target=_run_process,
            kwargs={
                "callback": self.__callback,
                "args": self.__args,
                "repeat": self.__repeat,
                "stop": self.__process_terminate,
                "on_end": self.__on_end,
            },
            daemon=self.__daemon
        )

    def __del__(self):
        """Destructor to ensure process is stopped when object is deleted."""
        self.stop()

    def get_args(self) -> tuple:
        """Gets the callback args"""
        return self.__args

    def has_started(self) -> bool:
        """
        Checks if the process has started.

        :return: True if process has started, otherwise False.
        :rtype: bool
        """
        return self.__process_started

    def is_alive(self) -> bool:
        """
        Checks if the process is alive.

        :return: True if process is alive, otherwise False.
        :rtype: bool
        """
        return self.__process.is_alive()

    def is_terminated(self) -> bool:
        """
        Checks if the process has terminated.

        :return: True if process HAS started and is NOT alive, otherwise False.
        :rtype: bool
        """
        return self.has_started() and not self.is_alive()

    def is_repeatable(self) -> bool:
        """Returns True if process executes callback repeatedly (until .stop() is called)"""
        return self.__repeat

    def is_daemon(self) -> bool:
        """Return whether this process is a daemon."""
        return self.__process.daemon

    def set_daemon(self, daemon: bool):
        """Set whether this process is a daemon."""
        self.__process.daemon = daemon

    def start(self):
        """
        Starts the process.

        This method begins the execution of the process by calling the __run method in the background.

        :raises RuntimeError: if start() is called more than once on the same process object.
        """
        if self.__process_started:
            raise RuntimeError("Process has already been started.")
        self.__process.start()
        self.__process_started = True

    def stop(self):
        """Stops the process."""
        with self.__process_terminate.get_lock():
            self.__process_terminate.value = 1

    def join(self, timeout: float | None = None):
        """
        Joins the process, waiting for it to finish.

        :param timeout: The maximum time to wait for the process to finish. Defaults to None.
        :type timeout: float, optional
        """
        if not self.__process_started:
            raise RuntimeError(
                "Cannot join a process that has not been started.")
        self.__process.join(timeout)

    def stop_join(self, timeout: float | None = None):
        """
        Calls stop() and join() to stop the process and wait for it to finish.

        :param timeout: The maximum time to wait for process to finish. Defaults to None.
        :type timeout: float, optional
        """
        self.stop()
        self.join(timeout=timeout)

    def copy(self) -> Self:
        """Creates a copy of the current process."""
        return self.__class__(
            callback=self.__callback,
            args=self.__args,
            daemon=self.__daemon,
            repeat=self.__repeat,
            on_end=self.__on_end
        )
