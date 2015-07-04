from .commands import CommandManager
from .data import DataManager
from .problems import ProblemManager


class BaseWorkshop(ProblemManager, DataManager, CommandManager):

    title = None
    name = None
    description = None
