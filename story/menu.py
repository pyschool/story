class Menu(object):

    def __init__(self, story):
        self.story = story

    def show(self):
        # TODO: draw menu
        for adventure in self.story.adventures:
            # adventure.name and adventure.title
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


class AdventureItem(Item):

    def __init__(self, menu, adventure):
        self.adventure = adventure
        super().__init__(menu)

    def select(self):
        pass

    @property
    def completed(self):
        return self.adventure.completed
