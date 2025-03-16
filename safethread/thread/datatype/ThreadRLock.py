

from threading import RLock
from typing import Any

from safethread import AbstractLock


class ThreadRLock(AbstractLock):
    def __init__(self) -> None:
        super().__init__()
        self.__lock = RLock()

    def __enter__(self, blocking: bool = True, timeout: float = -1) -> Any:
        """
        Lock the lock. blocking indicates whether we should wait
        for the lock to be available or not. If blocking is False
        and another thread holds the lock, the method will return False
        immediately. If blocking is True and another thread holds
        the lock, the method will wait for the lock to be released,
        take it and then return True.
        (note: the blocking operation is interruptible.)

        In all other cases, the method will return True immediately.
        Precisely, if the current thread already holds the lock, its
        internal counter is simply incremented. If nobody holds the lock,
        the lock is taken and its internal counter initialized to 1.
        """
        return self.__lock.__enter__(blocking=blocking, timeout=timeout)

    def __exit__(self, *args):
        """Release the lock."""
        t = args[0] if len(args) >= 1 else None
        v = args[1] if len(args) >= 2 else None
        tb = args[2] if len(args) >= 3 else None
        return self.__lock.__exit__(t, v, tb)

    def acquire(self, blocking=True, timeout: float = -1) -> bool:
        """
        Lock the lock. blocking indicates whether we should wait
        for the lock to be available or not. If blocking is False
        and another thread holds the lock, the method will return False
        immediately. If blocking is True and another thread holds
        the lock, the method will wait for the lock to be released,
        take it and then return True.
        (note: the blocking operation is interruptible.)

        In all other cases, the method will return True immediately.
        Precisely, if the current thread already holds the lock, its
        internal counter is simply incremented. If nobody holds the lock,
        the lock is taken and its internal counter initialized to 1.
        """
        return self.__lock.acquire(blocking=blocking, timeout=timeout)

    def release(self):
        """
        Release the lock, allowing another thread that is blocked waiting for
        the lock to acquire the lock. The lock must be in the locked state,
        and must be locked by the same thread that unlocks it; otherwise a
        RuntimeError is raised.

        Do note that if the lock was acquire()d several times in a row by the
        current thread, release() needs to be called as many times for the lock
        to be available for other threads.
        """
        self.__lock.release()
