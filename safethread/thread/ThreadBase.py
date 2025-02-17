import threading


class ThreadBase:
    """
    A base class for managing threads with thread safety.

    This class provides a structure for creating and managing threads using the threading module.
    It also ensures that the thread's operations are protected by a reentrant lock (_lock) to ensure thread safety.
    """

    def __init__(self, args: list, daemon: bool = True):
        """
        Initializes the thread and the reentrant lock.

        Args:

            args (list): The arguments to pass to the _run method when the thread starts.

            daemon (bool, optional): If True, the thread will be daemonized. Defaults to True.
        """
        self._lock = threading.RLock()
        self._thread_started = False
        self._thread = threading.Thread(
            target=self._run, args=args, daemon=daemon
        )

    def _run(self, *args):
        """
        Abstract method to be implemented by subclasses.

        This method should be overloaded in subclasses to define the work the thread will perform.

        Raises:

            Exception: If the method is not overloaded by a subclass.
        """
        raise Exception(f"_run() method NOT overloaded!")

    def has_started(self) -> bool:
        """
        Checks if the thread has started.

        Returns:

            bool: True if thread has started, otherwise False.
        """
        return self._thread_started

    def is_alive(self) -> bool:
        """
        Checks if the thread is alive.

        Returns:

            bool: True if thread is alive, otherwise False.
        """
        return self._thread.is_alive()

    def is_terminated(self) -> bool:
        """
        Checks if the thread has terminated.

        Returns:

            bool: True if thread HAS started and is NOT alive, otherwise False.
        """
        return self.has_started() and not self.is_alive()

    def set_daemon(self, daemon: bool):
        self._thread.daemon = daemon

    def is_daemon(self) -> bool:
        """Return whether this thread is a daemon."""
        return self._thread.daemon

    def join(self, timeout: float | None = None):
        """
        Joins the thread, waiting for it to finish.

        Args:

            timeout (float, optional): The maximum time to wait for the thread to finish. Defaults to None.
        """
        self._thread.join(timeout)

    def start(self):
        """
        Starts the thread.

        This method begins the execution of the thread by calling the _run method in the background.

        Raises:

            RuntimeError: if start() is called more than once on the same thread object.
        """
        self._thread.start()
        self._thread_started = True
