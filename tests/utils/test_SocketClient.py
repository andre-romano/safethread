import logging
import unittest
import socket
import threading

# Replace 'your_module' with the actual module name
from safethread.utils import SocketClient


class TestSocketClient(unittest.TestCase):
    def start_server(self):
        # Start a simple server for testing
        self.host = "127.0.0.1"
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.start()

        self.result = ""

    def stop_server(self):
        # Disconnect the client and stop the server
        self.server_socket.close()
        self.server_thread.join()

    def on_msg_client(self, msg):
        self.result = msg
        return None

    def on_msg_client_reply(self, msg):
        self.result = msg
        return msg

    def _run_server(self):
        """
        A simple server that echoes messages back to the client.
        """
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Server: Connected to {client_address}")

                while True:
                    message = client_socket.recv(1024).decode("utf-8")
                    if not message:
                        break  # Client disconnected
                    print(f"Server: Received '{message}'")
                    client_socket.sendall(message.encode(
                        "utf-8"))  # Echo the message back

                client_socket.close()
                print(f"Server: Disconnected from {client_address}")
            except OSError:
                # Server socket closed, stop the server
                break

    def test_connect_disconnect(self):
        """
        Test connecting and disconnecting from the server.
        """
        self.start_server()

        # Create a SocketClient instance for testing
        client = SocketClient(self.host, self.port)

        # Connect to the server
        client.connect()
        self.assertTrue(client.is_connected())

        # Disconnect from the server
        client.disconnect()
        self.assertFalse(client.is_connected())

        self.stop_server()

    def test_send_message(self):
        """
        Test sending a message to the server and receiving a response.
        """
        self.start_server()

        # Create a SocketClient instance for testing
        client = SocketClient(
            self.host,
            self.port,
            on_message_received=self.on_msg_client
        )

        # Connect to the server
        client.connect()

        # Send a message
        client.send_message("Hello, Server!")

        threading.Event().wait(0.1)
        self.assertEqual(self.result, "Hello, Server!")

        client.disconnect()
        self.stop_server()

    def test_receive_error(self):
        """
        Test handling errors during message reception.
        """
        self.start_server()

        def on_error(e):
            self.result = str(e)

        # Create a SocketClient instance for testing
        client = SocketClient(
            self.host,
            self.port,
            on_message_received=self.on_msg_client,
            on_receive_error=on_error
        )

        # Connect to the server
        client.connect()

        threading.Event().wait(0.1)

        # Simulate a server disconnection
        self.server_socket.close()

        threading.Event().wait(0.1)

        # Send a message
        client.send_message("Hello, Server!")

        threading.Event().wait(0.1)

        self.assertNotEqual(self.result, "")

        client.disconnect()
        self.stop_server()

    def test_get_status(self):
        """
        Test retrieving the connection status.
        """
        self.start_server()

        def on_error(e):
            self.result = str(e)

        # Create a SocketClient instance for testing
        client = SocketClient(
            self.host,
            self.port,
            on_message_received=self.on_msg_client,
            on_receive_error=on_error
        )

        # Connect to the server
        client.connect()

        # Check the status (should be success)
        status, error = client.get_status()
        self.assertEqual(status, 0)
        self.assertEqual(error, "")

        # Simulate an error
        client._SocketClient__error = "Connection error"  # type: ignore
        status, error = client.get_status()
        self.assertEqual(status, 1)
        self.assertEqual(error, "Connection error")

        client.disconnect()
        self.stop_server()

    def test_is_connected(self):
        """
        Test checking if the client is connected to the server.
        """
        self.start_server()

        def on_error(e):
            self.result = str(e)

        # Create a SocketClient instance for testing
        client = SocketClient(
            self.host,
            self.port,
            on_message_received=self.on_msg_client,
            on_receive_error=on_error
        )

        # Connect to the server
        client.connect()
        self.assertTrue(client.is_connected())

        # Disconnect from the server
        client.disconnect()
        self.assertFalse(client.is_connected())

        self.stop_server()


if __name__ == "__main__":
    unittest.main()
