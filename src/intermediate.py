from types import IntType

class Song(object):

    _C_2 = 48
    # Just trust me on this one, ok? It has to do with MIDI numbers and
    # the fact that LilyPond takes plain note names to mean notes in
    # the octave BELOW middle C, so we need some constant, and MIDI
    # numbers were a convenient choice.

    lilypond_notes = \
        ("c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b")


    def __init__(self, tab=True, midi=False, standard=False):
        self._notes = []
        self._tuning = (64, 59, 55, 50, 45, 40)
        self._midi = midi
        self._tab = tab
        self._std = standard

    def add_note(self, note):
        """Add a note to the end of this song."""
        assert type(note) is Note
        self._notes.append(note)

    def num_notes(self):
        """Return the number of notes in this song."""
        return len(self._notes)

    def lily_str(self):
        """Return the entire song in LilyPond syntax as a string."""
        str_list = ["music = {\n  "]
        str_list += [self.lilypondify(i)+" " for i in xrange(self.num_notes())]
        str_list.append("\n}\n\\score{\n  ")
        if self._tab and self._std:
            str_list.append("\\new StaffGroup ")
        str_list.append("<<\n  ")
        if self._std:
            str_list.append("  \\new Staff{\\music}\n  ")
        if self._tab:
            str_list.append("  \\new TabStaff{\\music}\n  ")
        str_list.append(">>\n\n")

        if self._tab or self._std:
            str_list.append("  \\layout{}\n")
        if self._midi:
            str_list.append("  \\midi{}\n")

        str_list.append("}")

        return "".join(str_list)

    def lilypondify(self, index):
        """Return the pitch of a note in LilyPond syntax.

        Keyword arguments:
        index -- the position in this song of the note to lilypondify
        """
        note = self._notes[index]

        pitch = self._pitchify(note)
        octave = (pitch - Song._C_2)/12 # This is why we need _C_2
        degree = pitch % 12 # C is 0, B is 11.
        name = Song.lilypond_notes[degree] # The note's letter name

        duration = note.get_duration()
        suff_list = [str(duration)]
        if note.is_dotted():
            suff_list.append(".")
        if self._tab:
            string = note.get_string()
            suff_list.append("\\"+str(string))
        suffix = "".join(suff_list)

        if octave < 0:
            return name + abs(octave)*"," + suffix
        else:
            return name + octave*"'" + suffix

    def _pitchify(self, note):
        string = note.get_string() - 1
        return self._tuning[string] + note.get_fret()


class Note(object):

    values = (1, 2, 4, 8, 16, 32, 64)

    def __init__(self, fret, string, duration, dotted):
        assert type(fret) is IntType
        assert type(string) is IntType
        assert string > 0
        assert duration in Note.values
        self._data = (fret, string, duration, dotted)

    def get_fret(self):
        """Return the fret at which to play this note."""
        return self._data[0]

    def get_string(self):
        """Return the number of the string on which to play this note."""
        return self._data[1]

    def get_duration(self):
        """Return the duration (as whole, half, etc.) of this note."""
        return self._data[2]

    def is_dotted(self):
        """Return true if this is a dotted note, false otherwise."""
        return self._data[3]


class LilyWriter(object):

    def __init__(self, song):
        assert type(song) is Song
        self._song = song

    def write_ly(self, filename):
        """Write a song in LilyPond syntax to a file.

        Keyword arguments:
        filename -- the path/name of the file to write
        """
        ly = self._song.lily_str()
        f = open(filename, "w")
        f.write(ly)
        f.close()
