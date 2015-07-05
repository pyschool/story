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

    def __init__(self, workshop):
        self.workshop = workshop
        self.padding_y = 2
        self.padding_x = 3

        # GUI canvas initialization.
        self.screen = curses.initscr()
        self.screen.keypad(True)

        curses.noecho()
        curses.start_color()

        # Color definitions.
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def show(self):
        position = 0

        # Exercises.
        for problem in self.problems:
            item = ProblemItem(self, problem, position)
            self.items.append(item)
            self.actionable_items.append(item)

            position += 1   # Position of the current item in the menu.
            self.actionable_count += 1  # Number of actionable items.

        default_items = [
            HelpItem(self, position),
            ExitItem(self, position + 1),
        ]

        for item in default_items:
            self.items.append(item)
            self.actionable_items.append(item)
            self.actionable_count += 1


        while (self.running):
            self.render_items()
            self.handle_key_press()

        curses.endwin()

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
        self.selected_item.set_style(curses.A_NORMAL)

        self.selected_index -= 1

        if (self.selected_index < 0):
            self.selected_index = len(self.actionable_items) - 1

        # Highlight the just selected item.
        self.selected_item.set_style(curses.color_pair(1))

    def select_next(self):
        # Unhighlight the previous selection.
        self.selected_item.set_style(curses.A_NORMAL)

        self.selected_index += 1

        if (self.selected_index >= self.actionable_count):
            self.selected_index = 0

        # Highlight the just selected item.
        self.selected_item.set_style(curses.color_pair(1))

    def render_items(self):
        self.screen.clear()
        self.screen.border(0)

        for item in self.items:
            item.render()

    def exit(self):
        self.running = False

    @property
    def problems(self):
        return self.workshop.problems

    @property
    def selected_item(self):
        return self.actionable_items[self.selected_index]


class Item(object):

    selectable = True
    style = curses.A_NORMAL

    def __init__(self, menu, text, position):
        self.menu = menu
        self.text = text
        self.position = position

    @property
    def completed(self):
        return False

    def set_style(self, style):
        self.style = style

    def select(self):
        raise NotImplemented

    def render(self):
        self.menu.screen.addstr(
            self.position + self.menu.padding_y,
            self.menu.padding_x,
            self.text.upper(),
            self.style
        )


class LineItem(Item):

    selectable = False


class TextItem(Item):

    selectable = False


class CommandItem(Item):

    def select(self):
        pass


class ProblemItem(Item):

    def __init__(self, menu, problem, position):
        self.problem = problem
        super().__init__(menu, problem.title, position)

    def select(self):
        pass

    @property
    def completed(self):
        return self.problem.completed


class HelpItem(CommandItem):
    command = 'help'

    def __init__(self, menu, position):
        super().__init__(menu, 'Help', position)


class ExitItem(Item):

    def __init__(self, menu, position):
        super().__init__(menu, 'Exit', position)

    def select(self):
        self.menu.exit()
