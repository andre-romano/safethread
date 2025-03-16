# Assuming SafeQueue is correctly imported
from safethread.thread.datatype import ThreadSafeQueue

# Initialize a SafeQueue with a maximum size of 3
safe_queue = ThreadSafeQueue(3)

# Put items into the queue
safe_queue.put(1)
safe_queue.put(2)
safe_queue.put(3)

# Try to put another item (this will block if the queue is full)
# Uncomment to test blocking behavior
# safe_queue.put(4)

# Get an item from the queue
item = safe_queue.get()
print(f"Got item from queue: {item}")  # Output: 1

# Check if the queue is empty
is_empty = safe_queue.empty()
print(f"Is the queue empty? {is_empty}")  # Output: False

# Get another item from the queue
item = safe_queue.get()
print(f"Got item from queue: {item}")  # Output: 2

# Put an item again
safe_queue.put(4)

# Get all remaining items
while not safe_queue.empty():
    item = safe_queue.get()
    print(f"Got item from queue: {item}")  # Output: 3, then 4
