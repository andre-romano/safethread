
from typing import Any, Callable

from ..datatype import SafeSet

from .Subscriber import Subscriber


class Publisher:
    """
    A thread-safe class that maintains a list of Subscriber instances and notifies them when data changes.    
    """

    def __init__(self):
        self.__subscribers = SafeSet()
        self.__data: Any = None

    def subscribe(self, subscriber: Subscriber):
        """
        Adds a subscriber to receive notifications.

        Args:
            subscriber (Subscriber): The subscriber instance.

        Raises:
            TypeError: if subscriber is not an instance of Subscriber class
        """
        if not isinstance(subscriber, Subscriber):
            raise TypeError("Expected an instance of Subscriber.")
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber: Subscriber):
        """
        Removes a subscriber from notifications.

        Args:
            subscriber (Subscriber): The subscriber instance.
        """
        self.__subscribers.remove(subscriber)

    def publish(self, data: Any):
        """
        Publishes new data and notifies all subscribers.

        Args:
            data (Any): The new data to be published.
        """
        self.__data = data
        # notify subscribers
        for subscriber in self.__subscribers:
            subscriber: Subscriber
            subscriber._notify(self.__data)
