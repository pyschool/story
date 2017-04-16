import curses
import os

from .data import _


SPACE = ' '


class Keys(object):

    ESCAPE = 27
    UP_ARROW = 259
    DOWN_ARROW = 258
    J = 106
    K = 107
    Q = 113
    ENTER = 10


class Menu(object):

    running = True
    padding_x = 2
    padding_y = 1
    x = 1
    y = 1
    width = 74

    def __init__(self, story):
        self.story = story

        items = [
            TitleItem(self, story.title),
            TextItem(self, _('Select an exercise and hit ENTER to begin')),
            LineItem(self),
            SpaceItem(self)
        ]

        for adventure in story.adventures:
            items.append(AdventureItem(self, adventure))

        items += [
            LineItem(self),
            SpaceItem(self),
            HelpItem(self),
            ExitItem(self),
        ]

        next(filter(lambda i: i.selectable, items)).selected = True
        self.items = items

    @property
    def height(self):
        return sum([item.size for item in self.items])

    @property
    def selectable_items(self):
        return filter(lambda i: i.selectable, self.items)

    @property
    def selected_item(self):
        return next(filter(lambda i: i.selected, self.selectable_items))

    def show(self):
        self.running = True
        if os.environ.get('TMUX'):
            os.environ['TERM'] = 'screen'
        curses.wrapper(self.display)

    def display(self, screen):
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        window = screen.subwin(
            sum([item.size for item in self.items]) + self.padding_y * 2,
            self.width + self.padding_x * 2,
            self.y,
            self.x
        )
        window.keypad(1)
        window.clear()

        # Colors definition.
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)

        window.bkgd(' ', curses.color_pair(1))

        while (self.running):
            # Render
            position = 0
            for item in self.items:
                item.render(
                    window,
                    self.padding_x,
                    self.padding_y + position,
                    self.width
                )
                position += item.size

            curses.doupdate()

            # Key
            key = window.getch()
            actions = {
                Keys.ESCAPE: self.exit,
                Keys.UP_ARROW: self.select_previous,
                Keys.K: self.select_previous,
                Keys.DOWN_ARROW: self.select_next,
                Keys.J: self.select_next,
                Keys.ENTER: self.selected_item.execute,
                Keys.Q: self.exit
            }
            selected_action = actions.get(key)
            if (selected_action):
                selected_action()

        window.clear()
        curses.doupdate()

    def select_previous(self):
        current_item = self.selected_item
        current_item.selected = False

        previous_item = None
        for item in self.selectable_items:
            if item == current_item and previous_item:
                break
            previous_item = item
        previous_item.selected = True

    def select_next(self):
        current_item = self.selected_item
        current_item.selected = False

        first_item = None
        previous_item = None
        for item in self.selectable_items:
            if first_item is None:
                first_item = item
            if previous_item == current_item:
                break
            previous_item = item
        if previous_item == item:
            item = first_item
        item.selected = True

    def exit(self):
        if self.running:
            curses.endwin()
        self.running = False


class Item(object):

    selectable = False
    size = 1

    def __init__(self, menu):
        self.menu = menu

    @property
    def style(self):
        return curses.color_pair(1)

    def render(self, window, x, y, width):
        raise NotImplementedError


class SpaceItem(Item):

    def render(self, *args, **kwargs):
        pass


class TextItem(Item):

    def __init__(self, menu, text=None):
        super().__init__(menu)
        if text:
            self.text = text

    def get_text(self, width):
        return self.text

    def render(self, window, x, y, width):
        window.addstr(y, x, self.get_text(width), self.style)


class LineItem(TextItem):

    def get_text(self, width):
        return width * '_'


class TitleItem(TextItem):

    def get_text(self, width):
        return super().get_text(width).upper()

    @property
    def style(self):
        return curses.A_BOLD | super().style


class SelectableMixin(object):

    selectable = True
    selected = False

    def get_text(self, width):
        text = super().get_text(width).upper()
        text = text[:width]
        text += (width - len(text)) * SPACE
        return text

    @property
    def style(self):
        if self.selected:
            return curses.color_pair(2)
        return curses.color_pair(1)

    def execute(self):
        raise NotImplementedError


class CommandItem(SelectableMixin, TextItem):

    pass


class AdventureItem(SelectableMixin, TextItem):

    def __init__(self, menu, adventure):
        super().__init__(menu)
        self.adventure = adventure

    def get_text(self, width):
        text = '» ' + super().get_text(width)
        text = text[:width]
        if self.completed:
            text = text[:width - 11] + '[COMPLETED]'
        return text

    @property
    def completed(self):
        return self.adventure.completed

    @property
    def text(self):
        return self.adventure.title

    def execute(self):
        self.menu.exit()
        self.menu.story.set_current(self.adventure.name)
        print(self.adventure.problem_formatted)


class HelpItem(CommandItem):

    text = _('Help')

    def execute(self):
        self.menu.exit()

        from .commands import HelpCommand
        HelpCommand(self.menu.story).handle()


class ExitItem(CommandItem):

    text = _('Exit')

    def execute(self):
        self.menu.exit()
