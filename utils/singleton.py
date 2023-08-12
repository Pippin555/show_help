#! python3.11
# coding: utf8

""" Singleton metaclass """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2021-2023 all rights reserved'


class Singleton(type):
    """ metaclass for Singleton """
    _instances = {}  # a dictionary containing all instances

    def __call__(cls, *args, **kwargs):
        """ this is run when created """

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
