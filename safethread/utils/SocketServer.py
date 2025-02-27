# import logging
import logging
import socket
import threading

from typing import Any, Callable, Optional, Tuple

from ..thread import ThreadBase


# logger = logging.getLogger("SocketServer")


class SocketServer:
    """
    A thread-safe asynchronous socket handler that manages server and client sockets.

    This class allows for asynchronous communication between a server and multiple clients.
    Each client connection is handled in a separate thread, and the server can send and
    receive messages asynchronously.
    """

    def __init__(
        self,
        host: str,
        port: int,
        max_clients: int = 5,
        protocol: socket.SocketKind = socket.SOCK_STREAM,
        on_message_received: Callable[[
            socket.socket, tuple, str], str | None] = lambda sock, addr, msg: None,
        on_server_error: Callable[[Exception], None] = lambda e: None,
    ) -> None:
        """
        Initializes SocketHandler instance.

        :param host: The host address to bind the server socket to.
        :type host: str
        :param port: The port number to bind the server socket to.
        :type port: int
        :param max_clients: The maximum number of clients that can connect to the server. Defaults to 5.
        :type max_clients: int
        :param protocol: The transport protocol used by server/clients. Defaults to socket.SOCK_STREAM (TCP).
        :type protocol: socket.SocketKind
        :param on_message_received: A callback function that is called when a message is received from a client.
                                    The function should accept 3 arguments: the client socket, address tuple (IP, port), and the message.
                                    The function can return a message to be sent to the client, if it returns a
                                    string.
        :type on_message_received: Callable[[socket.socket, tuple, str], str | None ]
        :param on_receive_error: A callback function that is called when an error happens when acceppting new clients,
                                in the server socket.
                                The function should accept one argument: the Exception.
        :type on_receive_error: Callable[[Exception], None]
        """
        self.__host = host
        self.__port = port
        self.__max_clients = max_clients
        self.__protocol = protocol
        self.__on_message_received = on_message_received
        self.__on_server_error = on_server_error

        # Client Threads
        self.__client_threads: list[ThreadBase] = []
        self.__client_lock = threading.RLock()

        # Server
        self.__reset_state()

    def __reset_state(self):
        """Resets server state to allow it to work again (after closed / stopped )"""
        # controls server state
        self.__error = ""
        self.__stop_server = False

        # Server socket
        self.__server_socket = socket.socket(socket.AF_INET, self.__protocol)
        self.__server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_socket.bind((self.__host, self.__port))
        self.__server_socket.listen(self.__max_clients)

        # Server Thread
        self.__server_thread = ThreadBase(self.__accept_clients)

    def __accept_clients(self) -> None:
        """
        Accepts incoming client connections and spawns a new thread for each client.

        This method runs in a separate thread and continuously listens for new client connections.
        When a client connects, a new thread is created to handle communication with that client.
        """
        while True:
            try:
                # logger.debug(f"Listening for clients ...")
                client_socket, client_address = self.__server_socket.accept()
                # logging.debug(f"New client connected: '{client_address}'")
                # Create a new thread for the client
                client_thread = ThreadBase(
                    self.__handle_client,
                    args=(client_socket, tuple(client_address),),
                )
                client_thread.start()
                # update client list
                with self.__client_lock:
                    # logging.debug(f"Adding client {client_address}")
                    self.__client_threads = [
                        t for t in self.__client_threads if t.is_alive()]
                    self.__client_threads.append(client_thread)
                    # logging.debug(f"List {self.__client_threads}")
            except Exception as e:
                if not self.__stop_server:
                    self.__error = str(e)
                    self.__on_server_error(e)
                break

    def __handle_client(self, client_socket: socket.socket, client_address: tuple) -> None:
        """
        Handles communication with a connected client.

        This method runs in a separate thread for each client and continuously listens for
        incoming messages from the client. When a message is received, the `on_message_received`
        callback is called (if provided).

        :param client_socket: The socket object representing the connected client.
        :type client_socket: socket.socket
        :param client_address: The client IP address.
        :type client_address: str
        """
        while True:
            try:
                # logger.debug(f"Waiting for msg ...")
                message = client_socket.recv(1024).decode("utf-8")
                # logging.debug(f"Received msg: {message}")
                if not message:
                    break  # Client disconnected

                response = self.__on_message_received(
                    client_socket, tuple(client_address), message)
                # Send the response back to the client
                if isinstance(response, str):
                    # logger.debug(f"Sending on_message_received() response to client... ")
                    client_socket.sendall(response.encode("utf-8"))
            except ConnectionError:
                break  # Client disconnected abruptly

        # Clean up
        # logger.debug("Finishing client socket ...")
        client_socket.close()

    def is_running(self) -> bool:
        """
        Checks if the server is running.

        :return: True if running, False otherwise.
        :rtype: bool
        """
        return self.__server_thread.is_alive()

    def get_status(self):
        """
        Retrieves the current status of the server.

        :return: A tuple containing a status code (0 for success, 1 for error) and an error message if any.
        """
        status = 0 if not self.__error else 1
        return (status, self.__error)

    def start_server(self) -> None:
        """
        Starts the server thread to accept incoming client connections.

        :raises RuntimeError: If the server thread is already running.
        """
        if self.__server_thread.is_alive():
            raise RuntimeError("Server is already running.")
        self.__server_thread.start()
        # logger.debug(f"Server started")

    def stop_server(self) -> None:
        """
        Stops the server thread and closes all client connections.

        This method stops the server thread and closes all active client sockets.

        :raises RuntimeError: If the server thread is already stopping or stopped.
        """
        if not self.__server_thread.is_alive():
            raise RuntimeError("Server is already stopped")
        if self.__stop_server:
            raise RuntimeError("Server is stopping ...")

        # logger.debug("Stopping server ...")
        self.__server_thread.stop()
        with self.__client_lock:
            for client_thread in self.__client_threads:
                client_thread.stop()
            self.__client_threads.clear()
        self.__stop_server = True
        self.__server_socket.close()
        # logger.debug("Server socket closed ...")
        self.__server_thread.join()
        # logger.debug("Server TERMINATED")
        self.__reset_state()

    def send_message(self, client_socket: socket.socket, message: str) -> None:
        """
        Sends a message to a specific client.

        :param client_socket: The socket object representing the client to send the message to.
        :type client_socket: socket.socket
        :param message: The message to send.
        :type message: str

        :raises RuntimeError: If the client socket is not connected.
        """
        try:
            # logger.debug(f"Sending message {message} ...")
            client_socket.sendall(message.encode("utf-8"))
            # logger.debug(f"OK")
        except (ConnectionError, OSError):
            raise RuntimeError(
                "Failed to send message: Client is not connected.")

    def broadcast_message(self, message: str) -> None:
        """
        Sends a message to all connected clients.

        :param message: The message to broadcast.
        :type message: str
        """
        with self.__client_lock:
            # logging.debug(f"Broadcasting message: '{message}'")
            for client_thread in self.__client_threads:
                if client_thread.is_alive():
                    # Extract client socket from thread args
                    client_socket = client_thread.get_args()[0]
                    self.send_message(client_socket, message)
