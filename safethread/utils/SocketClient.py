import json
import logging
import queue
import select
import socket
import struct
import time

from typing import Any, Callable, Optional, Type

from ..thread import ThreadBase

from .utils import *

# get logger instance
logger = logging.getLogger(__name__)


class SocketClient:
    """
    A asynchronous client class for communicating with a server that uses the SocketHandler class.

    This class allows clients to connect to the server, send messages, and receive responses
    asynchronously, using send and receive queues.

    The messages exchanged between client <-> server must be JSON serializable.
    """

    @staticmethod
    def __to_bytes(message: str) -> bytes:
        """
        Encodes a string message into a sequence of bytes.

        :param message: Message to encode.
        :type message: str

        :raises UnicodeEncodeError: if message cannot be encoded.
        """
        return message.encode("utf-8")

    @staticmethod
    def __from_bytes(message: bytes) -> Any:
        """
        Decodes a message, using JSON deserialization method.

        :param message: Message to decode.
        :type message: bytes

        :raises TypeError: if message cannot be deserialized using JSON.
        """
        if not isinstance(message, bytes):
            raise TypeError(
                f"from_bytes(): Unsupported value type '{type(message)}'")
        return json.loads(message)

    def __init__(
        self,
        host: str,
        port: int,
        protocol: socket.SocketKind = socket.SOCK_STREAM,
        connect_timeout: float | None = 5,  # seconds
        reconnect_wait: float = 0.5,  # seconds
        persistent: bool = False,
        on_connect: Callable[[int, Exception | None],
                             None] = lambda return_code, e: None,
        on_disconnect: Callable[[int, Exception | None],
                                None] = lambda return_code, e: None,
        on_receive: Callable[[Any, Exception | None],
                             None] = lambda message, e: None,
        on_send: Callable[[Any, Exception | None],
                          None] = lambda message, e: None,
    ) -> None:
        """
        Initialized async SocketClient class

        :param host: The host address of the server to connect to.
        :type host: str

        :param port: The port number of the server to connect to.
        :type port: int

        :param protocol: The transport protocol used by server/clients. Defaults to socket.SOCK_STREAM (TCP).
        :type protocol: socket.SocketKind    

        :param connect_timeout: Connect timeout (in seconds) for socket non-blocking connection. 
                        If connect_timeout is None, timeout is disabled.
                        Defaults to 5 seconds.
        :type connect_timeout: float | None

        :param reconnect_wait: Reconnect wait (in seconds) to retry socket connection. 
                        Defaults to 0.5 seconds.
        :type reconnect_wait: float

        :param persistent: If client socket must be persistent (retry when connection fails). 
                        Defaults to False (do not retry).
        :type persistent: bool

        :param on_connect: Run callback if connection success or error. 
                            Callback must have two arguments: a return code and an Exception raised during connection.
                            If connection success, return code = 0 and Exception = None.
                            If connection failed, return code != 0 and Exception is instance of Exception.
                            Defaults to ``lambda return_code,e: None``.
        :type on_connect: Callable[[int, Exception | None], None]

        :param on_disconnect: Run callback when socket is disconnected. 
                            Callback must have two arguments: a return code and an Exception raised during connection.
                            If connection success, return code = 0 and Exception = None.
                            If connection failed, return code != 0 and Exception is instance of Exception.
                            Defaults to ``lambda return_code,e: None``.
        :type on_disconnect: Callable[[int, Exception | None], None]

        :param on_receive: Run callback when a message is received (incoming data from server). 
                            Callback must have two arguments: message and an Exception raised during data reception.
                            If receive success, Exception = None.
                            If receive failed, Exception is instance of Exception.
                            Defaults to ``lambda message,e: None``.
        :type on_receive: Callable[[Any, Exception | None], None]

        :param on_send: Run callback when a message is sent (outbound data sent to server). 
                            Callback must have two arguments: message and an Exception raised during data sending.
                            If send success, Exception = None.
                            If send failed, Exception is instance of Exception.
                            Defaults to ``lambda message,e: None``.
        :type on_send: Callable[[Any, Exception | None], None]

        :raises ThreadBase.CallableException: If any callback argument is not callable.
        """
        # Config
        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__persistent_socket = persistent
        self.__connect_timeout = connect_timeout
        self.__reconnect_wait = reconnect_wait

        # check callbacks
        self.__on_connect = ThreadBase.is_callable(on_connect)
        self.__on_disconnect = ThreadBase.is_callable(on_disconnect)
        self.__on_receive = ThreadBase.is_callable(on_receive)
        self.__on_send = ThreadBase.is_callable(on_send)

        # connected to server?
        self.__connected = False

        # Receive buffer
        self.__recv_buffer: bytes = b""  # recv buffer
        self.__recv_msg_size: int = 0  # recv msg size

        # Queues
        self.__send_queue = queue.Queue()

        # Threads
        self.__thread = ThreadBase(self.__handle_socket)

        # Client socket
        self.__create_socket()

    def __del__(self):
        # close and reset socket
        self.disconnect()

    def __create_socket(self):
        """Creates client socket"""
        self.__client_socket = socket.socket(socket.AF_INET, self.__protocol)
        # Make the socket non-blocking
        # -- socket operations can now raise BlockingIOError
        self.__client_socket.setblocking(False)

    def __handle_socket(self) -> None:
        """
        Connects with the server, listens for incoming messages, and sends pending messages.

        This method runs in a separate thread and continuously listens for messages
        from the server, and sends messages to the server. When a message is received, it
        is placed inside the receive_queue. When a message needs to be sent, it must be placed
        in the send queue.

        If socket is persistent, then it will try to reconnect with the server automatically.
        """
        while self.__thread_continue:
            # sync socket.connect() call
            self.__connect()

            # receive messages
            self.__recv_buffer = b""
            self.__recv_msg_size = 0
            while True:
                try:
                    self.__recv_messages()
                    self.__send_messages()
                    time.sleep(0.5)  # limit CPU usage
                except (
                    OSError,  # sock.recv() errors after sock.close()
                    ConnectionAbortedError,  # sock.close() from server
                    ConnectionResetError,  # TCP reset
                    BrokenPipeError,  # sock.close() from server, during recv
                    EOFError,  # fin from server
                    queue.ShutDown,  # disconnect() called
                ) as e:
                    self.__on_disconnect(0, None)
                    break
                except Exception as e:
                    self.__on_disconnect(1, e)
                    break

            # if socket is persistent, retry connection after timeout
            if self.__persistent_socket:
                time.sleep(self.__reconnect_wait)  # wait
            else:
                self.disconnect()  # close socket

    def __connect(self):
        """
        Connects to the server (blocking call)

        :raises ConnectionError: if connection fails
        """
        try:
            # close old socket
            self.__connected = False
            self.__client_socket.close()

            # create new socket and connect
            self.__create_socket()
            self.__client_socket.connect((self.__host, self.__port))
        except BlockingIOError:  # The connection in progress (non-blocking)
            logging.info("Connection is in progress (non-blocking mode)")

            # Use select to wait for the socket to become writable
            _, writable, _ = select.select(
                [], [self.__client_socket], [], self.__connect_timeout)
            if not writable:
                e = ConnectionError(f"Connection timeout")
                logging.error(f"{e.__repr__()}")
                raise e

            # Check if the connection was successful
            err = self.__client_socket.getsockopt(
                socket.SOL_SOCKET, socket.SO_ERROR)
            if err != 0:
                e = ConnectionError(f"getsockopt() error code {err}")
                logging.error(f"Failed to connect to server: {e.__repr__()}")
                raise e
        except Exception as e:
            e = ConnectionError(f"Failed to connect to server: {e.__repr__()}")
            logger.error(f"{e}")
            self.__on_connect(1, e)
            return
        logging.debug(
            f"Connected to server at {self.__host}:{self.__port}")
        self.__connected = True
        self.__on_connect(0, None)

    def __recv_messages(self):
        """
        Listens for incoming messages from the server.

        :raises ConnectionAbortedError, ConnectionResetError, EOFError, BrokenPipeError: if socket disconnected from server.
        :raises RuntimeError: in case of other errors.
        """
        try:
            # get buffer data
            self.__recv_buffer += self.__client_socket.recv(1024)
            if not self.__recv_buffer:
                raise ConnectionAbortedError("Server disconnected")

            # get size, if unknown
            logger.debug(f"Received data - Decoding msg_size ...")
            if self.__recv_msg_size <= 0:
                size_bytes = self.__recv_buffer[:4]
                self.__recv_msg_size = struct.unpack('>i', size_bytes)[0]
                self.__recv_buffer = self.__recv_buffer[4:]

            # get message, until size is full-filled
            logger.debug(
                f"Msg_size = {self.__recv_msg_size} bytes - Receiving message ...")
            remaining_msg_size = self.__recv_msg_size - len(self.__recv_buffer)
            while remaining_msg_size > 0:
                try:
                    data = self.__client_socket.recv(1024)
                    if not data:
                        raise ConnectionAbortedError("Server disconnected")
                    data_size = len(data)
                    logger.debug(
                        f"Received {data_size}  bytes - {remaining_msg_size} remaining ...")
                    self.__recv_buffer += data
                    remaining_msg_size -= data_size
                except BlockingIOError:  # no data to be received
                    # Wait until the socket is ready for reading
                    logger.debug("Waiting for incoming data ...")
                    readable, _, _ = select.select(
                        [self.__client_socket], [], [], 1)

            # decode message
            logger.debug(f"Decoding message ...")
            message_bytes = self.__recv_buffer[:self.__recv_msg_size]
            message = self.__from_bytes(message_bytes)
            self.__recv_buffer = self.__recv_buffer[self.__recv_msg_size:]
            self.__recv_msg_size = 0

            # pass message to on_receive
            logger.debug(f"Recv message {message}")
            self.__on_receive(message, None)
        except BlockingIOError:
            pass  # no data to be received in socket.recv()
        except (
            OSError,  # sock.recv() errors after sock.close()
            ConnectionAbortedError,  # sock.close() from server
            ConnectionResetError,  # TCP reset
            BrokenPipeError,  # sock.close() from server, during recv
            EOFError,  # fin from server
        ) as e:
            raise e
        except Exception as e:
            # if was not a disconnection from client/server, then it is an error
            e = RuntimeError(
                f"Failed to receive message: '{e.__repr__()}'")
            logger.error(f"{e}")
            self.__on_receive(message, e)
            raise e

    def __send_messages(self) -> None:
        """
        Send messages to server (blocking).

        :raises queue.ShutDown: if disconnect() is called (socket is closed)
        """
        message = None
        try:
            message = self.__send_queue.get(block=False)

            # encode message to bytes (using big endian 4 bytes)
            logger.debug(f"Encoding message ...")
            message_bytes = self.__to_bytes(message)
            message_bytes = struct.pack(
                '>i', len(message_bytes)) + message_bytes

            # send message
            logger.debug(f"Sending message {message} ...")
            self.__send_data(message_bytes)
            self.__on_send(message, None)
            logger.debug(f"Message sent!")
        except queue.Empty:
            pass  # no item to be sent now
        except queue.ShutDown as e:
            raise e  # socket disconnected, indicate it here
        except Exception as e:
            e = RuntimeError(f"Failed to send message: '{e.__repr__()}'")
            logger.error(f"{e}")
            self.__on_send(message, e)

    def __send_data(self, data: bytes):
        """
        Attempts to send data on a socket with retries (blocking).

        :param data: The data to send.
        :type data: bytes
        """
        while data:
            try:
                # Attempt to send data
                sent = self.__client_socket.send(data)
                data = data[sent:]  # Remove the sent data from the buffer
            except BlockingIOError:
                # Wait until the socket is ready for writing
                _, writable, _ = select.select(
                    [], [self.__client_socket], [], 1)

    def connect(self) -> None:
        """
        Connects to the server, listens for incoming messages, and sends outbound data.

        :raises RuntimeError: If the socket is already connected, connecting, or is closed.
        """
        # check socket connection state
        if self.is_connected():
            raise RuntimeError("Socket is connected")
        if self.is_connecting():
            raise RuntimeError(
                "Socket is connecting, and thread is running ...")
        if self.is_closed():
            raise RuntimeError(
                "Socket is closed. Cannot reconnect from a closed socket.")

        # start threads
        self.__thread_continue = True
        self.__thread.start()

    def disconnect(self) -> None:
        """
        Disconnects the socket, releasing resources.

        Calling this method will close the socket and stop the internal thread.
        """

        try:
            # Update thread invariant
            self.__thread_continue = False

            # Close socket
            self.__connected = False
            self.__client_socket.close()

            # Shutdown queues
            self.__send_queue.shutdown(immediate=True)

            # Stop and join threads
            try_except_finally_wrap(self.__thread.stop_join)
        except Exception as e:
            logger.debug(
                f"SocketClient - Error during socket disconnect: {e}")
        finally:
            logger.debug("Disconnected from server.")

    def send(self, message: Any, block: bool = True, timeout: float | None = None) -> None:
        """
        Schedules a JSON serializable message to be sent to the server.

        :param message: The message to send (must be JSON serializable).
        :type message: Any
        :param block: True, if the command should block until message can be put in 
                    the send queue, False otherwise. Defaults to True.
        :type block: bool
        :param timeout: Timeout to put the message in the send queue. Default to None 
                        (no timeout).
        :type timeout: float | None

        :raises TypeError: if message is not JSON serializable
        :raises queue.Full: if send queue is full (and block=True or timeout expired)
        :raises queue.ShutDown: if socket disconnected
        """
        self.__send_queue.put(json.dumps(message),
                              block=block, timeout=timeout)

    def is_connected(self) -> bool:
        """
        Checks if the client is connected to the server.

        :return: True if connected, False otherwise.
        :rtype: bool
        """
        return self.__connected

    def is_connecting(self) -> bool:
        """
        Checks if the client is trying to connect with the server.

        :return: True if connection is in progress, False otherwise.
        :rtype: bool
        """
        return self.__thread.is_alive()

    def is_closed(self) -> bool:
        """
        Checks if the socket is closed (disconnected).

        :return: True if socket closed, False otherwise.
        :rtype: bool
        """
        return self.__thread.is_terminated()
