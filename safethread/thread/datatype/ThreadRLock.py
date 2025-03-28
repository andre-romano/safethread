

import threading
import _thread

from typing import Self

from safethread.AbstractLock import AbstractLock


class ThreadRLock(AbstractLock):
    """
    A re-entrant lock for thread synchronization.

    This class provides a reentrant lock mechanism, allowing the same thread to 
    acquire the lock multiple times without causing a deadlock. 

    It is designed to  be used as a context manager with the 'with' statement.
    """

    def __init__(self, lock: _thread.RLock | None = None) -> None:
        """
        Initializes the ThreadRLock object.

        :param lock: An existing threading.RLock to use with this object
        :type lock: threading.RLock, optional
        """
        super().__init__()

        if not lock:
            lock = threading.RLock()
        self.__lock: _thread.RLock = lock

    def __enter__(self) -> Self:  # type: ignore
        """
        Acquire the lock.

        This method is called when entering a context managed by the lock.
        It will attempt to acquire the lock, with behavior depending on the
        state of the lock and the `blocking` parameter.
        - If `blocking` is False and another thread holds the lock, the method
          will return immediately with a value of False.
        - If `blocking` is True and another thread holds the lock, the method
          will wait until the lock is available, acquire it, and then return True.
          Note that this blocking operation is interruptable.
        - If the current thread already holds the lock, the internal counter is
          incremented, and the method returns True immediately.
        - If no thread holds the lock, the lock is acquired, the internal counter
          is initialized to 1, and the method returns True immediately.

        :raises RuntimeError: if lock cannot be acquired

        :return: This lock object
        :rtype: Self
        """
        if not self.__lock.__enter__():
            raise RuntimeError("Cannot acquire ThreadRLock")
        return self

    def __exit__(self, *args):  # type: ignore
        """
        Exit the runtime context related to this object.

        This method is called when the 'with' statement is completed. It will
        release the lock acquired by the context manager.

        :param args: Optional exception type, value, and traceback information.
                     - args[0]: Exception type (if any)
                     - args[1]: Exception value (if any)
                     - args[2]: Exception traceback (if any)
        """
        t = args[0] if len(args) >= 1 else None
        v = args[1] if len(args) >= 2 else None
        tb = args[2] if len(args) >= 3 else None
        self.__lock.__exit__(t, v, tb)

    def acquire(self, blocking=True, timeout: float = -1) -> bool:
        """
        Acquire the lock.

        This method is called when entering a context managed by the lock.
        It will attempt to acquire the lock, with behavior depending on the
        state of the lock and the `blocking` parameter.
        - If `blocking` is False and another thread holds the lock, the method
          will return immediately with a value of False.
        - If `blocking` is True and another thread holds the lock, the method
          will wait until the lock is available, acquire it, and then return True.
          Note that this blocking operation is interruptable.
        - If the current thread already holds the lock, the internal counter is
          incremented, and the method returns True immediately.
        - If no thread holds the lock, the lock is acquired, the internal counter
          is initialized to 1, and the method returns True immediately.

        :return: True if lock acquired successfully, False otherwise.
        :rtype: bool
        """
        return self.__lock.acquire(blocking=blocking, timeout=timeout)

    def release(self):
        """
        Release the lock.

        This method releases the lock held by the current thread. If the lock 
        cannot be released, a RuntimeError is raised.

        :raises RuntimeError: If the lock cannot be released.
        """

        try:
            self.__lock.release()
        except Exception as e:
            raise RuntimeError(f"Failed to release the lock: {e}")
