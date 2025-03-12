from threading import RLock
from typing import Type, Self


class Singleton:
    """
    Singleton class that ensures only one instance of a subclass exists.

    This class provides a thread-safe mechanism to ensure that only a single instance
    of a subclass is created and shared across the application. The `getInstance` method
    is used to retrieve the single instance.
    """

    _instances = {}
    _lock = RLock()

    @classmethod
    def get_instance(cls: Type[Self], *args, **kwargs) -> Self:
        """
        Retrieves the single instance of the class, creating it if necessary.

        This method ensures that only one instance of the class is created. If an instance
        already exists, it is returned; otherwise, a new instance is created and returned.

        :param *args: Arguments to be passed to the class constructor.
        :param **kwargs: Keyword arguments to be passed to the class constructor.
        :type *args: tuple
        :type **kwargs: dict

        :return: The single instance of the class.
        :rtype: Self
        """
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = cls(*args, **kwargs)
            return cls._instances[cls]
