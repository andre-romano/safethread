import logging
import sys
import time
from typing import Any
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

logger = logging.getLogger(__name__)


class TestSocketClient(unittest.TestCase):

    def wait(self):
        while not self.terminate:
            time.sleep(0.2)
        logger.debug("Test terminated")

    def start_server(self):
        # Start a simple server for testing
        self.host = "127.0.0.1"
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        # create a dummy client socket
        self.client_socket = None
        self.client_closed = False
        self.__server_running = True

        # control main thread
        self.terminate = False

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
            logger.debug("Client socket closed")
        self.server_socket.close()
        logger.debug("Server socket closed")
        self.server_thread.join()
        logger.debug("Server stopped")

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
                        logger.error(f"{e.__repr__()}")

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

        def on_connect(return_code: int, e: Exception | None):
            if return_code == 0:
                logger.debug("Connected")
                self.assertEqual(return_code, 0)
                self.assertIsNone(e)

                self.assertTrue(client.is_connected())
                self.assertFalse(self.client_closed)

                # Disconnect from the server
                logger.debug("disconnecting...")
                client.disconnect()

                time.sleep(0.1)

                self.stop_server()
            else:
                logger.error(f"Connection failure: {e}")
                self.assertNotEqual(return_code, 0)
                self.assertIsNotNone(e)
                raise Exception(repr(e))
            self.terminate = True

        # Create a SocketClient instance for testing
        client = SocketClient(self.host, self.port,
                              on_connect=on_connect)

        # Connect to the server
        logger.debug("connecting ...")
        client.connect()

        # wait for terminate flag
        self.wait()

    def test_send_message(self):
        """
        Test sending a message to the server and receiving a response.
        """
        self.start_server()

        def on_receive(message: Any, e: Exception | None):
            # check for errors
            if e:
                logger.error(f"{e}")
                raise e

            # check msg
            logger.debug(f"Received msg {message}")
            self.assertEqual(message, "Hello, Server!")

            # disconnect
            client.disconnect()
            self.stop_server()
            self.terminate = True

        # Create a SocketClient instance for testing
        client = SocketClient(
            self.host,
            self.port,
            on_receive=on_receive
        )

        # Connect to the server
        client.connect()

        # Send a message
        client.send("Hello, Server!")

        # wait for terminate flag
        self.wait()

    def test_send_large_message(self):
        """
        Test sending a message to the server and receiving a response.
        """
        self.start_server()

        def on_receive(message: Any, e: Exception | None):
            # check for errors
            if e:
                logger.error(f"{e}")
                raise e

            # check msg
            logger.debug(f"Received msg: {message}")
            self.assertEqual(message, self.msg)

            # disconnect
            client.disconnect()
            self.stop_server()
            self.terminate = True

        # Create a SocketClient instance for testing
        client = SocketClient(
            self.host,
            self.port,
            on_receive=on_receive
        )

        # Connect to the server
        client.connect()

        # build large message
        self.msg = ""
        for i in range(100):
            self.msg += "Hello, Server!"

        # Send a message
        client.send(self.msg)

        # wait for terminate flag
        self.wait()

    def test_persistent_connection(self):
        """Test persistent connection behavior."""
        self.start_server()
        self.finish = False

        def on_connect(return_code: int, e: Exception | None):
            if return_code == 0:
                logger.debug("Connected OK")
            else:
                logger.debug("Connection failure")

        def on_disconnect(return_code: int, e: Exception | None):
            logger.debug("Disconnected from server")
            self.finish = True

            # avoid infinite loop
            if self.terminate:
                return

            # Restart the server
            self.start_server()

            # Send a message
            self.msg = "Hello again!"
            client.send(self.msg)

        def on_receive(message: Any, e: Exception | None):
            # check for errors
            if e:
                logger.error(f"{e}")
                raise e

            # check msg
            logger.debug(f"Received msg: {message}")
            self.assertEqual(message, self.msg)

            # disconnect
            if self.finish:
                # Disconnect
                client.disconnect()
                self.stop_server()
                self.terminate = True
                logger.debug("Terminate test")
            else:
                self.stop_server()

        client = SocketClient(
            self.host, self.port, persistent=True,
            connect_timeout=None,
            on_connect=on_connect,
            on_disconnect=on_disconnect,
            on_receive=on_receive,
        )

        # Connect to the server
        client.connect()

        # Send a message
        self.msg = "Hello again!"
        client.send(self.msg)

        # wait for terminate flag
        self.wait()


if __name__ == "__main__":
    unittest.main()
