from typing import Iterable

from .SafeBaseObj import SafeBaseObj


class SafeTuple(tuple, SafeBaseObj):
    def __init__(self, data: tuple | Iterable | None = None):
        """
        Initialize a shared tuple with a Lock for thread safety.

        If a `tuple` is provided, it is used as the initial data.
        If an iterable is provided, it is converted into a tuple.
        If no argument is provided, an empty tuple is used.

        :param data: The initial data to populate the tuple with.
        :type data: tuple, Iterable, or None
        """
        data = data if isinstance(data, tuple) else tuple(data or [])
        super().__init__(data)
