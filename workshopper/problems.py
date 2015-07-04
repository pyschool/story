import codecs
import inspect
import os


class BaseProblem(object):

    title = None
    files = [
        '{name}.{language}.rst',
        '{name}.{language}.md',
        '{name}.rst',
        '{name}.md',
    ]

    def __init__(self, manager):
        self.manager = manager

    @property
    def name(self):
        return self.__class__.__module__.split('.')[-1]

    @property
    def completed(self):
        return self.name in self.manager.completed

    def get_path(self, file):
        return os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            file)

    @property
    def problem(self):
        for file in self.files:
            file = self.get_path(
                file.format(name='README', language=self.manager.language))
            if os.path.exists(file):
                with codecs.open(file, encoding='utf-8') as f:
                    return f.read()
        raise Exception('Problem file not found')

    @property
    def solution(self):
        for file in self.files:
            file = self.get_path(
                file.format(name='SOLUTION', language=self.manager.language))
            if os.path.exists(file):
                with codecs.open(file, encoding='utf-8') as f:
                    return f.read()
        raise Exception('Solution file not found')

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


class ProblemManager(object):

    problems = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        problems = []
        for problem_module in self.problems:
            problem = problem_module.Problem(self)
            problems.append(problem)
        self.problems = problems

    def get_problem(self, name):
        for problem in self.problems:
            if problem.name == name:
                return problem
        return None
