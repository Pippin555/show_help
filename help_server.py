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

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtCore import QRect
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot

from socket_support import SocketServer
from tools import get_title

from my_exception import MyException


class HelpViewer:

    def __init__(self, port: int = 4995):
        """ ... """

        self.worker = Worker(port=port)
        self.worker.finished.connect(self.worker_exit)
        self.worker_thread = Thread(target=self.worker.run)

        # self.worker = Worker2(port=port, debug=True)
        # Move the worker object to the worker thread
        # self.worker.moveToThread(self.worker_thread)
        # # Connect the signal from the worker to a slot in the main thread
        self.worker.message_received.connect(self.on_message_received)
        # self.worker_thread.started.connect(self.worker.run)  # noqa

        self.worker_thread.start()

        self.app = QApplication(argv)
        self.web_view = QWebEngineView()
        self.web_view.closeEvent = self.window_closes
        self.web_view.setGeometry(QRect(100, 100, 1200, 800))  # noqa
        self.web_view.show()

    def run(self) -> int:
        """ run the ManWindow """

        print('web_engine.run()')
        ret_code = self.app.exec()
        print(f'app.exec has exited ret_code is {ret_code}')

        return ret_code

    def window_closes(self, event):
        """ ... """

        event.accept()
        print('window closes')
        self.worker.stop()

    def worker_exit(self):
        """ ... """

        assert self
        print('web_engine.worker_exit')
        self.web_view.close()
        print('worker_exit done')

    def display_subject(self, subject):
        """ ... """

        filename = abspath(join(curdir, 'help', f'{subject}.html'))
        self.change_page(subject, filename)

    def change_page(self, subject: str, filename: str):
        """ ... """

        self.web_view.setWindowTitle(subject)
        self.web_view.load(QUrl.fromLocalFile(filename))  # noqa

    def on_message_received(self, filename: str) -> str:
        """ ... """

        if isfile(filename):
            title = get_title(filename)
            self.change_page(subject=title, filename=filename)

        return "OK"


class Worker(QObject):
    finished = Signal()
    message_received = Signal(str)  # Define a signal

    def __init__(self, port: int):
        """ ... """

        super().__init__(parent=None)
        self.port = port
        self.server = None

    @Slot()
    def run(self):
        print("Worker.run() started")

        self.server = SocketServer(port=self.port, callback=self.received, debug=False)
        self.server.listen()
        self.server.close()

        print('Worker.run() has finished')

        self.finished.emit()

    def stop(self):
        """ ... """

        try:
            self.server.close()
        except Exception as _:
            print(str(MyException()))

    def received(self, message: str) -> str:
        # This method will be called after the timer expires

        self.message_received.emit(message)
        return "OK"


def main() -> int:
    """ main entry """

    viewer = HelpViewer(port=4995)
    viewer.display_subject('Introduction')

    try:
        ret_code = viewer.run()
        print(f'main is exiting with error code {ret_code}')
        return ret_code
    except Exception as _:
        print(str(MyException()))

    print('main is exiting with error code 1')
    return 1


if __name__ == "__main__":
    # entry point

    _exit(main())
