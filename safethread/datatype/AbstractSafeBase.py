
from typing import Any, Callable, Self

from .. import AbstractLock


class AbstractSafeBase:
    """
    A safe wrapper around a data object, ensuring safe access
    in multithreaded / multiprocessing environments using locking mechanisms.
    """

    @classmethod
    def create(cls, *args) -> Self:
        """
        Create an instance of the class.

        :param args: Arguments to initialize the instance.
        :return: A new instance of `SafeBaseObj`.
        """
        return cls(*args)

    def __index__(self):
        """
        Return the integer representation of the object, ensuring thread safety.

        :return: Integer representation of the object.
        :rtype: int
        """
        with self._lock:
            return self._data.__index__()

    def __ceil__(self):
        """
        Return the smallest integer greater than or equal to the object.

        :return: The smallest integer greater than or equal to the object.
        :rtype: int
        """
        with self._lock:
            return self._data.__ceil__()

    def __floor__(self):
        """
        Return the largest integer less than or equal to the object.

        :return: The largest integer less than or equal to the object.
        :rtype: int
        """
        with self._lock:
            return self._data.__floor__()

    def __trunc__(self):
        """
        Return the truncated integer value of the object.

        :return: The truncated integer value.
        :rtype: int
        """
        with self._lock:
            return self._data.__trunc__()

    def __round__(self, n=0):
        """
        Round the object to a given number of decimal places.

        :param int n: The number of decimal places to round to (default is 0).
        :return: The rounded value of the object.
        :rtype: float
        """
        with self._lock:
            return self._data.__round__(n)

    def __divmod__(self, other):
        """
        Perform a safe divmod operation with another object.

        :param other: The divisor.
        :type other: SafeBaseObj or compatible type
        :return: A tuple containing the quotient and remainder.
        :rtype: tuple
        """
        other = self.create(other)
        with self._lock, other._lock:
            return divmod(self._data, other._data)

    def __iadd__(self, other):
        """
        Perform an in-place addition operation safely.

        :param other: Another `SafeBaseObj` to add.
        :return: The modified `SafeBaseObj`.
        """
        other = self.create(other)
        with self._lock, other._lock:
            self._data += other._data
            return self

    def __add__(self, other):
        """
        Perform an addition operation safely and return a new instance.

        :param other: Another `SafeBaseObj` to add.
        :return: A new `SafeBaseObj` containing the sum of the two objects.
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data + other._data)

    def __sub__(self, other):
        """
        Perform a subtraction operation safely and return a new instance.

        :param other: The value to subtract.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the subtraction.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data - other._data)

    def __mul__(self, other):
        """
        Perform a multiplication operation safely and return a new instance.

        :param other: The value to multiply by.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the multiplication.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data * other._data)

    def __truediv__(self, other):
        """
        Perform a true division operation safely and return a new instance.

        :param other: The divisor.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the division.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data / other._data)

    def __floordiv__(self, other):
        """
        Perform a floor division operation safely and return a new instance.

        :param other: The divisor.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the floor division.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data // other._data)

    def __mod__(self, other):
        """
        Perform a modulo operation safely and return a new instance.

        :param other: The divisor for the modulo operation.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the remainder of the division.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data % other._data)

    def __pow__(self, other):
        """
        Perform an exponentiation operation safely and return a new instance.

        :param other: The exponent.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of exponentiation.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data ** other._data)

    def __lshift__(self, other):
        """
        Perform a left shift operation safely and return a new instance.

        :param other: The number of positions to shift.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the left-shifted value.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data << other._data)

    def __rshift__(self, other):
        """
        Perform a right shift operation safely and return a new instance.

        :param other: The number of positions to shift.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the right-shifted value.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data >> other._data)

    def __and__(self, other):
        """
        Perform a bitwise AND operation safely and return a new instance.

        :param other: The value to perform the AND operation with.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the AND operation.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data & other._data)

    def __or__(self, other):
        """
        Perform a bitwise OR operation safely and return a new instance.

        :param other: The value to perform the OR operation with.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the OR operation.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data | other._data)

    def __xor__(self, other):
        """
        Perform a bitwise XOR operation safely and return a new instance.

        :param other: The value to perform the XOR operation with.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the XOR operation.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self.create(self._data ^ other._data)

    def __radd__(self, other):
        """
        Perform a reflected addition operation safely.

        :param other: The value to add.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the addition.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__add__(self)

    def __rsub__(self, other):
        """
        Perform a reflected subtraction operation safely.

        :param other: The value to subtract from.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the subtraction.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__sub__(self)

    def __rmul__(self, other):
        """
        Perform a reflected multiplication operation safely.

        :param other: The value to multiply with.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the multiplication.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__mul__(self)

    def __rtruediv__(self, other):
        """
        Perform a reflected true division operation safely.

        :param other: The dividend.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the division.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__truediv__(self)

    def __rfloordiv__(self, other):
        """
        Perform a reflected floor division operation safely.

        :param other: The dividend.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the floor division.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__floordiv__(self)

    def __rmod__(self, other):
        """
        Perform a reflected modulo operation safely.

        :param other: The dividend for the modulo operation.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the remainder.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__mod__(self)

    def __rpow__(self, other):
        """
        Perform a reflected exponentiation operation safely.

        :param other: The base value.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of exponentiation.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__pow__(self)

    def __rlshift__(self, other):
        """
        Perform a reflected left shift operation safely.

        :param other: The value to be shifted.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the left-shifted value.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__lshift__(self)

    def __rrshift__(self, other):
        """
        Perform a reflected right shift operation safely.

        :param other: The value to be shifted.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the right-shifted value.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__rshift__(self)

    def __rand__(self, other):
        """
        Perform a reflected bitwise AND operation safely.

        :param other: The value to perform the AND operation with.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the AND operation.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__and__(self)

    def __ror__(self, other):
        """
        Perform a reflected bitwise OR operation safely.

        :param other: The value to perform the OR operation with.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the OR operation.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__or__(self)

    def __rxor__(self, other):
        """
        Perform a reflected bitwise XOR operation safely.

        :param other: The value to perform the XOR operation with.
        :type other: SafeBaseObj or compatible type
        :return: A new instance representing the result of the XOR operation.
        :rtype: SafeBaseObj
        """
        other = self.create(other)
        return other.__xor__(self)

    def __abs__(self):
        """
        Return the absolute value of the object safely.

        This method ensures thread safety while computing the absolute value.

        :return: A new instance representing the absolute value.
        :rtype: SafeBaseObj
        """
        with self._lock:
            return self.create(abs(self._data))

    def __neg__(self):
        """
        Return the negation of the object safely.

        This method ensures thread safety while computing the negation.

        :return: A new instance representing the negated value.
        :rtype: SafeBaseObj
        """
        with self._lock:
            return self.create(-self._data)

    def __pos__(self):
        """
        Return the positive value of the object safely.

        This method ensures thread safety while computing the positive representation.

        :return: A new instance representing the positive value.
        :rtype: SafeBaseObj
        """
        with self._lock:
            return self.create(+self._data)

    def __invert__(self):
        """
        Return the bitwise inversion of the object safely.

        This method ensures thread safety while computing the bitwise inversion.

        :return: A new instance representing the bitwise-inverted value.
        :rtype: SafeBaseObj
        """
        with self._lock:
            return self.create(~self._data)

    def __ne__(self, other) -> bool:
        """
        Check inequality between two objects safely.

        :param other: The object to compare with.
        :type other: SafeBaseObj or compatible type
        :return: True if the objects are not equal, False otherwise.
        :rtype: bool
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self._data != other._data

    def __eq__(self, other) -> bool:
        """
        Check if two `SafeBaseObj` instances are equal safely.

        :param other: Another `SafeBaseObj` to compare.
        :return: `True` if equal, otherwise `False`.
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self._data == other._data

    def __lt__(self, other):
        """
        Check if the object is less than another safely.

        :param other: The object to compare with.
        :type other: `type of other`
        :return: `True` if the object is less than the other object, otherwise `False`.
        :rtype: bool
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self._data < other._data

    def __le__(self, other):
        """
        Check if the object is less than or equal to another safely.

        :param other: The object to compare with.
        :type other: `type of other`
        :return: `True` if the object is less than or equal to the other object, otherwise `False`.
        :rtype: bool
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self._data <= other._data

    def __gt__(self, other):
        """
        Check if the object is greater than another safely.

        :param other: The object to compare with.
        :type other: `type of other`
        :return: `True` if the object is greater than the other object, otherwise `False`.
        :rtype: bool
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self._data > other._data

    def __ge__(self, other):
        """
        Check if the object is greater than or equal to another safely.

        :param other: The object to compare with.
        :type other: `type of other`
        :return: `True` if the object is greater than or equal to the other object, otherwise `False`.
        :rtype: bool
        """
        other = self.create(other)
        with self._lock, other._lock:
            return self._data >= other._data

    def __getitem__(self, index):
        """
        Retrieve an item safely from the object.

        :param index: The index of the item to retrieve.
        :return: The item at the given index.
        """
        with self._lock:
            return self._data[index]

    def __setitem__(self, index, value):
        """
        Set a value at a specific index safely.

        :param index: The index where the value should be set.
        :param value: The value to assign.
        """
        with self._lock:
            self._data[index] = value

    def __delitem__(self, index):
        """
        Remove an item by index safely.

        :param index: The index of the item to remove.
        :type index: int
        :raises IndexError: If the index is out of range.
        """
        with self._lock:
            del self._data[index]

    def __contains__(self, value):
        """
        Check if a value exists in the object safely.

        :param value: The value to check for presence in the object.
        :type value: `type of value`
        :return: `True` if the value exists in the object, otherwise `False`.
        :rtype: bool
        """
        with self._lock:
            return value in self._data

    def __sizeof__(self):
        """
        Return the size of the object in bytes, including lock overhead.

        :return: The size of the object in bytes.
        :rtype: int
        """
        with self._lock:
            return self._data.__sizeof__() + self._lock.__sizeof__()

    def __len__(self):
        """
        Return the length of the object safely.

        :return: The length of the internal data.
        """
        with self._lock:
            return len(self._data)

    def __iter__(self):
        """
        Return a thread-safe iterator for the object.

        :return: An iterator for the object's data.
        :rtype: iterator
        """
        with self._lock:
            return iter(self._data)

    def __hash__(self):
        """
        Return the hash of the object safely.

        :return: The hash value of the object's data.
        :rtype: int
        """
        with self._lock:
            return hash(self._data)

    def __repr__(self):
        """
        Return a string representation of the object safely.

        :return: A string representation of the object.
        """
        with self._lock:
            return repr(self._data)

    def __str__(self):
        """
        Return a string conversion of the object safely.

        :return: A string representation of the object.
        """
        with self._lock:
            return str(self._data)

    def __bool__(self):
        """
        Return the boolean representation of the object safely.

        :return: `True` if the object is truthy, otherwise `False`.
        """
        with self._lock:
            return bool(self._data)

    def __int__(self):
        """
        Return the integer representation of the object safely.

        :return: The integer representation of the object's data.
        :rtype: int
        """
        with self._lock:
            return int(self._data)

    def __float__(self):
        """
        Return the float representation of the object safely.

        :return: The float representation of the object's data.
        :rtype: float
        """
        with self._lock:
            return float(self._data)

    def __init__(self, data: Any):
        """
        Initialize a safe object with an internal lock.

        :param data: The initial data to be wrapped in a safe manner.
        """
        super().__init__()  # Ensure parent class initialization

        if isinstance(data, AbstractSafeBase):
            self._data = data._data
        else:
            self._data = self._create_data(data)

        if isinstance(data, AbstractSafeBase):
            self._lock = data._lock
        else:
            self._lock = self._create_lock()

    def _create_data(self, data: Any | None) -> Any:
        """
        Create a data instance.

        This method should be overridden by subclasses to provide a specific
        implementation of a lock.

        :raises NotImplementedError: If the method is not overridden by a subclass.

        :return: An instance of data.
        """

        raise NotImplementedError("Method NOT overloaded")

    def _create_lock(self) -> AbstractLock:
        """
        Create a lock instance.

        This method should be overridden by subclasses to provide a specific
        implementation of a lock.

        :raises NotImplementedError: If the method is not overridden by a subclass.

        :return: An instance of a lock.
        :rtype: AbstractLock
        """

        raise NotImplementedError("Method NOT overloaded")

    def get_lock(self) -> AbstractLock:
        """
        Retrieve the lock associated with this object.

        :return: The lock object.
        :rtype: AbstractLock
        """
        return self._lock

    def execute(self, callback: Callable[[], Any]):
        """
        Run a callback function in a thread-safe manner.

        :param callback: The function to execute safely.
        :type callback: Callable[[],Any]
        """
        with self._lock:
            callback()

    def copy(self):
        """
        Return a thread-safe copy of the object.

        :return: A new instance of `SafeBaseObj` containing a copy of the data.

        :raises AttributeError: if self._data.copy() does not exist
        """
        with self._lock:
            return self.create(self._data.copy())

    def copyObj(self):
        """
        Return an internal data copy.

        :return: A copy of the internal data

        :raises AttributeError: if self._data.copy() does not exist
        """
        with self._lock:
            return self._data.copy()
