

from typing import Any, Protocol, Self


class AbstractEvent(Protocol):
    def is_set(self) -> bool:
        """
        Checks if event is set

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method NOT overloaded")

    def set(self):
        """
        Sets event

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method NOT overloaded")
