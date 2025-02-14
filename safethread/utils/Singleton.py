import logging

from threading import RLock
from typing import Type, Self

# Configuração do logger
logger = logging.getLogger(__name__)


class Singleton:
    """Singleton class, to allow only ONE instance of a given subclass."""

    _instances = {}
    _lock = RLock()

    @classmethod
    def getInstance(cls: Type[Self], *args, **kwargs) -> Self:
        """Main method to get the instance of the class."""
        # This ensures the singleton logic is respected
        with cls._lock:
            logger.debug(f"Getting instance of {cls.__name__}")
            if cls not in cls._instances:
                logger.debug(f"Creating new instance of {cls.__name__}")
                cls._instances[cls] = cls(*args, **kwargs)
            return cls._instances[cls]
