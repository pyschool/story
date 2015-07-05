from story.adventure import BaseAdventure


class ExampleAdventure(BaseAdventure):

    pass


def test_adventure_name():
    assert ExampleAdventure(None).name == 'test_adventures'
