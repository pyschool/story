class Exercise(object):

    name = None
    title = None

    def __init__(self, workshop):
        self.workshop = workshop

    def get_name(self):
        return self.name

    def get_title(self):
        return self.title
