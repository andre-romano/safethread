import logging

from typing import Self

# Configuração do logger
logger = logging.getLogger(__name__)


class Factory:

    @classmethod
    def create(cls, *args) -> Self:
        """Método de fábrica para criar uma instância da subclasse."""
        return cls(*args)
