"""
Handles the Main Menu of the story
"""
import curses.panel
import os
import locale


from .translation import gettext as _, LANGUAGES

SPACE = ' '


class Keys():

    ESCAPE = 27
    UP_ARROW = 259
    DOWN_ARROW = 258
    J = 106
    K = 107
    Q = 113
    ENTER = 10


class Level(list):

    padding_x = 2
    padding_y = 1
    x = 1
    y = 1
    width = 74

    def __init__(self, menu):
        self.menu = menu
        self.window = None
        self.panel = None

    @property
    def height(self):
        return sum([item.size for item in self])

    @property
    def selectables(self):
        return filter(lambda i: i.selectable, self)

    @property
    def selected(self):
        return next(filter(lambda i: i.selected, self.selectables))

    def reset(self):
        first = True
        for item in self.selectables:
            item.selected = False
            if first:
                item.selected = True
                first = False

    def previous(self):
        current_item = self.selected
        current_item.selected = False

        previous_item = None
        for item in self.selectables:
            if item == current_item and previous_item:
                break
            previous_item = item
        previous_item.selected = True

    def next(self):
        current_item = self.selected
        current_item.selected = False

        first_item = None
        previous_item = None
        for item in self.selectables:
            if first_item is None:
                first_item = item
            if previous_item == current_item:
                break
            previous_item = item
        if previous_item == item:
            item = first_item
        item.selected = True

    def ensure_ui(self):
        if self.window is None:
            self.window = curses.newwin(
                self.height + self.padding_y * 2,
                self.width + self.padding_x * 2,
                self.y,
                self.x
            )
            self.window.keypad(1)
            self.window.bkgd(' ', curses.color_pair(1))
        if self.panel is None:
            self.panel = curses.panel.new_panel(self.window)
            self.panel.hide()

    def render(self):
        self.ensure_ui()

        position = 0
        for item in self:
            item.render(
                self.window,
                self.padding_x,
                self.padding_y + position,
                self.width
            )
            position += item.size

        curses.doupdate()

    def wait(self):
        {
            Keys.ESCAPE: lambda: self.menu.exit(),
            Keys.UP_ARROW: lambda: self.previous(),
            Keys.K: lambda: self.previous(),
            Keys.DOWN_ARROW: lambda: self.next(),
            Keys.J: lambda: self.next(),
            Keys.ENTER: lambda: self.selected.action(),
            Keys.Q: lambda: self.menu.exit()
        }.get(self.window.getch(), lambda: None)()

    def show(self):
        self.ensure_ui()
        self.panel.show()
        curses.panel.update_panels()

    def hide(self):
        self.ensure_ui()
        self.panel.hide()
        curses.panel.update_panels()


class Menu():

    running = True
    levels = []

    def __init__(self, story):
        self.story = story
        self.screen = None

    def get_initial(self):
        level = Level(self)
        level.extend([
            TitleItem(self, self.story.title),
            TextItem(self, _('Select an exercise and hit ENTER to begin')),
            LineItem(self),
            SpaceItem(self)
        ])

        for adventure in self.story.adventures:
            level.append(AdventureItem(self, adventure))

        level.extend([
            LineItem(self),
            SpaceItem(self),
            HelpItem(self),
            ChooseLanguageItem(self),
            ExitItem(self)
        ])
        level.reset()
        return level

    @property
    def active(self):
        return self.levels[-1]

    def push(self, new):
        if self.levels:
            self.active.hide()
        self.levels.append(new)
        new.show()

    def pop(self):
        old = self.levels.pop()
        old.hide()
        self.active.show()
        return old

    def show(self):
        self.running = True
        if os.environ.get('TMUX'):
            os.environ['TERM'] = 'screen'
        curses.wrapper(self.display)

    def display(self, screen):
        self.screen = screen
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)

        self.push(self.get_initial())

        while (self.running):
            self.active.render()
            self.active.wait()

        curses.doupdate()

    def back(self):
        self.pop()

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

    @staticmethod
    def lr_justify(left, right, width):
        return '{}{}{}' \
            .format(left, ' '*(width-len(left+right)), right)[:width]

    def render(self, window, x, y, width):
        # FIXME: We need to cast get_text to str because of lazy()
        text = str(self.get_text(width)).ljust(width)

        window.addstr(y, x, text, self.style)


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

    def action(self):
        raise NotImplementedError


class CommandItem(SelectableMixin, TextItem):

    pass


class AdventureItem(SelectableMixin, TextItem):

    def __init__(self, menu, adventure):
        super().__init__(menu)
        self.adventure = adventure

    def get_text(self, width):
        left_text = '» ' + super().get_text(width).rstrip()
        if self.completed:
            return self.lr_justify(left_text, '[%s]' % _('COMPLETED'), width)
        else:
            return left_text[:width]

    @property
    def completed(self):
        return self.adventure.completed

    @property
    def text(self):
        return self.adventure.title

    def action(self):
        self.menu.exit()
        self.menu.story.set_current(self.adventure.name)
        print(self.adventure.problem_formatted)


class ChooseLanguageItem(SelectableMixin, TextItem):

    text = _('Choose language')

    def __init__(self, menu):
        super().__init__(menu)

        self.level = Level(menu)
        self.level.extend([
            TitleItem(menu, menu.story.title),
            TextItem(menu, _('Choose a language:')),
            LineItem(menu),
            SpaceItem(menu),
        ])
        for code, name in LANGUAGES:
            self.level.append(LanguageItem(self.menu, code, name))
        self.level.extend([
            LineItem(menu),
            SpaceItem(menu),
            BackItem(menu),
            ExitItem(menu)
        ])
        self.level.reset()

    def action(self):
        self.menu.push(self.level)


class LanguageItem(SelectableMixin, TextItem):

    def __init__(self, menu, code, name):
        super().__init__(menu)
        self.code = code
        self.name = name

    def get_text(self, width):
        left_text = '» ' + super().get_text(width).rstrip()
        if self.menu.story.language == self.code:
            return self.lr_justify(left_text, '[%s]' % _('CURRENT'), width)
        else:
            return left_text[:width]

    @property
    def text(self):
        return self.name

    def action(self):
        self.menu.story.language = self.code
        self.menu.back()


class HelpItem(CommandItem):

    text = _('Help')

    def action(self):
        self.menu.exit()

        from .commands import HelpCommand
        HelpCommand(self.menu.story).handle()


class BackItem(CommandItem):

    text = _('Cancel')

    def action(self):
        self.menu.back()


class ExitItem(CommandItem):

    text = _('Exit')

    def action(self):
        self.menu.exit()
