
# EXAMPLE CODE BELOW

from safethread.thread.datatype import SafeDictThread

# Create a SafeDict instance
safe_dict = SafeDictThread()

# Update the dictionary in a thread-safe manner
safe_dict.update({'a': 1, 'b': 2})

# Retrieve a value in a thread-safe manner
print(safe_dict.get('a'))  # Output: 1

# Remove a key in a thread-safe manner
safe_dict.pop('b')

# Final state of the dictionary
print(dict(safe_dict.items()))  # Output: {'a': 1}
