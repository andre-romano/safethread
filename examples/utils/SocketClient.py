from safethread.utils import SocketClient


def on_message_received(message: str) -> None:
    """
    Callback function that handles incoming messages from the server.
    """
    print(f"Client: Received message from server: {message}")


def on_receive_error(error: Exception) -> None:
    """
    Callback function that handles errors during message reception.
    """
    print(f"Client: Error receiving message: {error}")


# Create a SocketClient instance
client = SocketClient(
    host="127.0.0.1",  # Server IP address
    port=12345,        # Server port
    on_message_received=on_message_received,
    on_receive_error=on_receive_error,
)

# Connect to the server
try:
    client.connect()
    print("Client connected to the server.")
except RuntimeError as e:
    print(f"Client failed to connect: {e}")
    exit(1)

# Send messages to the server
try:
    client.send_message("Hello, Server!")
    client.send_message("How are you?")
except RuntimeError as e:
    print(f"Client failed to send message: {e}")

# Keep the client running to receive responses
try:
    while client.is_connected():
        pass
except KeyboardInterrupt:
    # Disconnect the client on keyboard interrupt
    client.disconnect()
    print("Client disconnected.")
