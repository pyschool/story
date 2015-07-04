from workshopper.problems import BaseProblem


class ExampleProblem(BaseProblem):

    pass


def test_problem_name():
    print(ExampleProblem(None).name)
    assert 0 == 0
