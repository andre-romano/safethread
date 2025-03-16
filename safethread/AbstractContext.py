

from typing import Any, Protocol


class AbstractContext(Protocol):
    """
    Abstract base class for context managers.

    This class defines the interface for context managers by providing
    abstract methods for entering and exiting the context. Subclasses
    must override these methods to implement specific context management
    behavior.
    """

    def __enter__(self, blocking: bool = True, timeout: float = -1) -> Any:
        """
        Enter context-manager

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method NOT overloaded")

    def __exit__(self, *args):
        """
        Exits context-manager

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method NOT overloaded")
