

from typing import Any, Protocol, Self


class AbstractEvent(Protocol):
    """
    Abstract base class for event handling.

    This class defines the interface for event objects, which can be set or checked if they are set.
    Subclasses must override the `is_set` and `set` methods.
    """

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
