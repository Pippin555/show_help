#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from sys import exit as _exit
from sys import argv

from os import curdir

from os.path import abspath
from os.path import isfile
from os.path import join

from threading import Thread
from typing import Optional

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtCore import QRect

from socket_support import SocketServer


class HelpViewer:

    def __init__(self, port: int = 4995):
        """ ... """

        self.thread = Thread(target=self.socket_thread)
        self.server = SocketServer(port=port, callback=self.change_page, debug=True)

    def socket_thread(self):
        """ ... """
        self.server.listen()

    def display_subject(self, subject):
        """ ... """

        self.app = QApplication(argv)
        self.web_view = QWebEngineView()
        self.web_view.setWindowTitle(subject.capitalize())

        self.web_view.setGeometry(QRect(100, 100, 1200, 800))
        file = self.html_file(subject=subject)
        if file is not None:
            self.web_view.load(QUrl.fromLocalFile(file))
        self.web_view.show()
        _exit(self.app.exec())

    def html_file(self, subject: str) -> Optional[str]:
        """ ... """

        file = abspath(join(curdir, 'help', f'{subject}.html'))
        if not isfile(file):
            print(f'subject not found {subject}')
            return None
        return file

    def change_page(self, subject: str):
        """ ... """

        file = self.html_file(subject=subject)
        if file is not None:
            self.web_view.load(QUrl.fromLocalFile(file))


def main() -> int:
    """ main entry """

    subject = None
    it_arg = iter(argv[1:])

    for arg in it_arg:
        match arg:
            case '-h':
                subject = next(it_arg)

    viewer = HelpViewer(port=4995)
    viewer.display_subject(subject)
    return 0


if __name__ == "__main__":
    # entry point

    _exit(main())
