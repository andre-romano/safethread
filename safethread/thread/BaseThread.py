import threading

from typing import Any, Callable, Iterable, Self


class BaseThread:
    """
    A base class for managing threads with thread safety.

    This class provides a structure for creating and managing threads using the threading module.
    It also ensures that the thread's operations are protected by a reentrant lock (_lock) to ensure thread safety.
    """

    class CallableException(Exception):
        """Raised if a callable argument is not a Callable class (e.g., lambda, function, etc)"""

    @staticmethod
    def is_callable(callback: Callable) -> Callable:
        """
        Checks if callback is a Callable (function, lambda, etc).

        :param callback: The Callable to check.
        :type callback: Callable
        :raises ThreadBase.CallableException: If the callback argument is not callable.
        :return: The callback Callable.
        :rtype: Callable
        """
        if not callable(callback):
            raise BaseThread.CallableException(
                "'callback' must be a Callable (e.g., function, lambda, etc)"
            )
        return callback

    @staticmethod
    def get_lock():
        """Get a new instance of RLock (reentrant lock)."""
        return threading.RLock()

    def __init__(
        self,
        callback: Callable,
        args: Iterable | None = None,
        daemon: bool = True,
        repeat: bool = False,
        on_end: Callable[[Self], Any] = lambda threadBase: None
    ):
        """
        Initializes the thread.

        :param callback: The Callable to check. Format: callback(*args)
        :type callback: Callable
        :param args: The arguments to pass to the callback() method when the thread starts.
        :type args: Iterable, optional
        :param daemon: If True, the thread will be daemonized. Defaults to True.
        :type daemon: bool, optional
        :param repeat: If True, the thread will repeat the execution of callback until .stop() is called. Defaults to False.
        :type repeat: bool, optional
        :param on_end: The callback to be called when the thread ends.
        :type on_end: Callable[[ThreadBase], None], optional
        """
        self.__on_end: Callable = self.is_callable(on_end)
        self.__callback: Callable = self.is_callable(callback)
        self.__args = tuple(args or [])

        self.__repeat = repeat
        self.__daemon = daemon

        self.__thread_started = False
        self.__thread_terminate = False

        self.__thread = threading.Thread(
            target=self.__run, daemon=self.__daemon
        )

    def __del__(self):
        """Destructor to ensure thread is stopped when object is deleted."""
        self.stop()

    def __run(self):
        """
        The main run loop of the thread. This will repeatedly execute the callback at 
        the given interval (timeout) and stop after the first execution if repeat is False.

        This method runs in a separate thread and should not be called directly.

        MUST NOT BE OVERLOADED.
        """
        while not self.__thread_terminate:
            # Run callback
            self.__callback(*self.__args)
            # Terminate thread if not repeating
            if not self.__repeat:
                self.stop()
        # call on end callback
        self.__on_end(self)

    def get_args(self) -> tuple:
        """Gets the callback args"""
        return self.__args

    def has_started(self) -> bool:
        """
        Checks if the thread has started.

        :return: True if thread has started, otherwise False.
        :rtype: bool
        """
        return self.__thread_started

    def is_alive(self) -> bool:
        """
        Checks if the thread is alive.

        :return: True if thread is alive, otherwise False.
        :rtype: bool
        """
        return self.__thread.is_alive()

    def is_terminated(self) -> bool:
        """
        Checks if the thread has terminated.

        :return: True if thread HAS started and is NOT alive, otherwise False.
        :rtype: bool
        """
        return self.has_started() and not self.is_alive()

    def is_repeatable(self) -> bool:
        """Returns True if thread executes callback repeatedly (until .stop() is called)"""
        return self.__repeat

    def is_daemon(self) -> bool:
        """Return whether this thread is a daemon."""
        return self.__thread.daemon

    def set_daemon(self, daemon: bool):
        """Set whether this thread is a daemon."""
        self.__thread.daemon = daemon

    def start(self):
        """
        Starts the thread.

        This method begins the execution of the thread by calling the __run method in the background.

        :raises RuntimeError: if start() is called more than once on the same thread object.
        """
        if self.__thread_started:
            raise RuntimeError("ThreadBase has already been started.")
        self.__thread.start()
        self.__thread_started = True

    def stop(self):
        """Stops the thread."""
        self.__thread_terminate = True

    def join(self, timeout: float | None = None):
        """
        Joins the thread, waiting for it to finish.

        :param timeout: The maximum time to wait for the thread to finish. Defaults to None.
        :type timeout: float, optional

        :raises RuntimeError: if an attempt is made to join the current thread, or the join() is called before start()
        """
        if not self.__thread_started:
            raise RuntimeError(
                "Cannot join a thread that has not been started.")
        self.__thread.join(timeout)

    def stop_join(self, timeout: float | None = None):
        """
        Calls stop() and join() to stop the thread and wait for it to finish.

        :param timeout: The maximum time to wait for thread to finish. Defaults to None.
        :type timeout: float, optional

        :raises RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        self.stop()
        self.join(timeout=timeout)

    def copy(self) -> Self:
        """Creates a copy of the current thread."""
        return self.__class__(
            callback=self.__callback,
            args=self.__args,
            daemon=self.__daemon,
            repeat=self.__repeat,
            on_end=self.__on_end
        )
