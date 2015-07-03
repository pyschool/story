class Command(object):

    def __init__(self, workshop):
        self.workshop = workshop

    def handle(self, *args, **kwargs):
        pass


class MenuCommand(Command):

    name = 'menu'


class HelpCommand(Command):

    name = 'help'


class VerifyCommand(Command):

    name = 'help'


class ExitCommand(Command):

    name = 'help'
