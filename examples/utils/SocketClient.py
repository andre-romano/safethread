import queue
import sys
from typing import Any

from safethread.utils import SocketClient


def on_connect(return_code: int, e: Exception | None):
    if return_code == 0:
        print("Client connected to the server.")
    else:
        print(f"ERROR: Failed to connect - {e.__repr__()}.")


def on_disconnect(return_code: int, e: Exception | None):
    if return_code == 0:
        print("Client disconnected from server.")
    else:
        print(f"ERROR: Disconnected with error - {e.__repr__()}.")


def on_receive(message: Any, e: Exception | None):
    if e is not None:
        print(f"Message received: {message}")
    else:
        print(f"ERROR: Message receive error - {e.__repr__()}.")


# Create a SocketClient instance
client = SocketClient(
    host="127.0.0.1",  # Server IP address
    port=12345,        # Server port
    on_connect=on_connect,
    on_disconnect=on_disconnect,
    on_receive=on_receive,
)

# Connect to the server
try:
    client.connect()
except RuntimeError as e:
    print(f"Failed to connect: {e.__repr__()}")
    sys.exit(1)

# Send messages to the server
try:
    client.send("Hello, Server!")
    client.send("How are you?")
except (queue.ShutDown, queue.Full) as e:
    print(f"Client failed to send message: {e.__repr__()}")

# Keep the client running to receive responses
try:
    while True:
        pass
except KeyboardInterrupt:
    # Disconnect the client on keyboard interrupt
    client.disconnect()
    print("Client disconnected.")
