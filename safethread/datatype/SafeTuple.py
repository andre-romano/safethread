
from typing import Iterable

from .SafeBaseObj import SafeBaseObj


class SafeTuple(tuple, SafeBaseObj):
    def __init__(self, data: tuple | Iterable | None = None):
        """Initialize a shared tuple with a Lock for thread safety."""
        data = data if isinstance(data, tuple) else tuple(data or [])
        super().__init__(data)
