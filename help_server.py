#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa
__version__ = '1.0'

import socket

from threading import Thread

from typing import Callable


class HelpServer:
    """ listen in on port 9191 on local host"""
    _HOST = 'localhost'
    _PORT = 9191

    def __init__(self, callback: Callable):
        self.callback = callback
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HelpServer._HOST, HelpServer._PORT))
        self.server.listen(5)  # max connections
        self.thread = Thread(target=self._run)
        self.thread.start()

    def _connect(self, comm, addr):
        """ handle one connection, there really should only be one """

        done = False
        while not done:
            # 1024 max number of bytes
            message = comm.recv(1024).decode('utf-8')
            done = message == 'done'
            if not done:
                if self.callback is not None:
                    result = self.callback(message)
                comm.send('OK'.encode('utf-8'))

        comm.close()

    def _run(self):
        """ run the server """

        while True:
            try:
                comm, addr = self.server.accept()
                thread = Thread(target=self._connect(comm, addr))
                thread.start()
            except:
                break

    def close(self):
        """ shutdown and close the server """

        # self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        if self.callback is not None:
            result = self.callback('quit')
            self.thread.join()
