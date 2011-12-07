from __future__ import print_function

import sys
import argparse

if (sys.version_info > (3,0)):
    raw_input = input
import traceback


class BaseCommand(object):
    name = None
    description = None
    help = None

    @classmethod
    def get_data(cls, location):
        import aiclass.data
        if location.startswith('data:'):
            return getattr(aiclass.data, location[5:].upper().replace('-', '_')+'_DATA')

        with open(location, 'r') as f:
            return f.read()
    
    @classmethod
    def configure_parser(cls, parser):
        pass
    
    @classmethod
    def create_from_args(cls, args):
        return cls()

    def call(self, string):
        raise NotImplementedError

    def loop(self):
        while True:
            string = raw_input('>>> ')
            try:
                print(self.call(string))
            except Exception:
                traceback.print_exception(*sys.exc_info())


def get_command_from_args(argv=None):
    from aiclass import search, network, naive, plan, propositional

    COMMANDS = [
        search.SearchCommand,
        network.NetworkCommand,
        naive.NaiveCommand,
        plan.PlanCommand,
        propositional.ProposCommand ]

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



