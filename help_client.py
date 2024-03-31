#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from sys import exit as _exit
from sys import argv

from os import listdir
from os import curdir

from os.path import abspath
from os.path import isfile
from os.path import join
from os.path import splitext
from os.path import basename
from os.path import split

from typing import Callable

from re import compile as _compile

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QListWidgetItem

from PySide6.QtCore import QModelIndex

from socket_support import SocketClient

from tools import has_ext
from tools import get_title


class MyMainWindow(QMainWindow):
    """ sub-clossed """

    def __init__(self, window_closing: Callable):
        """ initialize the class """

        super().__init__()
        self.window_closing = window_closing

    def closeEvent(self, event):
        """ the event occurred """

        print('MyWindow close event')
        if self.window_closing is not None:
            self.window_closing()
        event.accept()


class HelpClient:
    """ ... """

    def __init__(self):
        """ ..."""

        self.app = QApplication(argv)
        self.main = MyMainWindow(window_closing=self.close_event)
        self.main.setGeometry(100,100,200,600)
        self.main.setWindowTitle('Help Client')

        # Create a central widget
        central_widget = QWidget()
        self.main.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        self.listbox = QListWidget()
        self.layout.addWidget(self.listbox)
        # Connect item selection signal to a custom slot
        self.listbox.doubleClicked.connect(self.on_item_selected)
        self.client = SocketClient(port=4995)
        self.main.show()

    def close_event(self):
        # Perform any necessary cleanup before closing the window

        print('Help Client close event')
        if self.client is not None:
            answer = self.client.communicate('[QUIT]')
            print(f'answer {answer}')

    def populate(self, path: str):
        """ populate the list of help subjects """

        for file in listdir(path):
            if has_ext(file=file, wanted='.html'):
                filename = join(path, file)
                subject = get_title(filename)
                item = QListWidgetItem(filename)
                item.setData(0, subject)  # this is shown in the list
                item.setData(1, filename) # Storing filename as userData
                self.listbox.addItem(item)

    def on_item_selected(self, event: QModelIndex):
        """ ... """

        row = event.row()
        selected_item = self.listbox.item(row)
        if selected_item:
            title = selected_item.data(0)     # the title that was selected
            filename = selected_item.data(1)  # fhe associated filename

            # print(f'Selected Title: {title}')
            # print(f'Filename:       {filename}')
            self.display_help_page(filename)

    def display_help_page(self, filename):
        """ ... """
        print(f'display {filename}')
        answer = self.client.communicate(filename)
        if answer is None:
            print('could not connect to the server')
        else:
            print(f'answer {answer}')

    def run(self) -> int:
        """ run the main window """

        return self.app.exec()


def main() -> int:
    _help = HelpClient()
    _help.populate(abspath(join(curdir, 'help')))
    _help.run()
    return 0


if __name__ == "__main__":
    # entry point

    _exit(main())
