

from typing import Protocol, Self


class AbstractContext(Protocol):
    """
    Abstract base class for context managers.

    This class defines the interface for context managers by providing
    abstract methods for entering and exiting the context. Subclasses
    must override these methods to implement specific context management
    behavior.
    """

    def __enter__(self) -> Self:
        """
        Enter context-manager
        """
        ...

    def __exit__(self, *args):
        """
        Exits context-manager
        """
        ...
