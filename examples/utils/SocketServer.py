import socket
import time

# Replace 'your_module' with the actual module name
from safethread.utils import SocketServer


def on_message_received(client_socket: socket.socket, address: tuple, message: str) -> str:
    """
    Callback function that handles incoming messages from clients.
    """
    print(f"Server: Received message from {address} client: {message}")
    return f"Server response: {message}"  # Echo the message back with a prefix


def on_error(e: Exception):
    print(e)


# Create a SocketServer instance
server = SocketServer(
    host="127.0.0.1",  # Server IP address
    port=12345,        # Server port
    on_message_received=on_message_received,
    on_server_error=on_error
)

# Start the server
server.start_server()
print("Server started. Waiting for client connections...")

# Send messages to users
# server.send_message(client_socket,"Message here")

server.broadcast_message("broadcasting to everyone")

# Keep the server running for a while
# time.sleep(1)

# Stop the server
server.stop_server()
print("Server stopped.")
