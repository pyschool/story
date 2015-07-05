import pytest

from story import __version__
from story.commands import BaseCommand, CommandManager, VerifyCommand


class TestCommandManager(object):

    def test_version(self):
        assert CommandManager().get_version() == __version__


class TestBaseCommand(object):

    def test_handle(self):
        with pytest.raises(NotImplementedError):
            BaseCommand(None).handle(None)


class TestVerifyCommand(object):

    def test_create_parser(self, monkeypatch):
        command = VerifyCommand(CommandManager())

        class Parser():
            def add_argument(self, argument):
                assert argument == 'file'

        command.create_parser(Parser())
