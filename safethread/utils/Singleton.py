
from threading import RLock
from typing import Type, Self


class Singleton:
    """Singleton class, to allow only ONE instance of a given subclass."""

    _instances = {}
    _lock = RLock()

    @classmethod
    def getInstance(cls: Type[Self], *args, **kwargs) -> Self:
        """Main method to get the instance of the class."""
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = cls(*args, **kwargs)
            return cls._instances[cls]
