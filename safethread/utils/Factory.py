
from typing import Self


class Factory:
    """Factory class, to control subclass creation using create() method."""

    @classmethod
    def create(cls, *args) -> Self:
        """Creates an instance of Self class"""
        return cls(*args)
