class Menu(object):

    pass


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


class ExerciseItem(Item):

    def __init__(self, menu, exercise):
        self.exercise = exercise
        super().__init__(menu)

    def select(self):
        pass

    @property
    def completed(self):
        return self.exercise.completed
