import argparse
import sys

from . import __version__
from .menu import Menu
from .data import _


class BaseCommand(object):

    name = None
    help = None

    def __init__(self, manager):
        self.manager = manager

    def create_parser(self, parser):
        pass

    def handle(self, args):
        raise NotImplementedError(
            'Subclasses of BaseCommand must provide a handle() method')


class MenuCommand(BaseCommand):

    name = 'menu'
    help = _('Show a menu to interactively select an adventure.')

    def handle(self, args):
        Menu(self.manager).show()


class ListCommand(BaseCommand):

    name = 'list'
    help = _('Show a newline-separated list of all the adventures.')

    def handle(self, args):
        for adventure in self.manager.adventures:
            sys.stdout.write('[{}] {}\n'.format(
                '*' if adventure.completed else ' ',
                adventure.name
            ))
        sys.exit(0)


class SelectCommand(BaseCommand):

    name = 'select'
    help = _('Select an adventure.')

    def create_parser(self, parser):
        super().create_parser(parser)
        parser.add_argument('name')

    def handle(self, args):
        self.manager.current = args.name


class CurrentCommand(BaseCommand):

    name = 'current'
    help = _('Show the currently selected adventure.')

    def handle(self, args):
        current = self.manager.current
        if current is None:
            sys.stderr.write(_('Please select an adventure first.\n'))
            sys.exit(1)
        adventure = self.manager.get_adventure(current)
        if not adventure:
            sys.stderr.write(_('Invalid adventure: {}.\n').format(current))
            sys.exit(1)
        sys.stdout.write('{}\n'.format(adventure.name))
        sys.exit(0)


class PrintCommand(BaseCommand):

    name = 'print'
    help = _('Print the adventure.')

    def handle(self, args):
        current = self.manager.current
        if current is None:
            sys.stderr.write(_('Please select an adventure first.\n'))
            sys.exit(1)
        adventure = self.manager.get_adventure(current)
        if not adventure:
            sys.stderr.write(_('Invalid adventure: {}.\n').format(current))
            sys.exit(1)
        sys.stdout.write(adventure.problem_formatted)


class NextCommand(BaseCommand):

    name = 'next'
    help = _('Print the instructions for the next incomplete adventure '
             'after the currently selected adventure.')

    def handle(self, args):
        sys.stdout.write(_('Not implemented.\n'))


class ResetCommand(BaseCommand):

    name = 'reset'
    help = _('Reset completed adventure progress.')

    def handle(self, args):
        self.manager.data = {}


class RunCommand(BaseCommand):

    name = 'run'
    help = _('Run your program against the selected input.')

    def handle(self, args):
        sys.stdout.write(_('Not implemented.\n'))


class VerifyCommand(BaseCommand):

    name = 'verify'
    help = _('Verify the solution for the current adventure.')

    def create_parser(self, parser):
        super().create_parser(parser)
        parser.add_argument('file')

    def handle(self, args):
        current = self.manager.current
        if current is None:
            sys.stderr.write(_('Please select an adventure first.\n'))
            sys.exit(1)
        adventure = self.manager.get_adventure(current)
        if not adventure:
            sys.stderr.write(_('Invalid adventure: {}.\n').format(current))
            sys.exit(1)
        sys.exit(adventure.verify(args.file))


class SolutionCommand(BaseCommand):

    name = 'solution'
    help = _('Print the solution for an adventure.')

    def handle(self, args):
        current = self.manager.current
        if current is None:
            sys.stderr.write(_('Please select an adventure first.\n'))
            sys.exit(1)
        adventure = self.manager.get_adventure(current)
        if not adventure:
            sys.stderr.write(_('Invalid adventure: {}.\n').format(current))
            sys.exit(1)
        sys.stdout.write(adventure.solution_formatted)


class HelpCommand(BaseCommand):

    name = 'help'

    def handle(self, *args):
        self.manager.parser.print_help()


class CommandManager(object):

    parser = None
    languages = ('en',)
    default_language = 'en'
    commands = (
        MenuCommand,
        ListCommand,
        SelectCommand,
        CurrentCommand,
        PrintCommand,
        NextCommand,
        ResetCommand,
        RunCommand,
        VerifyCommand,
        SolutionCommand,
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
            parser.add_argument(
                '-v', '--version', action='version',
                version=self.get_version())
            parser.add_argument(
                '-l', '--language', action='store',
                help=_('Change the system to the specified language.'))
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
    def begin(cls):
        cls().execute()
