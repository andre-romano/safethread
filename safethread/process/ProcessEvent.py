import multiprocessing

from .. import BaseEvent


class ProcessEvent(BaseEvent):
    """
    A process-safe class to handle events using multiprocessing.

    This class provides an event object that can be used to synchronize processes.
    """

    def __init__(self) -> None:
        """
        Initializes the ProcessEvent instance.

        The event is initially unset.
        """
        super().__init__(multiprocessing.Event())
