from typing import Any, Callable

from ..datatype import SafeList

from .Subscriber import Subscriber


class Publisher:
    """
    A thread-safe class that maintains a list of Subscriber instances and notifies them when data changes.

    This class allows subscribers to be added or removed from a list, and will notify them whenever
    new data is published. It is designed to be thread-safe.
    """

    def __init__(self):
        """
        Initializes a new Publisher instance.
        """
        self.__subscribers = SafeList()

    def subscribe(self, subscriber: Subscriber):
        """
        Adds a subscriber to receive notifications when new data is published.

        :param subscriber: The subscriber instance to be added.
        :type subscriber: Subscriber

        :raises TypeError: If the subscriber is not an instance of the Subscriber class.
        """
        if not isinstance(subscriber, Subscriber):
            raise TypeError("Expected an instance of Subscriber.")
        self.__subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber):
        """
        Removes a subscriber from the list of subscribers, preventing further notifications.

        :param subscriber: The subscriber instance to be removed.
        :type subscriber: Subscriber
        """
        self.__subscribers.remove(subscriber)

    def publish(self, data: Any):
        """
        Publishes new data and notifies all subscribed listeners.

        :param data: The new data to be published to subscribers.
        :type data: Any
        """
        # Notify all subscribers with the new data
        for subscriber in self.__subscribers:
            subscriber: Subscriber
            subscriber._notify(data)
