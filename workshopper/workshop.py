from .commands import MenuCommand, VerifyCommand, HelpCommand, ExitCommand


class Workshop(object):

    title = None
    languages = ['en']
    commands = [
        MenuCommand,
        VerifyCommand,
        HelpCommand,
        ExitCommand,
    ]
    default_command = MenuCommand.name
