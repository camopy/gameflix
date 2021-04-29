class Game:
    def __init__(self, name, category, console, id=None):
        self._id = id
        self._name = name
        self._category = category
        self._console = console

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def console(self):
        return self._console

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, generated_id):
        self._id = generated_id