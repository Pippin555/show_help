#! python3.11
# coding: utf8

""" Singleton metaclass """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2023-2023 all rights reserved'

from sys import argv
from sys import exit as _exit

from utils.config import Config


class ExampleConfig(Config):
    """ the derived configuration for example.py
        this creates a file in a folder with the
        name example and  name example.json in it
        (this name of __file__).

        The location of the folder depends on the
        platform. For Windows this is:
        %APPDATA%/python_data/example/example.json
        APPDATA is an environment variable that points
        to the user's roaming folder:
        C:/Users/<Username>/AppData/Roaming
        For MAC or Linux, te system default paths
        are used, see file config.py function
        get_config_name()
        for unknown systems, a folder with the same
        name as the executable and a file with the name
        of the executable, with extension .json is used
    """


def init_config():
    """ initialize the configuration """

    # initialize the value in the config
    value = {'index': 0}

    # store the value in the configuration class
    # the value above is overwritten by the value
    # in the configuration file
    _ = ExampleConfig(main=__file__, value=value)

    # ExampleConfig() can be created anywhere in the
    # application, it all uses the only instance
    # that is created and stored in the Singleton class
    #
    # do not forget to save ExampleConfig on exit
    #
    # see also the alternate way to use and savef
    # the configuration


def use_config() -> int:
    """ get the value from the configuration """

    conf = ExampleConfig()
    value = conf.value
    value['index'] += 1
    print(f'the index is {value["index"]}')


    return 0


def save_config() -> int:
    """ save the configuration """

    ExampleConfig().save()


def normal_main() -> int:
    """ main entry """

    init_config()
    use_config()
    save_config()

    return 0


def alternative_main() -> int:
    """ alternative main entry """

    # initialize the value in the config
    value = {'index': 0}

    # store the value in the configuration class
    with ExampleConfig(main=__file__, value=value) as _:
        use_config()

    # the 'with' clause causes the Config.__entry__() to be called
    # when 'with' ix exited the Config.__exit__(...) is called
    # the __exit__(...) contains the .save() function
    return 0


def main() -> int:
    """ three main function modes """

    mode = 'normal'
    for arg in argv[1:]:
        match arg:
            case '-n':
                mode = 'normal'
            case '-a':
                mode = 'alter'
            case '-c':
                mode = 'clear'

    ret_code = -1
    match mode:
        case 'normal':
            ret_code = normal_main()

        case 'clear':
            # note: clear() is a static function
            ExampleConfig.clear(main=__file__)
            ret_code = 0

        case 'alter':
            ret_code = alternative_main()

    return ret_code


if __name__ == '__main__':
    _exit(main())
