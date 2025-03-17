
from typing import Any, Callable, Iterable, Self, Type

from . import BaseEvent, AbstractLock, AbstractProcess

from .utils import is_callable


def _run_parallel(
        callback: Callable[..., bool],
        args: tuple,
        repeat: bool,
        stop: BaseEvent,
        on_end: Callable[[Exception | None], Any],
):
    """
    The main run loop of the thread / process. This will repeatedly execute the callback at
    the given interval (timeout) and stop after the first execution if repeat is False.

    This method runs in a separate thread / process and should not be called directly.
    """
    try:
        while not stop.is_set():
            res = callback(*args)
            if isinstance(res, bool) and res == False:
                break
            if not repeat:
                break
        on_end(None)
    except Exception as e:
        on_end(e)


def _dummy_callback(*args) -> bool:
    """Dummy callback that does nothing"""
    return True


def _dummy_on_end(e: Exception | None):
    """
    Called when the thread / process terminates

    :param e: Exception if thread / process terminated with error, None otherwise.
    :type e: Exception | None
    """
    pass


class AbstractParallel:
    """
    A base class for managing parallel instances (threads / processes) safely.

    This class provides a structure for creating and managing process / thread classes using the ``multiprocessing`` or `threading` modules.
    It also ensures that the operations are protected by a reentrant locks (_lock) to ensure safety.
    """

    @staticmethod
    def create_lock() -> AbstractLock:
        """Get a new instance of an RLock (reentrant lock)."""
        raise NotImplementedError("create_lock() NOT overloaded")

    def __init__(
        self,
        callback: Callable[..., bool],
        args: Iterable | None = None,
        daemon: bool = True,
        repeat: bool = False,
        on_end: Callable[[Exception | None], Any] = _dummy_on_end,
    ):
        """
        Initializes the process.

        :param callback: The Callable to check. If callback returns False, it calls .stop() to finish the process loop. Format: result = callback(*args)
        :type callback: Callable[..., bool]

        :param args: The arguments to pass to the callback() method when the thread / process starts.
        :type args: Iterable, optional

        :param daemon: If True, the thread / process will be daemonized. Defaults to True.
        :type daemon: bool, optional

        :param repeat: If True, the thread / process will repeat the execution of callback until .stop() is called. Defaults to False.
        :type repeat: bool, optional

        :param on_end: The callback to be called when the thread / process ends. NEEDS TO BE A GLOBAL FUNCTION.
        :type on_end: Callable[[Exception | None], Any], optional
        """
        self.__args = tuple(args or [])

        self.__callback: Callable[..., bool] = _dummy_callback
        self.__callback = is_callable(callback)

        self.__on_end: Callable[[Exception | None], Any] = _dummy_on_end
        self.__on_end = is_callable(on_end)

        self.__repeat = repeat
        self.__daemon = daemon

        self.__process_started = False
        self.__process_terminate = self._create_terminate_event()

        self._process = self._create_process_thread(
            target=_run_parallel,
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
        """Destructor to ensure thread / process is stopped when object is deleted."""
        try:
            self.stop()
        except:
            pass

    def _create_process_thread(self, target: Callable, kwargs: dict, daemon: bool) -> AbstractProcess:
        """
        Creates an instance of AbstractProcess.

        MUST BE OVERLOADED.

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("_create_process_thread() NOT overloaded")

    def _create_terminate_event(self) -> BaseEvent:
        """
        Creates an instance of AbstractEvent to control parallel loop termination. When event is set, loop is terminated.

        MUST BE OVERLOADED.

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("_create_terminate_event() NOT overloaded")

    def get_args(self) -> tuple:
        """
        Gets the callback args

        :return: Args passed to callback
        :rtype: tuple
        """
        return self.__args

    def has_started(self) -> bool:
        """
        Checks if the thread / process has started.

        :return: True if thread / process has started, otherwise False.
        :rtype: bool
        """
        return self.__process_started

    def is_alive(self) -> bool:
        """
        Checks if the process / thread is alive.

        :return: True if process / thread is alive, otherwise False.
        :rtype: bool
        """
        return self._process.is_alive()

    def is_terminated(self) -> bool:
        """
        Checks if the thread / process has terminated.

        :return: True if thread / process HAS started and is NOT alive, otherwise False.
        :rtype: bool
        """
        return self.has_started() and not self.is_alive()

    def is_repeatable(self) -> bool:
        """
        Checks if thread / process executes callback repeatedly (until .stop() is called)

        :return: True if callback is executed repeatedly, False otherwise
        :rtype: bool
        """
        return self.__repeat

    def is_daemon(self) -> bool:
        """
        Return whether this thread / process is a daemon.

        :return: True if daemon, False otherwise
        :rtype: bool
        """
        return self._process.daemon

    def set_daemon(self, daemon: bool):
        """
        Set whether this thread / process is a daemon.

        :param daemon: True to set thread/process as daemon, False otherwise.
        :type daemon: bool
        """
        self._process.daemon = daemon

    def start(self):
        """
        Starts the thread / process.

        This method begins the execution of the thread / process by calling the __run method in the background.

        :raises RuntimeError: if start() is called more than once on the same thread / process object.
        """
        if self.__process_started:
            raise RuntimeError("Thread / Process has already been started.")
        self._process.start()
        self.__process_started = True

    def stop(self):
        """Stops the thread / process."""
        self.__process_terminate.set()

    def join(self, timeout: float | None = None):
        """
        Joins the thread / process, waiting for it to finish.

        :param timeout: The maximum time to wait for the thread / process to finish. Defaults to None.
        :type timeout: float, optional
        """
        if not self.__process_started:
            raise RuntimeError(
                "Cannot join a thread / process that has not been started.")
        self._process.join(timeout=timeout)

    def stop_join(self, timeout: float | None = None):
        """
        Calls stop() and join() to stop the thread / process and wait for it to finish.

        :param timeout: The maximum time to wait for thread / process to finish. Defaults to None.
        :type timeout: float, optional
        """
        self.stop()
        self.join(timeout=timeout)

    def copy(self) -> Self:
        """
        Creates a copy of the current thread / process.

        :return: Copy of this object
        :rtype: Self
        """
        return self.__class__(
            callback=self.__callback,
            args=self.__args,
            daemon=self.__daemon,
            repeat=self.__repeat,
            on_end=self.__on_end
        )
