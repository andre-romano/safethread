
from .SafeBaseObj import SafeBaseObj


class SafeList(SafeBaseObj):
    def __init__(self, listObj: list | None = None):
        """Inicializa uma lista compartilhada com bloqueio para segurança em threads."""
        super().__init__(listObj or [])
        self._data: list

    def append(self, value):
        """Adiciona um item à lista de maneira segura."""
        with self._lock:
            self._data.append(value)

    def clear(self):
        """Esvazia a lista de maneira segura."""
        with self._lock:
            self._data.clear()

    def count(self, value):
        """Conta o número de ocorrências de um item na lista."""
        with self._lock:
            return self._data.count(value)

    def extend(self, values):
        """Adiciona múltiplos itens à lista de maneira segura."""
        with self._lock:
            self._data.extend(values)

    def index(self, value, start=0, end=None):
        """Retorna o índice do primeiro item correspondente de maneira segura."""
        with self._lock:
            return self._data.index(value, start, end if end is not None else len(self._data))

    def insert(self, index, value):
        """Insere um item na posição especificada de maneira segura."""
        with self._lock:
            self._data.insert(index, value)

    def pop(self, index=-1):
        """Remove e retorna um item da lista de maneira segura."""
        with self._lock:
            return self._data.pop(index)

    def remove(self, value):
        """Remove um item da lista de maneira segura."""
        with self._lock:
            self._data.remove(value)

    def reverse(self):
        """Inverte a ordem da lista de maneira segura."""
        with self._lock:
            self._data.reverse()

    def sort(self, **kwargs):
        """Ordena a lista de maneira segura."""
        with self._lock:
            self._data.sort(**kwargs)
