import threading

from .. import BaseEvent


class ThreadEvent(BaseEvent):
    """
    A thread-safe class to handle events using threading.

    This class provides an event object that can be used to synchronize threads.
    It is implemented using `threading.Event` for better performance and reliability.
    """

    def __init__(self) -> None:
        """
        Initializes the ThreadEvent instance.

        The event is initially unset.
        """
        super().__init__(threading.Event())
