

from typing import Protocol


class AbstractProcess(Protocol):
    """Represents a process / thread instance interface"""

    def start(self) -> None:
        """
        Starts the process / thread

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method not OVERLOADED")

    def join(self, timeout: float | None = None) -> None:
        """
        Joins the process / thread

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method not OVERLOADED")

    def is_alive(self) -> bool:
        """
        Checks if the process/thread is alive.

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method not OVERLOADED")

    @property
    def daemon(self):
        """
        Gets process/thread as daemon.

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method not OVERLOADED")

    @daemon.setter
    def daemon(self, d: bool):
        """
        Setter method for 'daemon'

        :raises NotImplementedError: if method is not overloaded
        """
        raise NotImplementedError("Method not OVERLOADED")
