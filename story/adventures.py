import codecs
import inspect
import os

from .format import highlight
from .data import _


class BaseAdventure(object):

    files = [
        '{name}.{language}.rst',
        '{name}.rst',
    ]

    def __init__(self, manager):
        self.manager = manager

    @property
    def name(self):
        return self.__class__.__module__.split('.')[-1]

    @property
    def title(self):
        return self.name

    @property
    def completed(self):
        return self.name in self.manager.completed

    def get_path(self, file):
        return os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            file)

    @property
    def problem(self):
        problem = 'Adventure description not found.'
        for file in self.files:
            file = self.get_path(
                file.format(name='README', language=self.manager.language))
            if os.path.exists(file):
                with codecs.open(file, encoding='utf-8') as f:
                    problem = f.read()
                    break
        return problem.format(**self.get_context())

    @property
    def solution(self):
        for file in self.files:
            file = self.get_path(
                file.format(name='SOLUTION', language=self.manager.language))
            if os.path.exists(file):
                with codecs.open(file, encoding='utf-8') as f:
                    return f.read()
        raise Exception('Solution file not found')

    def get_context(self):
        return {
            'script': self.manager.name,
            'story_name': self.manager.name,
            'story_title': self.manager.title,
            'story_adventures': len(self.manager.adventures),
            'adventure_title': self.title,
            'adventure_position': self.manager.adventures.index(self) + 1,
        }

    @property
    def problem_formatted(self):
        context = self.get_context()
        context['adventure_problem'] = self.problem.format(**context)
        return highlight(problem_wrapper.format(**context))

    @property
    def solution_formatted(self):
        context = self.get_context()
        context['adventure_solution'] = self.solution.format(**context)
        return highlight(solution_wrapper.format(**context))

    def verify(self, file):
        try:
            self.test(file)
            self.manager.completed = self.name
            self.manager.current = None
            return 0
        except AssertionError:
            raise

    def test(self, file):
        pass


class AdventureManager(object):

    adventures = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        adventures = []
        for adventure_module in self.adventures:
            adventure = adventure_module.Adventure(self)
            adventures.append(adventure)
        self.adventures = adventures

    def get_adventure(self, name):
        for adventure in self.adventures:
            if adventure.name == name:
                return adventure
        return None


problem_wrapper = _('''
 
{story_title}: {adventure_title}
==============================================================================

{adventure_problem}

------------------------------------------------------------------------------

 » To print these instructions again, run: {script} print
 » To execute your program in a test environment, run: {script} run program.py
 » To verify your program, run: {script} verify program.py
 » For help run: {script} help
 
''')


solution_wrapper = _('''
 
{story_title}: {adventure_title} [SOLUTION]
==============================================================================

{adventure_solution}

------------------------------------------------------------------------------

 » To print these instructions again, run: {script} print
 » To execute your program in a test environment, run: {script} run program.py
 » To verify your program, run: {script} verify program.py
 » For help run: {script} help
 
''')
