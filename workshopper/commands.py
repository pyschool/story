import argparse
import sys

from . import __version__
from .menu import Menu


class BaseCommand(object):

    name = None
    help = None

    def __init__(self, manager):
        self.manager = manager

    def create_parser(self, parser):
        pass

    def handle(self, args):
        raise NotImplementedError(
            'subclasses of BaseCommand must provide a handle() method')


class MenuCommand(BaseCommand):

    name = 'menu'

    def handle(self, args):
        Menu(self.manager).show()


class HelpCommand(BaseCommand):

    name = 'help'

    def handle(self, args):
        self.manager.parser.print_help()


class VerifyCommand(BaseCommand):

    name = 'verify'
    help = 'Verify the solution for the current problem.'

    def create_parser(self, parser):
        super().create_parser(parser)
        parser.add_argument('file')

    def handle(self, args):
        current = self.manager.current
        if current is None:
            sys.stderr.write('Please select a problem first.\n')
            sys.exit(1)
        problem = self.manager.get_problem(current)
        if not problem:
            sys.stderr.write('Invalid problem: {}.\n'.format(current))
            sys.exit(1)
        sys.exit(problem.verify(args.file))


class SelectCommand(BaseCommand):

    name = 'select'
    help = 'Select a problem by name.'

    def create_parser(self, parser):
        super().create_parser(parser)
        parser.add_argument('problem')

    def handle(self, args):
        self.manager.current = args.problem


class ListCommand(BaseCommand):

    name = 'list'
    help = 'List available problems.'

    def handle(self, args):
        for problem in self.manager.problems:
            sys.stdout.write('[{}] {}\n'.format(
                '*' if problem.completed else ' ',
                problem.name
            ))
        sys.exit(0)


class ShowCommand(BaseCommand):

    name = 'show'
    help = 'Show the problem.'

    def handle(self, args):
        current = self.manager.current
        if current is None:
            sys.stderr.write('Please select a problem first.\n')
            sys.exit(1)
        problem = self.manager.get_problem(current)
        if not problem:
            sys.stderr.write('Invalid problem: {}.\n'.format(current))
            sys.exit(1)
        sys.stdout.write(problem.highlighted_problem)


class SolutionCommand(BaseCommand):

    name = 'solution'
    help = 'Show the solution for a problem.'

    def handle(self, args):
        current = self.manager.current
        if current is None:
            sys.stderr.write('Please select a problem first.\n')
            sys.exit(1)
        problem = self.manager.get_problem(current)
        if not problem:
            sys.stderr.write('Invalid problem: {}.\n'.format(current))
            sys.exit(1)
        sys.stdout.write(problem.solution)


class ResetCommand(BaseCommand):

    name = 'reset'
    help = 'Clean workshop progress.'

    def handle(self, args):
        self.manager.data = {}


class VersionCommand(BaseCommand):

    name = 'version'

    def handle(self, args):
        return __version__


class CommandManager(object):

    parser = None
    languages = ('en',)
    default_language = 'en'
    commands = (
        MenuCommand,
        VerifyCommand,
        SelectCommand,
        ListCommand,
        ShowCommand,
        SolutionCommand,
        ResetCommand,
        HelpCommand,
    )
    default_command = MenuCommand.name
    version = __version__

    def __init__(self, argv=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.argv = argv or sys.argv[:]
        commands = []
        default_command = None
        for command_class in self.commands:
            command = command_class(self)
            if self.default_command == command_class.name:
                default_command = command
            commands.append(command)
        self.commands = commands
        self.default_command = default_command

    def create_parser(self):
        if self.parser is None:
            parser = argparse.ArgumentParser(
                description=self.description,
                add_help=True)
            parser.add_argument('-v', '--version',
                                action='version', version=self.get_version())
            parser.add_argument('-l', '--language', action='store')
            subparsers = parser.add_subparsers()
            for command in self.commands:
                subparser = subparsers.add_parser(
                    command.name, help=command.help)
                subparser.set_defaults(handle=command.handle)
                command.create_parser(subparser)
            self.parser = parser
        return self.parser

    def get_version(self):
        return self.version

    def execute(self):
        r = self.create_parser().parse_args(self.argv[1:])
        if r.language:
            self.language = r.language
        if not hasattr(r, 'handle'):
            self.default_command.handle(r)
        else:
            r.handle(r)

    @classmethod
    def run(cls):
        cls().execute()
