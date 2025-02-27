import socket

from typing import Callable, Optional

from ..thread import ThreadBase  # Replace with the actual import path


class SocketClient:
    """
    A client class for communicating with a server that uses the SocketHandler class.

    This class allows clients to connect to the server, send messages, and receive responses
    asynchronously.

    :param host: The host address of the server to connect to.
    :type host: str
    :param port: The port number of the server to connect to.
    :type port: int
    :param protocol: The transport protocol used by server/clients. Defaults to socket.SOCK_STREAM (TCP).
    :type protocol: socket.SocketKind
    :param on_message_received: A callback function that is called when a message is received from the server.
                                The function should accept one argument: the message.
                                The function can return a message to be sent to the client, if it returns a 
                                string.
    :type on_message_received: Callable[[str], str | None]
    :param on_receive_error: A callback function that is called when an error happens when the message is being received from the server.
                                The function should accept one argument: the Exception.                                
    :type on_receive_error: Callable[[Exception], None]
    """

    def __init__(
        self,
        host: str,
        port: int,
        protocol: socket.SocketKind = socket.SOCK_STREAM,
        on_message_received: Callable[[str], str | None] = lambda msg: None,
        on_receive_error: Callable[[Exception], None] = lambda e: None,
    ) -> None:
        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__on_message_received = on_message_received
        self.__on_receive_error = on_receive_error

        # reset socket state
        self.__reset_state()

    def __reset_state(self):
        """Resets client socket state to allow it to work again (after closed / stopped )"""
        # disconnect from server?
        self.__disconnect = False

        # error in connection
        self.__error = ""

        # Client socket
        self.__client_socket = socket.socket(socket.AF_INET, self.__protocol)

        # Thread for receiving messages
        self.__receive_thread = ThreadBase(self.__receive_messages)

    def connect(self) -> None:
        """
        Connects to the server.

        :raises RuntimeError: If the client is already connected.
        """
        if self.__receive_thread.is_alive():
            raise RuntimeError("Client is already connected.")

        try:
            self.__client_socket.connect((self.__host, self.__port))
            self.__receive_thread.start()
            print(f"Connected to server at {self.__host}:{self.__port}")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to server: {e}")

    def disconnect(self) -> None:
        """
        Disconnects from the server and stops the receive thread.

        :raises RuntimeError: If the client is not connected.
        """
        if not self.__receive_thread.is_alive():
            raise RuntimeError("Client is not connected.")

        if self.__disconnect:
            raise RuntimeError("Client already disconnected.")

        self.__disconnect = True
        self.__receive_thread.stop()
        self.__client_socket.close()
        self.__receive_thread.join()
        self.__reset_state()
        print("Disconnected from server.")

    def send_message(self, message: str) -> None:
        """
        Sends a message to the server.

        :param message: The message to send.
        :type message: str

        :raises RuntimeError: If the client is not connected to the server.
        """
        if not self.__receive_thread.is_alive():
            raise RuntimeError("Client is not connected to the server.")

        try:
            self.__client_socket.sendall(message.encode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}")

    def __receive_messages(self) -> None:
        """
        Listens for incoming messages from the server.

        This method runs in a separate thread and continuously listens for messages
        from the server. When a message is received, the `on_message_received` callback
        is called (if provided).
        """
        while True:
            try:
                message = self.__client_socket.recv(1024).decode("utf-8")
                if not message:
                    break  # Server disconnected
                response = self.__on_message_received(message)
                # Send the response back to the server
                if isinstance(response, str):
                    self.__client_socket.sendall(response.encode("utf-8"))
            except Exception as e:
                # if was not a disconnection from client, then it is an error
                if not self.__disconnect:
                    self.__error = str(e)
                    self.__on_receive_error(e)
                break

        # Clean up
        try:
            self.__receive_thread.stop()
            self.__client_socket.close()
        except:
            pass
        finally:
            self.__reset_state()

    def get_status(self):
        """
        Retrieves the current status of connection.

        :return: A tuple containing a status code (0 for success, 1 for error) and an error message if any.
        """
        status = 0 if not self.__error else 1
        return (status, self.__error)

    def is_connected(self) -> bool:
        """
        Checks if the client is connected to the server.

        :return: True if connected, False otherwise.
        :rtype: bool
        """
        return self.__receive_thread.is_alive()
