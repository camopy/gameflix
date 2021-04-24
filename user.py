class User:
    def __init__(self, id, name, password):
        self._id = id
        self._name = name
        self._password = password

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password