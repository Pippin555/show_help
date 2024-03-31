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

from typing import Optional

from re import compile as _compile

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QListWidgetItem

from PySide6.QtCore import QModelIndex

from socket_support import SocketClient

_title_expr = _compile(r'<title>(.*?)</title>')


def has_ext(file: str, wanted: str) -> bool:
    """ return True when the file has the wanted extension """

    _, ext = splitext(file)
    return ext.lower() == wanted.lower()


def get_title(html_file: str) -> str:
    """ extract the title from a tml file """

    # Open the HTML file and read its contents
    with open(html_file, 'r', encoding='utf-8') as stream:
        html_content = stream.read()

    # Search for the title pattern in the HTML content
    match = _title_expr.search(html_content)
    if match:
        return match.groups()[0].strip()
    return 'No Title'
