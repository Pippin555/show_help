#! python3.11
# coding: utf-8

""" install help in ~/.pianoscript/docs/help """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from sys import exit as _exit
from sys import argv

from os import walk
from os import curdir
from os import mkdir
from os import remove

from os.path import join
from os.path import splitext
from os.path import basename
from os.path import expanduser
from os.path import abspath
from os.path import isdir
from os.path import isfile
from os.path import dirname

from shutil import copy as _copy


def this() -> str:
    """ basename of this script """

    name, _ = splitext(basename(__file__))
    return name


def make_dir(target: str):
    """ make a directory with subdirectories """

    folders = []
    while not isdir(target):
        folders.insert(0, target)
        target = dirname(target)

    for target in folders:
        print(f'makedir {target}')
        mkdir(target)


def main() -> int:
    """ main entry """

    it_args = iter(argv[1:])
    source = abspath(next(it_args, join(curdir, 'help')))

    if not isdir(source):
        print(f'source folder not found: {source}')
        return 1

    user_help = expanduser('~/.pianoscript/docs/help')  # noqa
    target = abspath(user_help)

    if not isdir(target):
        make_dir(target)

    branch = len(source) + 1
    for root, _, files in walk(source):
        for file in files:
            source_file = join(root, file)
            print(f'source: {source_file}')

            leaf = source_file[branch:]
            target_file = join(target, leaf)

            make_dir(dirname(target_file))
            print(f'target: {target_file}')
            print('-----')

            if isfile(target_file):
               remove(target_file)

            _copy(source_file, target_file)

    return 0


if __name__ == '__main__':
    _exit(main())
