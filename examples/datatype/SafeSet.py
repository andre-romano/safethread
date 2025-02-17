# Assuming SafeSet is correctly imported
from safethread.datatype import SafeSet

# Initialize an empty SafeSet
safe_set = SafeSet()

# Add elements to the set
safe_set.add(1)
safe_set.add(2)
safe_set.add(3)

# Check the current state of the set
print(f"SafeSet contains: {safe_set._data}")  # Output: {1, 2, 3}

# Perform set operations (example: union)
another_set = SafeSet([2, 3, 4, 5])
result = safe_set.union(another_set)
print(f"Union of sets: {result}")  # Output: {1, 2, 3, 4, 5}

# Remove an element from the set
safe_set.remove(2)
print(f"SafeSet after removing 2: {safe_set._data}")  # Output: {1, 3}

# Discard an element (no error if the element is not present)
safe_set.discard(10)  # Does nothing since 10 is not in the set

# Clear the set
safe_set.clear()
print(f"SafeSet after clearing: {safe_set._data}")  # Output: set()
