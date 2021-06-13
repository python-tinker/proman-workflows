# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide CLI for git-tools.'''

from argufy import Parser

from .cli import hooks, setup, submodule, message


def main():
    ''' CLI.'''
    parser = Parser(command_type='subcommand')
    parser.add_commands(hooks)
    parser.add_commands(setup)
    parser.add_commands(submodule)
    parser.add_commands(message)
    hooks.test = 'test'
    parser.dispatch()


if __name__ == '__main__':
    main()