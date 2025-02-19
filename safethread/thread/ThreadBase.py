import threading

from typing import Callable, Iterable


class ThreadBase:
    """
    A base class for managing threads with thread safety.

    This class provides a structure for creating and managing threads using the threading module.
    It also ensures that the thread's operations are protected by a reentrant lock (_lock) to ensure thread safety.
    """

    class CallableException(Exception):
        """"Raised if a callable argument is not a Callable class (e.g., lambda, function, etc)"""

        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    @staticmethod
    def is_callable(callback: Callable) -> Callable:
        """
        Checks if callback is a Callable (function, lambda, etc).

        Args:

            callback (Callable): The Callable to check.

        Raises:

            ThreadBase.CallableException: If the callback argument is not callable.

        Returns:

            callback (Callable): The callback Callable
        """
        if not isinstance(callback, Callable):
            raise ThreadBase.CallableException(
                "'callback' must be a Callable (e.g., function, lambda, etc)"
            )
        return callback

    @staticmethod
    def get_lock():
        """Get a new instance of RLock (reentrant lock)"""
        return threading.RLock()

    def __init__(self, callback: Callable, args: Iterable | None = None, daemon: bool = True, repeat: bool = False):
        """
        Initializes the thread and the reentrant lock.

        Args:

            callback (Callable): The Callable to check. Format: callback(*args)

            args (Iterable, optional): The arguments to pass to the callback() method when the thread starts.

            daemon (bool, optional): If True, the thread will be daemonized. Defaults to True.

            repeat (bool, optional): If True, the thread will repeat the execution of callback until .stop() is called. Defaults to False.
        """
        self.__callback: Callable = self.is_callable(callback)
        self.__args = tuple(args or [])
        self.__repeat = repeat

        self.__thread_started = False
        self.__thread_terminate = False

        self.__thread = threading.Thread(
            target=self.__run, daemon=daemon
        )

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

    def has_started(self) -> bool:
        """
        Checks if the thread has started.

        Returns:

            bool: True if thread has started, otherwise False.
        """
        return self.__thread_started

    def is_alive(self) -> bool:
        """
        Checks if the thread is alive.

        Returns:

            bool: True if thread is alive, otherwise False.
        """
        return self.__thread.is_alive()

    def is_terminated(self) -> bool:
        """
        Checks if the thread has terminated.

        Returns:

            bool: True if thread HAS started and is NOT alive, otherwise False.
        """
        return self.has_started() and not self.is_alive()

    def is_repeatable(self) -> bool:
        """Returns True if thread executes callback repeatedly (until .stop() is called)"""
        return self.__repeat

    def is_daemon(self) -> bool:
        """Return whether this thread is a daemon."""
        return self.__thread.daemon

    def set_daemon(self, daemon: bool):
        self.__thread.daemon = daemon

    def join(self, timeout: float | None = None):
        """
        Joins the thread, waiting for it to finish.

        Args:

            timeout (float, optional): The maximum time to wait for the thread to finish. Defaults to None.

        Raises:

            RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        self.__thread.join(timeout)

    def start(self):
        """
        Starts the thread.

        This method begins the execution of the thread by calling the __run method in the background.

        Raises:

            RuntimeError: if start() is called more than once on the same thread object.
        """
        self.__thread.start()
        self.__thread_started = True

    def stop(self):
        """Stops the thread"""
        self.__thread_terminate = True
