#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa
__version__ = '1.3'

from os.path import isfile
from os.path import abspath
from os.path import join

from os import listdir

from sys import argv
from sys import stderr
from sys import exit as _exit

from typing import Optional

import webview

from help_server import HelpServer


class WebViewContainer:
    """ the container that maintains the webview """
    def __init__(self,
                 folder: str,
                 title: str,
                 subject: str):
        """ initialize the class"""

        self._folder = folder
        self._timer = None
        self._running = False

        url = self._get_url(folder=folder,
                            subject=subject)

        print(f'help_viewer url is "{url}"')
        if url is not None:
            self.window = webview.create_window(title=title,
                                                url=url)

            self._help_server = HelpServer(callback=self._help_callback)
            self._run()

        else:
            print(f'help file not found: "{url}"', file=stderr)

    def _run(self):
        """ run the webview window """

        assert self
        webview.start()

    def close_help_server(self):
        """ program is exiting """

        if hasattr(self, '_help_server'):
            if self._help_server is not None:
                self._help_server.close()

    def _help_callback(self, subject: str):
        """ help was requested """

        if subject == 'quit':
            self._help_server = None
            return

        self._change_subject(subject)

    def _change_subject(self, subject: str):
        """ change the page """

        url = self._get_url(self._folder, subject)
        if url is None:
            return

        self.window.load_url(url)

    def _get_url(self,
                 folder: str,
                 subject: str) -> Optional[str]:
        """ find the .html file """

        assert self
        subject = subject.replace(' ', '')
        url = join(folder, f'{subject}.html')

        print(f'url is {url}')
        print(folder)
        for file in listdir(folder):
            print(join(folder, file))

        return url if isfile(url) else None


def main() -> int:
    """ the main program """

    folder = './Help'
    subject: Optional[str] = 'Pianoscript'
    title = 'Help PianoScript'

    print(f'args = {argv[1:]}')
    i_arg = iter(argv[1:])
    for arg in i_arg:
        if arg == '-f':
            folder = next(i_arg)

        if arg == '-t':
            title = next(i_arg)

        if arg == '-s':
            subject = next(i_arg)

    container = WebViewContainer(folder=abspath(folder),
                                 title=title,
                                 subject=subject)

    container.close_help_server()

    return 0


# program starts here
if __name__ == '__main__':
    _exit(main())
