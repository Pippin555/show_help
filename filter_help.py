#! python3.11
# coding: utf-8

""" display the help file of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa


from sys import argv
from sys import exit as _exit

from os import mkdir
from os import walk
from os import remove
from os import rmdir

from os.path import dirname
from os.path import isdir
from os.path import join
from os.path import splitext
from os.path import abspath
from os.path import sep as _sep

from re import compile as _compile

from shutil import copy as _copy

_PATT = _compile('<p class="rvps5" .*</p>')


def main() -> int:
    """ main function """

    source_path = None
    target_path = None

    iarg = iter(argv[1:])
    for arg in iarg:
        match arg:
            case '-s':
                source_path = abspath(next(iarg))
            case '-t':
                target_path = abspath(next(iarg))

    assert source_path
    assert target_path

    script_path = dirname(__file__)
    _create_dir(target_path)
    _clean_dir(target_path)

    for root, paths, files in walk(source_path):
        for file in files:
            source_file = join(root, file)
            source_base = _relative_path(source_path, source_file)
            target_file = join(target_path, source_base)
            _create_dir(dirname(target_file))

            _, ext = splitext(target_file)
            if ext.lower() == '.html':
                _filter(source_file, target_file)
            else:
                _copy(source_file, target_file)

    return 0


def _relative_path(root_path: str, file_path: str) -> str:
    """ get the path relative to the root """
    root_branches = root_path.split(_sep)
    file_branches = file_path.split(_sep)

    index_root = len(root_branches)
    result = join(*file_branches[index_root:])
    return result


def _create_dir(path: str):
    """ create directory and sub directories """

    if isdir(path):
        return

    # list folders, bottoms up
    folders = []
    while not isdir(path):
        folders.insert(0, path)
        path = dirname(path)

    # create directories, top down
    for folder in folders:
        mkdir(folder)


def _clean_dir(top_path: str) -> None:
    """ remove all files from this path """

    for root, _, files in walk(top_path):
        for file in files:
            fullname = join(root, file)
            remove(fullname)

    folders = []
    for root, paths, _ in walk(top_path):
        for path in paths:
            folders.append(join(root, path))

    folders = sorted(folders, reverse=True)
    for folder in folders:
        rmdir(folder)


def _filter(source: str, target: str):
    """ take away the nagging advertisement """

    with open(file=target, mode='w', encoding='utf8') as out:
        with open(file=source, mode='r', encoding='utf8') as inp:
            contents = inp.read()
            mat = _PATT.search(contents)
            if mat:
                start, finish = mat.regs[0]
                contents = contents[:start] + contents[finish:]
                out.write(contents)


if __name__ == '__main__':
    _exit(main())
