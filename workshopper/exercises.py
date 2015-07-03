class Exercise(object):

    title = None

    def __init__(self, workshop):
        self.workshop = workshop

    @property
    def name(self):
        # TODO: Get from file
        return ''
