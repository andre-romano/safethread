import logging
import sys
import time
import unittest
import socket
import threading

from safethread.utils import SocketClient

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set logging level
    # Log format
    format="%(asctime)s - [%(levelname)s] - %(name)s() - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
    handlers=[logging.StreamHandler(sys.stdout)]  # Log to stdout
)


class TestSocketClient(unittest.TestCase):

    def start_server(self):
        # Start a simple server for testing
        self.host = "127.0.0.1"
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        # create a dummy client socket
        self.client_socket = None
        self.client_closed = False
        self.__server_running = True

        # Start the server in a separate thread
        self.server_thread = threading.Thread(
            target=self._run_server, daemon=True)
        self.server_thread.start()

        self.result = ""

    def stop_server(self):
        # Disconnect the client and stop the server
        self.__server_running = False
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()
        self.server_thread.join()

    def _run_server(self):
        """
        A simple server that echoes messages back to the client.
        """
        while self.__server_running:
            try:
                self.client_socket, self.client_address = self.server_socket.accept()
                self.client_closed = False
                print(f"Server: Connected to {self.client_address}")

                while self.__server_running:
                    try:
                        message = self.client_socket.recv(1024).decode("utf-8")
                        if not message:
                            break  # Client disconnected
                        print(f"Server: Received '{message}'")
                        self.client_socket.sendall(message.encode(
                            "utf-8"))  # Echo the message back
                    except (
                        ConnectionAbortedError,  # sock.close() from server
                        ConnectionResetError  # TCP reset
                    ) as e:
                        break
                    except Exception as e:
                        logging.error(f"{e.__repr__()}")

                self.client_socket.close()
                self.client_closed = True
                print(f"Server: Disconnected from {self.client_address}")
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

        def on_connect():
            logging.debug("Connected -")
            self.assertTrue(client.is_connected())
            logging.debug("OK")

        # Connect to the server
        client.connect(callback_succ=on_connect)
        logging.debug("connecting ...")
        time.sleep(0.1)

        # Disconnect from the server
        client.disconnect()
        logging.debug("disconnecting...")

        time.sleep(0.1)
        self.assertFalse(client.is_connected())
        self.assertTrue(self.client_closed)

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
        )

        # Connect to the server
        client.connect()

        # Send a message
        client.send("Hello, Server!")

        message = client.receive()
        logging.debug(f"Received msg {message}")
        self.assertEqual(message, "Hello, Server!")

        client.disconnect()
        self.stop_server()

    def test_persistent_connection(self):
        """Test persistent connection behavior."""
        self.start_server()

        client = SocketClient(self.host, self.port, persistent=True)

        def on_connect():
            self.assertTrue(client.is_connected())

        # Connect to the server
        client.connect(callback_succ=on_connect)

        # Send a message
        client.send("Hello again!")
        message = client.receive()
        self.assertEqual(message, "Hello again!")

        # Simulate server disconnection
        self.stop_server()

        time.sleep(1)  # Wait for client to detect disconnection

        # Restart the server
        self.start_server()

        # Send a message
        client.send("Hello again!")
        message = client.receive()
        self.assertEqual(message, "Hello again!")

        # Disconnect
        client.disconnect()
        self.stop_server()


if __name__ == "__main__":
    unittest.main()
