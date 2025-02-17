# Assuming SafeList is correctly imported
from safethread.datatype import SafeList

# Initialize a SafeList with some data
safe_list = SafeList([1, 2, 3])

# Append an item to the list
safe_list.append(4)

# Extend the list with more items
safe_list.extend([5, 6])

# Print the list after appending and extending
print("List after appending and extending:", list(
    safe_list))  # Output: [1, 2, 3, 4, 5, 6]

# Remove an item from the list
safe_list.remove(2)

# Print the list after removing an item
print("List after removing 2:", list(safe_list))  # Output: [1, 3, 4, 5, 6]

# Count occurrences of a value
count = safe_list.count(3)
print("Count of 3 in the list:", count)  # Output: 1

# Sort the list in descending order
safe_list.sort(reverse=True)
print("List after sorting in descending order:",
      list(safe_list))  # Output: [6, 5, 4, 3, 1]

# Pop an item from the list
popped_item = safe_list.pop()
print("Popped item:", popped_item)  # Output: 1

# Clear the list
safe_list.clear()
print("List after clearing:", list(safe_list))  # Output: []
