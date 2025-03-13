
import os

from safethread.thread.utils import FileHandler

# Assume AsyncFileHandler is already imported

# File where data will be written and read
filename = "example.log"


def on_read(data, e):
    if e:
        print(f"Error: {e}")
        raise e
    # Process the lines read from the file
    print(f"{data}")


# Initialize the AsyncFileHandler with default settings (text mode and max read queue size of 100)
file_handler = FileHandler(
    filename,
    on_read=on_read
)

# Example of writing data to the file using the `put` method
data_to_write = [
    "First line of text\n",
    "Second line of text\n",
    "Third line of text\n"
]

# Put data into the write queue
print(f"Putting data to write ...")
for data in data_to_write:
    print(data)
    file_handler.put(data)


# Start the writer thread
print(f"Writing data into file '{filename}' ...")
file_handler.start_write()
file_handler.join_write()  # Wait for the write thread to finish

# Now that data is written, we will read it
print(f"Reading data from file '{filename}' ...")
file_handler.start_read()
file_handler.join_read()  # Wait for the read thread to finish

# Clean up the file
if os.path.exists(filename):
    os.remove(filename)
