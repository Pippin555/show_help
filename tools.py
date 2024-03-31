#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from os.path import splitext

from re import compile as _compile

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
