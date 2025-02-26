from typing import Any, Callable, Iterable, Self

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

    def subscribe(self, subscribers: Subscriber | Iterable[Subscriber]) -> Self:
        """
        Adds a subscriber(s) to receive notifications when new data is published.

        :param subscribers: The subscriber(s) instance(s) to be added.
        :type subscribers: Subscriber | Iterable[Subscriber]

        :raises TypeError: If the subscribers is not an instance of the Subscriber
            class or contains an Iterable[Subscriber].

        :return: current object
        """
        if isinstance(subscribers, Subscriber):
            subscribers = [subscribers]
        if isinstance(subscribers, Iterable):
            for subscriber in subscribers:
                self.__subscribers.append(subscriber)
            return self
        raise TypeError(
            "Expected an instance of Subscriber or Iterable[Subscriber].")

    def unsubscribe(self, subscriber: Subscriber):
        """
        Removes a subscriber from the list of subscribers, preventing further notifications.

        :param subscriber: The subscriber instance to be removed.
        :type subscriber: Subscriber

        :return: current object
        """
        self.__subscribers.remove(subscriber)
        return self

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
