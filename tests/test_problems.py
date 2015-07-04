from workshopper.problems import BaseProblem


class ExampleProblem(BaseProblem):

    pass


def test_problem_name():
    assert ExampleProblem(None).name == 'test_problems'
