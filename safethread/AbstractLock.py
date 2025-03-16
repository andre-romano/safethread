

from typing import Any, Self

from . import AbstractContext


class AbstractLock(AbstractContext):
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
