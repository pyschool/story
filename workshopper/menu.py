class Menu(object):

    def __init__(self, workshop):
        self.workshop = workshop

    def show(self):
        # TODO: draw menu
        for problem in self.workshop.problems:
            # problem.name and problem.title
            pass
        print('Drawing menu....')


class Item(object):

    selectable = True

    def __init__(self, menu):
        self.menu = menu

    @property
    def completed(self):
        return False

    def select(self):
        raise NotImplemented


class LineItem(Item):

    selectable = False


class TextItem(Item):

    selectable = False


class CommandItem(Item):

    def select(self):
        pass


class ProblemItem(Item):

    def __init__(self, menu, problem):
        self.problem = problem
        super().__init__(menu)

    def select(self):
        pass

    @property
    def completed(self):
        return self.problem.completed
