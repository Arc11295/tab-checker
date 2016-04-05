from types import IntType

class Song(object):

    def __init__(self):
        self._notes = []

    def add_note(self, note):
        assert type(note) is Note
        self._notes.append(note)


class Note(object):

    def __init__(self, fret, string, duration):
        assert type(fret) is IntType
        assert type(string) is IntType
        self._data = (fret, string, duration)

    def get_fret(self):
        return self._data[0]

    def get_string(self):
        return self._data[1]

    def get_duration(self):
        return self._data[2]
