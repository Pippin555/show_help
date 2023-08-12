#! python3.11
# coding: utf-8`

""" the GUI for the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa
__version__ = 'Sihir.entertainment.player.v1.0'  # noqa

from sys import exit as _exit

from tkinter import Tk

from pygame.mixer import music as _music
from pygame.mixer import init as _mixer_init


def main() -> int:
    """ main entry """

    _mixer_init()
    _music.load("C:\\Users\\hsalo\\Downloads\\Irving_Berlin_Always.mid")
    _music.play()

    root = Tk()
    root.mainloop()
    return 0


if __name__ == '__main__':
    _exit(main())
