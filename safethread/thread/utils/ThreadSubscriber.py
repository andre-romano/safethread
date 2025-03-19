from typing import Any, Callable


class ThreadSubscriber:
    """
    A class that subscribes to a Publisher and receives notifications when data changes.

    This class allows a subscriber to register a callback function that is called whenever
    new data is published by a Publisher.

    :param callback: A function that will be called whenever new data is published.
    :type callback: Callable[[Any], None]

    :raises TypeError: If the `callback` argument is not a callable function or object.
    """

    def __init__(self, callback: Callable[[Any], None]):
        """
        Initializes the Subscriber with the provided callback function.

        :param callback: The function to be called when new data is published.
        :type callback: Callable[[Any], None]

        :raises TypeError: If `callback` is not callable.
        """
        super().__init__()

        self.__callback: Callable[[Any], None] = lambda input: None
        if not callable(callback):
            raise TypeError("`callback` argument is not a callable")
        self.__callback = callback

    def _notify(self, data: Any):
        """
        Called when new data is published.

        This method triggers the callback function provided during initialization with
        the new data.

        :param data: The updated data from the publisher.
        :type data: Any
        """
        self.__callback(data)
