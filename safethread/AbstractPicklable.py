from typing import Protocol, Tuple, Type, Any, Self


class AbstractPicklable(Protocol):
    """
    A protocol defining the interface for objects that support pickling.

    Classes implementing this protocol must provide a `__reduce__` method
    to customize their serialization behavior when pickled.
    """

    def __reduce__(self) -> Tuple[Type[Self], Tuple[Any, ...]]:
        """
        Customize the pickling behavior of the object.

        This method should return a tuple containing:
        - The class of the object.
        - A tuple of arguments to pass to the class constructor for unpickling.

        :return: A tuple containing the class and its constructor arguments.
        :rtype: Tuple[Type[Self], Tuple[Any, ...]]

        :raises NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError(
            "Method `__reduce__` must be implemented by subclasses")
