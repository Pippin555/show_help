#! python3.12
# coding: utf8

""" list all processes or run help_server """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2024-2024 all rights reserved'

from sys import exit as _exit
from sys import argv

import psutil

import subprocess


def all_processes() -> None:
    """ list all processes """

    all_proc = {}
    for process in psutil.process_iter():
        name = process.name()
        if name not in all_proc:
            all_proc[name] = process

    keys = [key for key in all_proc.keys()]
    keys.sort()
    for key in keys:
        print(key)


def check_and_start_process(proc_name: str, proc_exe: str) -> bool:
    """ try to find a process, else start it """

    for process in psutil.process_iter():
        if process.name() == proc_name:
            # print(f'Process is running {proc_name}')
            return True

    try:
        process = subprocess.Popen(proc_exe)
        # print(f"Started {proc_name} and running when poll() returns None")
        return process.poll() is None

    except FileNotFoundError:
        print(f"Process {proc_name} no started")
        return False


def main() -> int:
    """ either list all processes or start help_server """

    for arg in argv[1:]:
        if arg == '-l':
            all_processes()
            return 0

    process_name = 'help_server.exe'
    process_exe = 'C:\\Users\\hsalo\\source\\repos\\Philip\\show_help\\help_server.exe'
    check_and_start_process(process_name, process_exe)
    return 0


if __name__ == '__main__':
    # main entry

    _exit(main())