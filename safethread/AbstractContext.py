

from typing import Any, Protocol


class AbstractContext(Protocol):
    def __enter__(self) -> Any:
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
