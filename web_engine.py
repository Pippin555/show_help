#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from sys import exit as _exit
from sys import argv

from os.path import abspath
from os.path import isfile
from os.path import splitext
from os.path import basename

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtCore import QRect


def display_html(html_file):

    app = QApplication(argv)
    web_view = QWebEngineView()

    title, _ = splitext(basename(html_file))
    web_view.setWindowTitle(title.capitalize())

    web_view.setGeometry(QRect(100, 100, 1200, 800))
    web_view.load(QUrl.fromLocalFile(html_file))
    web_view.show()
    _exit(app.exec())


def main() -> int:
    """ main entry """

    html_file = None
    it_arg = iter(argv[1:])

    for arg in it_arg:
        match arg:
            case '-h':
                html_file = abspath(next(it_arg))

    if not isfile(html_file):
        print(f'file not found {html_file}')
        return 1

    display_html(html_file)
    return 0


if __name__ == "__main__":
    # entry point

    _exit(main())
