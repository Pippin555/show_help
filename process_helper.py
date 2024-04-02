#! python3.12
# coding: utf8

""" connect to the server using sockets """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2024-2024 all rights reserved'

from sys import exit as _exit

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


def check_and_start_process(proc_name:str, proc_exe:str) -> bool:
    """ try to find a process, else start it """

    for process in psutil.process_iter():
        if process.name() == proc_name:
            print(f'Process is running {process_name}')
            return True

    try:
        subprocess.Popen(proc_exe)
        print(f"Started {proc_name}")
        return True
    except FileNotFoundError:
        print(f"Process {proc_name} not found.")
        return False


if __name__ == '__main__':
    # main entry
    # all_processes()

    process_name = 'help_server.exe'
    process_exe = 'C:\\Users\\hsalo\\source\\repos\\Philip\\show_help\\help_server.exe'
    check_and_start_process(process_name, process_exe)