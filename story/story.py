from .commands import CommandManager
from .data import DataManager
from .adventures import AdventureManager


class BaseStory(AdventureManager, DataManager, CommandManager):

    name = None

    @property
    def title(self):
        return self.name

    @property
    def description(self):
        return self.name
