from __future__ import print_function

try:
    import readline
except ImportError:
    pass

import argparse
import sys
from aiclass import search, network, naive, plan, propositional as propos


COMMANDS = [
    search.SearchCommand,
    network.NetworkCommand,
    naive.NaiveCommand,
    plan.PlanCommand,
    propos.ProposCommand ]


def get_command_from_args(argv=None):
    parser = argparse.ArgumentParser(prog='aiclass')
    subparsers = parser.add_subparsers(title='available commands', dest='command')

    cmds = {}

    for cmd in COMMANDS:
        subparser = subparsers.add_parser(
            cmd.name,
            description = cmd.description,
            help = cmd.help)

        cmd.configure_parser(subparser)
        cmds[cmd.name] = cmd

    args = parser.parse_args(argv)

    return cmds[args.command].create_from_args(args)


def main():
    command = get_command_from_args()
    command.loop()
    print('quit')


    
if __name__ == '__main__':
    main()


