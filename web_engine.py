#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from sys import exit as _exit
from sys import argv

from os.path import abspath
from os.path import isfile

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtCore import QRect


def display_html(html_file):
    app = QApplication(argv)
    web_view = QWebEngineView()
    web_view.setGeometry(QRect(100, 100, 1200, 800))
    web_view.load(QUrl.fromLocalFile(html_file))
    web_view.show()
    _exit(app.exec())


if __name__ == "__main__":
    html_file = abspath("./help/Pianoscript.html")
    if isfile(html_file):
        display_html(html_file)
    else:
        print('file not found {html_file}')