# Assuming SafeTuple is correctly imported
from safethread.datatype import SafeTuple

# Initialize a SafeTuple with a tuple
safe_tuple = SafeTuple((1, 2, 3))

# Print the contents of the SafeTuple
print(f"SafeTuple contains: {safe_tuple}")  # Output: (1, 2, 3)

# You can iterate over the tuple just like a regular tuple
for item in safe_tuple:
    print(f"Item: {item}")

# You can also access specific elements by index
print(f"First element: {safe_tuple[0]}")  # Output: 1
