#! python3.12
# coding: utf8

""" connect to the server using sockets """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2024-2024 all rights reserved'

import socket
import time

from typing import Optional
from typing import Callable


class SocketClient:
    """ simplest socket client"""

    def __init__(self, port: int):
        self._port = port

    def connect_to_server(self) -> Optional[socket]:
        """ Create a TCP/IP socket """

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        client_socket.settimeout(5)  # Timeout of 5 second

        # Connect the socket to the server address and port
        server_address = ('localhost', self._port)

        try:
            client_socket.connect(server_address)
            # print('Connected to server:', server_address)
            return client_socket

        except socket.error as e:
            # print('Error connecting to server:', e)
            return None

    def communicate(self, message: str) -> Optional[str]:
        """ establish a socket connection and send a message, return the answer """

        outer = True
        while outer:
            client_socket = self.connect_to_server()
            if client_socket is None:
                # Wait for a second before attempting to reconnect
                return None

            try:
                while outer:
                    try:
                        client_socket.sendall(message.encode())
                    except socket.error as e:
                        print('Error sending data:', e)
                        break  # Exit the loop if an error occurs

                    # Receive response from the server
                    try:
                        data = client_socket.recv(1024)
                    except socket.timeout:
                        print('No response received within timeout period')
                        continue  # Continue waiting for user input
                    except socket.error as e:
                        print('Error receiving data:', e)
                        break  # Exit the loop if an error occurs

                    if not data:
                        print('Connection closed by server')
                        break  # Exit the loop if server closes the connection

                    return data.decode()

            finally:
                pass

            # Close the connection
            print('client: close the socket')
            client_socket.close()

        return None


class SocketServer:
    """ simplest socket server """

    def __init__(self, port: int, callback: Callable, debug: bool):
        """ initialize the class"""

        self._port = port
        self._callback = callback
        self._debug = debug
        self._busy = False
        self._server_socket = None

    def listen(self):
        """ listen to TCP messages on the configured port """

        connection = None
        # Create a TCP/IP socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_address = ('localhost', self._port)
        self._server_socket.bind(server_address)
        self._busy = True

        # Listen for incoming connections
        self._server_socket.listen(1)

        if self._debug:
            print('Server is listening...')

        while self._busy:

            if self._debug:
                print('outer loop')

            # Wait for a connection
            try:
                connection, client_address = self._server_socket.accept()

                if self._debug:
                    print('Connection from', client_address)

            except socket.error as e:
                if self._debug and self._busy:
                    print('Error accepting connection:', e)
                continue  # Continue listening for new connections

            try:
                while self._busy:
                    print('inner loop')
                    # Set a timeout for receiving data
                    connection.settimeout(10)  # 10 seconds timeout (adjust as needed)
                    answer = ''
                    # Receive data from the client
                    try:
                        data = connection.recv(1024)

                    except socket.timeout:
                        if self._debug:
                            print('No data received within timeout period')
                        break  # Break out of the inner loop if timeout occurs

                    except socket.error as e:
                        if self._debug:
                            print('Error receiving data:', e)
                        break  # Break out of the inner loop if an error occurs

                    if not data:
                        break  # Break out of the inner loop if no data is received

                    message = data.decode()
                    print(message)
                    self._busy, answer = self.check_message(message)

                    # Send a response back to the client
                    connection.sendall(answer.encode())
            finally:
                pass

        if connection is not None:
            # Close the connection

            if self._debug:
                print('server: close the connection')
            connection.close()

    def close(self):
        """ ... """

        if self._debug:
            print('server.close()')

        self._busy = False
        self._server_socket.close()

    def check_message(self, message: str):
        """ check the message, get an answer from the callback """

        print(message)
        busy = message != '[QUIT]'
        if busy:
            if message and self._callback:
                answer = self._callback(message)
            else:
                answer = 'ignored'
        else:
            answer = 'Server is halting'
            if self._debug:
                print(answer)

        print(f'busy: {busy}')
        return busy, answer
