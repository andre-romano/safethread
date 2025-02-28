import queue

from safethread.utils import SocketClient

# Create a SocketClient instance
client = SocketClient(
    host="127.0.0.1",  # Server IP address
    port=12345,        # Server port
)


def on_connect():
    print("Client connected to the server.")


# Connect to the server
try:
    client.connect(callback_succ=on_connect)
except RuntimeError as e:
    print(f"Failed to connect: {e.__repr__()}")

# Send messages to the server
try:
    client.send("Hello, Server!")
    client.send("How are you?")
except (queue.ShutDown, queue.Full) as e:
    print(f"Client failed to send message: {e.__repr__()}")

# Keep the client running to receive responses
try:
    while client.is_connected():
        msg = client.receive()
        print("Server reply: {msg}")
except KeyboardInterrupt:
    # Disconnect the client on keyboard interrupt
    client.disconnect()
    print("Client disconnected.")
