
from safethread.utils import FileHandler

# Assume AsyncFileHandler is already imported

# File where data will be written and read
filename = "example.log"

# Initialize the AsyncFileHandler with default settings (text mode and max read queue size of 100)
file_handler = FileHandler(filename)

# Example of writing data to the file using the `put` method
data_to_write = [
    "First line of text\n",
    "Second line of text\n",
    "Third line of text\n"
]

# Put data into the write queue
for data in data_to_write:
    print(f"Putting data to write: '{data[:-1]}'")
    file_handler.put(data)


# Start the writer thread
file_handler.start_write()
file_handler.join_write()  # Wait for the write thread to finish

# Now that data is written, we will read it
file_handler.start_read()
file_handler.join_read()  # Wait for the read thread to finish

# Process the lines read from the file
print("Reading data from the file:")
line = file_handler.get()
# Stop when queue is empty (meaning reading is finished)
while line is not None:
    print(f"Read line: '{line[:-1]}'")
    line = file_handler.get()

# Check the status of the read/write operations
status, error_message = file_handler.get_status()
if status == 0:
    print("File operations completed successfully.")
else:
    print(f"ERROR: {error_message}")
