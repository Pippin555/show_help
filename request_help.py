#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa
__version__ = '1.0'

from sys import exit as _exit

from tkinter import Tk
from tkinter import Button
from tkinter import Label

import socket


class RequestHelp:
    """ request a help page """

    def __init__(self):
        """ initialize the class """
        self.HOST = 'localhost'
        self.PORT = 9191
        self.socket = None

        self.root = Tk()
        self.root.title('Request Help')
        self.root.protocol("WM_DELETE_WINDOW", self._cancel)

        self.btn1 = Button(text='PianoScript',
                           command=self._piano_script,
                           width=16)

        self.btn1.grid(row=0,
                       column=0,
                       padx=2,
                       pady=2,
                       sticky='news')

        self.btn2 = Button(text='Settings-Title',
                           command=self._settings_title,
                           width=16)

        self.btn2.grid(row=0,
                       column=1,
                       padx=2,
                       pady=2,
                       sticky='news')

        self.btn3 = Button(text='Editor',
                           command=self._editor,
                           width=16)

        self.btn3.grid(row=1,
                       column=0,
                       padx=2,
                       pady=2,
                       sticky='news')

        self.lbl = Label(text='')

        self.lbl.grid(row=1,
                      column=1,
                      padx=2,
                      pady=2,
                      sticky='news')

        self.root.mainloop()

    def _piano_script(self):
        """ button clicked"""
        self.send('PianoScript')

    def _settings_title(self):
        """ button clicked """
        self.send('Settings-Title')

    def _editor(self):
        """ button clicked """
        self.send('Editor')

    def _cancel(self):
        """ window is closing """

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.send('done')
        self.root.destroy()

    def send(self, subject: str) -> None:
        """ send a message to the help socket """

        try:
            if self.socket is None:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.HOST, self.PORT))

            result = self.socket.send(subject.encode('utf-8'))
            answer = self.socket.recv(1024).decode('utf8')
            if answer == '':
                answer = 'off line'
                self.socket = None

            self.lbl.config(text=answer)

        except Exception as exc:
            error, *_ = exc.args
            if error == 10061:
                message = 'off line'
            else:
                message = str(exc)

            self.lbl.config(text=message)
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = None

    def quit(self):
        """ quitting """

        sock = self.socket
        if sock is not None:
            sock.send('done'.encode('utf-8'))


def main() -> int:
    """ main entry """

    req = RequestHelp()
    req.quit()

    return 0


if __name__ == '__main__':
    _exit(main())
