
from typing import Any, List, Callable


class Subscriber:
    """
    A class that subscribes to a Publisher and receives notifications when data changes.

    Args:
        callback (Callable[[Any], None]): A function that will be called whenever new data is published.

    Raises:
        TypeError: if callback is not a Callable class (lambda, function, etc)
    """

    def __init__(self, callback: Callable[[Any], None]):
        if not callable(callback):
            raise TypeError("Subscriber callback must be a callable function.")
        self.__callback = callback

    def _notify(self, data: Any):
        """
        Called when new data is published.

        Args:
            data (Any): The updated data from the publisher.
        """
        self.__callback(data)
