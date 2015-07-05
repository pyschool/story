import curses


class Keys(object):
    ESCAPE = 27
    UP_ARROW = 259
    DOWN_ARROW = 258
    ENTER = 10


class Menu(object):
    running = True
    items = []
    actionable_items = []
    actionable_count = 0
    selected_index = 0
    padding_y = 2
    padding_x = 3
    x = 2
    y = 2
    width = 50

    def __init__(self, story):
        self.story = story

        # Screen initialization.
        self.screen = curses.initscr()
        self.screen.keypad(True)

        curses.noecho()
        curses.start_color()
        curses.curs_set(0)
        self.screen.refresh()

        # Colors definition.
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)

    @property
    def height(self):
        height = 0

        for item in self.items:
            height += item.size

        return height

    @property
    def adventures(self):
        return self.story.adventures

    @property
    def selected_item(self):
        return self.actionable_items[self.selected_index]

    def show(self):
        # Menu header.
        title = TextItem(self, self.story.title.upper(), 0)
        usage = TextItem(self, 'Select an exercise and hit ENTER to begin', 1)

        self.items.append(title)
        self.items.append(usage)
        self.items.append(LineItem(self, 2))

        title.set_style(curses.A_BOLD)

        position = 0

        for item in self.items:
            position += item.size

        # Exercises.
        for adventure in self.adventures:
            item = AdventureItem(self, adventure, position)
            self.items.append(item)
            self.actionable_items.append(item)

            position += 1   # Position of the current item in the menu.
            self.actionable_count += 1  # Number of actionable items.

        self.items.append(LineItem(self, position))

        default_items = [
            HelpItem(self, position + 2),
            ExitItem(self, position + 3),
        ]


        for item in default_items:
            self.items.append(item)
            self.actionable_items.append(item)
            self.actionable_count += 1


        while (self.running):
            self.render_items()
            self.handle_key_press()

    def handle_key_press(self):
        key = self.screen.getch()
        actions = {
            Keys.ESCAPE: self.exit,
            Keys.UP_ARROW: self.select_prev,
            Keys.DOWN_ARROW: self.select_next,
            Keys.ENTER: self.selected_item.select
        }

        selected_action = actions.get(key)

        if (selected_action):
           selected_action()

    def select_prev(self):
        # Unhighlight the previous selection.
        self.selected_item.set_style(self.selected_item.default_style)

        self.selected_index -= 1

        if (self.selected_index < 0):
            self.selected_index = len(self.actionable_items) - 1

        # Highlight the just selected item.
        self.selected_item.set_style(curses.color_pair(2))

    def select_next(self):
        # Unhighlight the previous selection.
        self.selected_item.set_style(self.selected_item.default_style)

        self.selected_index += 1

        if (self.selected_index >= self.actionable_count):
            self.selected_index = 0

        # Highlight the just selected item.
        self.selected_item.set_style(curses.color_pair(2))

    def render_items(self):
        # Menu container.
        self.container = curses.newwin(
            self.height + self.padding_y * 2,
            self.width + self.padding_x * 2,
            self.x,
            self.y,
        )
        self.container.bkgd(curses.color_pair(1))

        for item in self.items:
            item.render()

        self.container.refresh()

    def exit(self):
        if (self.running):
            curses.endwin()
        self.running = False


class Item(object):

    selectable = True
    style = curses.A_NORMAL
    default_style = curses.A_NORMAL
    size = 1

    def __init__(self, menu, text, position):
        self.menu = menu
        self.text = text.upper()
        self.position = position

    @property
    def completed(self):
        return False

    def set_style(self, style):
        self.style = style

    def select(self):
        raise NotImplemented

    def render(self):
        text = self.text + ' ' * (self.menu.width - len(self.text))

        self.menu.container.addstr(
            self.position + self.menu.padding_y,
            self.menu.padding_x,
            text,
            self.style
        )


class LineItem(Item):

    selectable = False
    style = curses.A_UNDERLINE
    size = 2

    def __init__(self, menu, position):
        self.menu = menu
        self.position = position
        self.text = ' ' * menu.width


class TextItem(Item):

    selectable = False

    def __init__(self, menu, text, position):
        super().__init__(menu, text, position)
        self.text = text


class CommandItem(Item):

    def __init__(self, menu, position):
        self.menu = menu
        self.position = position

    def select(self):
        pass


class AdventureItem(Item):

    def __init__(self, menu, adventure, position):
        self.adventure = adventure
        super().__init__(menu, '» ' + adventure.title, position)

    @property
    def completed(self):
        return self.adventure.completed

    def select(self):
        self.menu.exit()
        print(self.adventure.problem_formatted)


class HelpItem(CommandItem):

    text = 'HELP'
    default_style = curses.A_BOLD

    def select(self):
        self.menu.exit()

        from .commands import HelpCommand
        HelpCommand(self.menu.story).handle()


class ExitItem(Item):

    style = curses.A_BOLD
    default_style = curses.A_BOLD

    def __init__(self, menu, position):
        super().__init__(menu, 'Exit', position)

    def select(self):
        self.menu.exit()
