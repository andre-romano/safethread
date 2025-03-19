

from typing import Protocol, Self


from safethread.AbstractContext import AbstractContext


class AbstractLock(AbstractContext, Protocol):
    """
    Abstract base class that defines the interface for lock objects.

    It inherits from AbstractContext ( defines __enter__() and __exit__() methods ) and 
    provides two methods that must be implemented by subclasses: acquire() and release().
    """

    def acquire(self, blocking=True, timeout: float = -1) -> bool:
        """
        Acquires the lock
        """
        ...

    def release(self):
        """
        Releases the lock

        :raises NotImplementedError: if method is not overloaded
        """
        ...
