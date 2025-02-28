import logging
import queue
import select
import socket
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
    """

    def __init__(
        self,
        host: str,
        port: int,
        protocol: socket.SocketKind = socket.SOCK_STREAM,
        connect_timeout: float = 5,  # seconds
        reconnect_wait: float = 0.5,  # seconds
        persistent: bool = False,
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
                        Defaults to 5 seconds.
        :type connect_timeout: float
        :param reconnect_wait: Reconnect wait (in seconds) to retry socket connection. 
                        Defaults to 0.5 seconds.
        :type reconnect_wait: float
        :param persistent: If client socket must be persistent (retry when connection fails). 
                        Defaults to False (do not retry).
        :type persistent: bool
        """
        # Config
        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__persistent_socket = persistent
        self.__connect_timeout = connect_timeout
        self.__reconnect_wait = reconnect_wait

        # connected to server?
        self.__connected = False

        # Queues
        self.__send_queue = queue.Queue()
        self.__recv_queue = queue.Queue()
        self.__error_queue = queue.Queue()

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
            while True:
                try:
                    self.__recv_messages()
                    self.__send_messages()
                    time.sleep(0.5)  # limit CPU usage
                except:
                    break

            # if socket is persistent, retry connection after timeout
            if self.__persistent_socket:
                time.sleep(self.__reconnect_wait)  # wait
            else:
                self.disconnect()  # close socket

    def __connect(self):
        """
        Connects to the server (blocking call)

        :raises RuntimeError: other errors
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
            _, writable, _ = select.select([], [self.__client_socket], [])

            # Check if the connection was successful
            err = self.__client_socket.getsockopt(
                socket.SOL_SOCKET, socket.SO_ERROR)
            if err != 0:
                e = ConnectionError(f"getsockopt() error code {err}")
                logging.error(f"Failed to connect to server: {e.__repr__()}")
                raise e
        except Exception as e:
            e = RuntimeError(f"Failed to connect to server: {e.__repr__()}")
            logger.error(f"{e}")
            self.__error_queue.put(e)
            self.__connection_callback_fail()
            return
        logging.debug(
            f"Connected to server at {self.__host}:{self.__port}")
        self.__connected = True
        self.__connection_callback_succ()

    def __recv_messages(self):
        """
        Listens for incoming messages from the server.

        :raises ConnectionAbortedError, ConnectionResetError, EOFError, BrokenPipeError: if socket disconnected from server.
        :raises queue.Full: if receive queue is FULL (valid only if receive queue max size is limited).
        :raises RuntimeError: in case of other errors.
        """

        try:
            while True:  # store all data stored in recv inside receive queue
                message = self.__client_socket.recv(1024)
                try:
                    message = message.decode("utf-8")
                except UnicodeDecodeError:
                    pass  # Keep message as bytes if decoding fails
                if not message:
                    raise ConnectionAbortedError("Server disconnected")
                logger.debug(f"Recv message {message}")
                self.__recv_queue.put(message, block=False)
        except BlockingIOError:
            pass  # no data to be received in socket.recv()
        except queue.Full as e:
            raise queue.Full(
                f"Failed to receive message: 'receive queue is FULL'")
        except (
            OSError,  # sock.recv() errors after sock.close()
            ConnectionAbortedError,  # sock.close() from server
            ConnectionResetError,  # TCP reset
            BrokenPipeError,  # sock.close() from server, during recv
            EOFError,  # fin from server
            queue.ShutDown  # socket.disconnect() call
        ) as e:
            raise e
        except Exception as e:
            # if was not a disconnection from client/server, then it is an error
            e = RuntimeError(f"Failed to receive message: '{e.__repr__()}'")
            if self.is_connected():
                self.__error_queue.put(e)
            logger.error(f"{e}")
            raise e

    def __send_messages(self) -> None:
        """
        Send messages to server (blocking).

        :raises queue.ShutDown: if disconnect() is called (socket is closed)
        """
        try:
            while True:  # send all data stored inside send queue
                message = self.__send_queue.get(block=False)
                logger.debug(f"Sending message {message} ...")
                if isinstance(message, str):
                    message = message.encode("utf-8")
                self.__send_data(message)
        except queue.Empty:
            pass  # no item to be sent now
        except queue.ShutDown as e:
            raise e  # socket disconnected, indicate it here
        except Exception as e:
            e = RuntimeError(f"Failed to send message: '{e.__repr__()}'")
            self.__error_queue.put(e)
            logger.error(f"{e}")

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
                _, writable, _ = select.select([], [self.__client_socket], [])

    def connect(self,
                callback_succ: Callable[[], None] = lambda: None,
                callback_fail: Callable[[], None] = lambda: None,
                ) -> None:
        """
        Connects to the server, listens for incoming messages, and sends outbound data.

        :param callback_succ: Run callback if connection success. 
                            Callback must have no arguments.
                            Defaults to lambda:None.
        :type callback_succ: Callable[[],None]
        :param callback_fail: Run callback if connection failed.
                            Callback must have no arguments.
                            Defaults to lambda:None.
        :type callback_fail: Callable[[],None]

        :raises ThreadBase.CallableException: If any callback argument is not callable.
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

        # check callbacks
        self.__connection_callback_succ = ThreadBase.is_callable(callback_succ)
        self.__connection_callback_fail = ThreadBase.is_callable(callback_fail)

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
            self.__recv_queue.shutdown(immediate=True)
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
        Schedules a message (string, or binary) to be sent to the server.

        :param message: The message to send.
        :type message: Any
        :param block: True, if the command should block until message can be put in 
                    the send queue, False otherwise. Defaults to True.
        :type block: bool
        :param timeout: Timeout to put the message in the send queue. Default to None 
                        (no timeout).
        :type timeout: float | None

        :raises queue.Full: if send queue is full (and block=True or timeout expired)
        :raises queue.ShutDown: if socket disconnected
        """
        self.__send_queue.put(message, block=block, timeout=timeout)

    def receive(self, block: bool = True, timeout: float | None = None) -> Any:
        """
        Receives a message (string, or binary) from the server.

        :param block: True, if the command should block until message can be get() 
                    from receive queue, False otherwise. Defaults to True.
        :type block: bool
        :param timeout: Timeout to get the message from receive queue. 
                        Default to None (no timeout).
        :type timeout: float | None

        :raises queue.Empty: if receive queue is empty (and block=True or timeout expired)
        :raises queue.ShutDown: if socket disconnected
        """
        return self.__recv_queue.get(block=block, timeout=timeout)

    def get_error(self, block: bool = True, timeout: float | None = None) -> Exception:
        """
        Returns the exception object associated with the error reported.

        :param block: True, if the command should block until an Exception is raised,
                    False otherwise. Defaults to True.
        :type block: bool
        :param timeout: Timeout to wait for Exceptions raised inside socket code. 
                        Default to None (no timeout).
        :type timeout: float | None

        :returns: Exception object

        :raises queue.Empty: if receive queue is empty (and block=True or timeout expired)
        :raises queue.ShutDown: if socket disconnected
        """
        return self.__error_queue.get(block=block, timeout=timeout)

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
