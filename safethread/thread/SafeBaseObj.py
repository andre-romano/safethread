import logging

from threading import RLock

from ..utils import Factory

# Configuração do logger
logger = logging.getLogger(__name__)


class SafeBaseObj(Factory):
    """
    A thread-safe wrapper around a data object, ensuring safe access 
    in multithreaded environments using locking mechanisms.
    """

    def __index__(self):
        """Return the integer representation of the object, ensuring thread safety."""
        with self._lock:
            return self._data.__index__()

    def __ceil__(self):
        """Return the smallest integer greater than or equal to the object."""
        with self._lock:
            return self._data.__ceil__()

    def __floor__(self):
        """Return the largest integer less than or equal to the object."""
        with self._lock:
            return self._data.__floor__()

    def __trunc__(self):
        """Return the truncated integer value of the object."""
        with self._lock:
            return self._data.__trunc__()

    def __round__(self, n=0):
        """Round the object to a given number of decimal places."""
        with self._lock:
            return self._data.__round__(n)

    def __divmod__(self, other):
        """Perform a safe divmod operation with another object."""
        other = self.create(other)
        with self._lock, other._lock:
            return divmod(self._data, other._data)

    def __iadd__(self, other):
        """Perform an in-place addition operation safely."""
        other = self.create(other)
        with self._lock, other._lock:
            self._data += other._data
            return self

    def __add__(self, other):
        """Perform an addition operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data + other._data)

    def __sub__(self, other):
        """Perform a subtraction operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data - other._data)

    def __mul__(self, other):
        """Perform a multiplication operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data * other._data)

    def __truediv__(self, other):
        """Perform a true division operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data / other._data)

    def __floordiv__(self, other):
        """Perform a floor division operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data // other._data)

    def __mod__(self, other):
        """Perform a modulo operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data % other._data)

    def __pow__(self, other):
        """Perform an exponentiation operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data ** other._data)

    def __lshift__(self, other):
        """Perform a left shift operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data << other._data)

    def __rshift__(self, other):
        """Perform a left shift operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data >> other._data)

    def __and__(self, other):
        """Return the intersection of two sets safely."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data & other._data)

    def __or__(self, other):
        """Return the union of two sets safely."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data | other._data)

    def __xor__(self, other):
        """Perform a bitwise XOR operation safely and return a new instance."""
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data ^ other._data)

    def __radd__(self, other):
        """Perform a reflected addition operation safely."""
        other = self.create(other)
        return other.__add__(self)

    def __rsub__(self, other):
        """Perform a reflected subtraction operation safely."""
        other = self.create(other)
        return other.__sub__(self)

    def __rmul__(self, other):
        """Perform a reflected multiplication operation safely."""
        other = self.create(other)
        return other.__mul__(self)

    def __rtruediv__(self, other):
        """Perform a reflected true division operation safely."""
        other = self.create(other)
        return other.__truediv__(self)

    def __rfloordiv__(self, other):
        """Perform a reflected floor division operation safely."""
        other = self.create(other)
        return other.__floordiv__(self)

    def __rmod__(self, other):
        """Perform a reflected modulo operation safely."""
        other = self.create(other)
        return other.__mod__(self)

    def __rpow__(self, other):
        """Perform a reflected exponentiation operation safely."""
        other = self.create(other)
        return other.__pow__(self)

    def __rlshift__(self, other):
        """Perform a reflected left shift operation safely."""
        other = self.create(other)
        return other.__lshift__(self)

    def __rrshift__(self, other):
        """Perform a reflected right shift operation safely."""
        other = self.create(other)
        return other.__rshift__(self)

    def __rand__(self, other):
        """Perform a reflected bitwise AND operation safely."""
        other = self.create(other)
        return other.__and__(self)

    def __ror__(self, other):
        """Perform a reflected bitwise OR operation safely."""
        other = self.create(other)
        return other.__or__(self)

    def __rxor__(self, other):
        """Perform a reflected bitwise XOR operation safely."""
        other = self.create(other)
        return other.__xor__(self)

    def __abs__(self):
        """Return the absolute value of the object safely."""
        with self._lock:
            return self.create(abs(self._data))

    def __neg__(self):
        """Return the negation of the object safely."""
        with self._lock:
            return self.create(-self._data)

    def __pos__(self):
        """Return the positive value of the object safely."""
        with self._lock:
            return self.create(+self._data)

    def __invert__(self):
        """Return the bitwise inversion of the object safely."""
        with self._lock:
            return self.create(~self._data)

    def __ne__(self, other) -> bool:
        """Verifica desigualdade entre dois objetos."""
        other = self.create(other)
        with self._lock, other._lock:
            return self._data != other._data

    def __eq__(self, other) -> bool:
        """Check if two sets are equal safely."""
        other = self.create(other)
        with self._lock, other._lock:
            return self._data == other._data

    def __lt__(self, other):
        """Check if the object is less than another safely."""
        other = self.create(other)
        with self._lock, other._lock:
            return self._data < other._data

    def __le__(self, other):
        """Check if the object is less than or equal to another safely."""
        other = self.create(other)
        with self._lock, other._lock:
            return self._data <= other._data

    def __gt__(self, other):
        """Check if the object is greater than another safely."""
        other = self.create(other)
        with self._lock, other._lock:
            return self._data > other._data

    def __ge__(self, other):
        """Check if the object is greater than or equal to another safely."""
        other = self.create(other)
        with self._lock, other._lock:
            return self._data >= other._data

    def __getitem__(self, index):
        """Retrieve an item safely from the object."""
        with self._lock:
            if index not in self._data:
                msg = f"Index '{index}' not found."
                logger.error(msg)
                raise KeyError(msg)
            return self._data[index]

    def __setitem__(self, index, value):
        """Set a value at a specific index safely."""
        with self._lock:
            self._data[index] = value

    def __delitem__(self, index):
        """Remove an item by index safely."""
        with self._lock:
            del self._data[index]

    def __contains__(self, value):
        """Check if a value exists in the object safely."""
        with self._lock:
            return value in self._data

    def __sizeof__(self):
        """Return the size of the object in bytes, including lock overhead."""
        with self._lock:
            return self._data.__sizeof__() + self._lock.__sizeof__()

    def __len__(self):
        """Return the size of the object safely."""
        with self._lock:
            return len(self._data)

    def __iter__(self):
        """Return a thread-safe iterator for the object."""
        with self._lock:
            return iter(self._data.copy())

    def __hash__(self):
        """Return the hash of the object safely."""
        with self._lock:
            return hash(self._data)

    def __repr__(self):
        """Return a string representation of the object safely."""
        with self._lock:
            return repr(self._data)

    def __str__(self):
        """Return a string conversion of the object safely."""
        with self._lock:
            return str(self._data)

    def __bool__(self):
        """Return the boolean representation of the object safely."""
        with self._lock:
            return bool(self._data)

    def __int__(self):
        """Return the integer representation of the object safely."""
        with self._lock:
            return int(self._data)

    def __float__(self):
        """Return the float representation of the object safely."""
        with self._lock:
            return float(self._data)

    def __init__(self, data):
        """
        Initialize a thread-safe object with an internal lock.

        :param data: The initial data to be wrapped in a thread-safe manner.
        """
        super().__init__()  # Ensure parent class initialization
        self._data = data if not isinstance(data, SafeBaseObj) else data._data
        self._lock = RLock() if not isinstance(data, SafeBaseObj) else data._lock

    def copy(self):
        """Return a thread-safe copy of the object."""
        with self._lock:
            return self.create(self._data.copy())

    def copyObj(self):
        """Return an internal data copy."""
        with self._lock:
            return self._data.copy()
