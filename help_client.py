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
from os.path import join

from typing import Callable

from jsons import loads

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
    """ sub-classed """

    def __init__(self, window_closing: Callable):
        """ initialize the class """

        super().__init__()
        self.window_closing = window_closing

    def closeEvent(self, event):
        """ the event occurred """

        if self.window_closing is not None:
            self.window_closing()

        event.accept()


class HelpClient:
    """ ... """

    def __init__(self):
        """ ..."""

        self.app = QApplication(argv)
        self.main = MyMainWindow(window_closing=self.close_event)
        self.main.setGeometry(100, 100, 200, 600)
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

    def populate1(self, path: str):
        """ populate the list of help subjects """

        for file in listdir(path):
            if has_ext(file=file, wanted='.html'):
                filename = join(path, file)
                subject = get_title(filename)
                item = QListWidgetItem(filename)
                item.setData(0, subject)   # this is shown in the list
                item.setData(1, filename)  # Storing filename as userData
                self.listbox.addItem(item)

    def populate(self, path: str):
        """ populate from the _toc.json file """

        with open(file=join(path, '_toc.json'), mode='r', encoding='utf8') as stream:
            contents = stream.read()
            data = loads(contents)
            for info in data:
                value = info.get('a_attr', None)
                if value is not None:
                    href = value.get('href', None)
                    filename = join(path, href)
                    subject = info.get('text', None)
                    item = QListWidgetItem(filename)
                    item.setData(0, subject)  # this is shown in the list
                    item.setData(1, filename)  # Storing filename as userData
                    self.listbox.addItem(item)
            pass

    def on_item_selected(self, event: QModelIndex):
        """ ... """

        row = event.row()
        selected_item = self.listbox.item(row)
        if selected_item:
            filename = selected_item.data(1)  # fhe associated filename
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
    """ main entry """

    help_path = abspath(join(curdir, 'help'))

    _help = HelpClient()
    _help.populate(path=help_path)
    _help.run()
    return 0


if __name__ == "__main__":
    # entry point

    _exit(main())
