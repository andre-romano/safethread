

from typing import Any, Self


class AbstractPicklable:
    """
    Abstract base class that defines the interface for picklable objects.
    """

    def __reduce__(self) -> tuple[type[Self], tuple]:
        """
        Releases the lock

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method NOT overloaded")
        return (self.__class__, ())
