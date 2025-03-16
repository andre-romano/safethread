

from typing import Any, Self

from . import AbstractContext


class AbstractLock(AbstractContext):
    """
    Abstract base class that defines the interface for lock objects.

    It inherits from AbstractContext ( defines __enter__() and __exit__() methods ) and 
    provides two methods that must be implemented by subclasses: acquire() and release().
    """

    def acquire(self) -> bool:
        """
        Acquires the lock

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method NOT overloaded")

    def release(self):
        """
        Releases the lock

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method NOT overloaded")
