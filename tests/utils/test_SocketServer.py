import time
import unittest
import socket
import threading

from safethread.utils import SocketServer


class TestSocketServer(unittest.TestCase):

    def test_start_stop_server(self):
        """
        Test starting and stopping the server.
        """
        def on_error(e):
            raise e

        # Create a SocketServer instance for testing
        host = "127.0.0.1"
        port = 12845
        server = SocketServer(
            host,
            port,
            on_message_received=lambda sock, addr, msg: msg,
            on_server_error=on_error
        )

        # Start the server
        server.start_server()

        # Start the server
        self.assertTrue(server.is_running())

        # Wait for the server to accept the connection
        threading.Event().wait(0.1)

        # Stop the server
        server.stop_server()
        self.assertFalse(server.is_running())

    def test_accept_client_connection(self):
        """
        Test that the server accepts client connections.
        """
        def on_error(e):
            raise e

        # Create a SocketServer instance for testing
        host = "127.0.0.1"
        port = 11111
        server = SocketServer(
            host,
            port,
            on_message_received=lambda sock, addr, msg: msg,
            on_server_error=on_error
        )

        # Start the server
        server.start_server()

        # Simulate a client connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Wait for the server to accept the connection
        threading.Event().wait(0.1)

        # Verify that a client thread was created
        with server._SocketServer__client_lock:  # type: ignore
            self.assertEqual(
                len(server._SocketServer__client_threads),  # type: ignore
                1
            )

        # Clean up
        client_socket.close()

        # Start and stop the server
        server.stop_server()
        server.start_server()

        # Verify that the server socket and threads are reset
        self.assertIsNotNone(
            server._SocketServer__server_socket)  # type: ignore

        self.assertEqual(
            len(server._SocketServer__client_threads), 0)  # type: ignore

        self.assertTrue(
            server._SocketServer__server_thread.is_alive())  # type: ignore

        # Start and stop the server
        server.stop_server()
        server.start_server()

    def test_client_msg_reception(self):
        def on_error(e):
            raise e

        # Create a SocketServer instance for testing
        host = "127.0.0.1"
        port = 12845
        server = SocketServer(
            host,
            port,
            on_message_received=lambda sock, addr, msg: msg,
            on_server_error=on_error
        )

        # Start the server
        server.start_server()

        # Simulate a client connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Wait for the server to accept the connection
        threading.Event().wait(0.1)

        # Send a message from the client
        client_socket.sendall("Hello FROM Server!".encode("utf-8"))

        # Receive the response from the server
        response = client_socket.recv(1024).decode("utf-8")
        self.assertEqual(response, "Hello FROM Server!")

        # Clean up
        client_socket.close()

    def test_client_msg_reception_two(self):

        def on_msg(sock, addr, msg):
            return str(addr[0])

        def on_error(e):
            raise e

        # Create a SocketServer instance for testing
        host = "127.0.0.1"
        port = 12899
        server = SocketServer(
            host,
            port,
            on_message_received=on_msg,
            on_server_error=on_error
        )

        # Start the server
        server.start_server()

        # Simulate a client connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Wait for the server to accept the connection
        threading.Event().wait(0.1)

        # Send a message from the client
        client_socket.sendall("Hello FROM Server!".encode("utf-8"))

        # Receive the response from the server
        response = client_socket.recv(1024).decode("utf-8")
        self.assertEqual(response, "127.0.0.1")

        # Clean up
        client_socket.close()

    def test_broadcast_message(self):
        """
        Test that the server broadcasts messages to all connected clients.
        """

        def on_error(e):
            raise e

        # Create a SocketServer instance for testing
        host = "127.0.0.1"
        port = 44444
        server = SocketServer(
            host,
            port,
            on_message_received=lambda sock, addr, msg: msg,
            on_server_error=on_error
        )

        # Start the server
        server.start_server()

        # Simulate two client connections
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect((host, port))

        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect((host, port))

        # Wait for the server to accept the connection
        threading.Event().wait(0.1)

        # Broadcast a message to all clients
        server.broadcast_message("HELLO EVERYONE")

        # Verify that both clients received the message
        response1 = client1.recv(1024).decode("utf-8")
        response2 = client2.recv(1024).decode("utf-8")

        self.assertEqual(response1, "HELLO EVERYONE")
        self.assertEqual(response2, "HELLO EVERYONE")

        # Clean up
        client1.close()
        client2.close()

    def test_send_message_to_disconnected_client(self):
        """
        Test that sending a message to a disconnected client raises an error.
        """
        def on_error(e):
            raise e

        # Create a SocketServer instance for testing
        host = "127.0.0.1"
        port = 33333
        server = SocketServer(
            host,
            port,
            on_message_received=lambda sock, addr, msg: msg,
            on_server_error=on_error
        )

        # Start the server
        server.start_server()

        # Simulate a client connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Wait for the server to accept the connection
        threading.Event().wait(0.1)

        # Disconnect the client
        client_socket.close()

        # Attempt to send a message to the disconnected client
        with self.assertRaises(RuntimeError):
            server.send_message(client_socket, "Test message")


if __name__ == "__main__":
    unittest.main()
