from __future__ import print_function
from string import Template
from types import IntType

class Song(object):

    C_2 = 48
    # Just trust me on this one, ok? It has to do with MIDI numbers and
    # the fact that LilyPond takes plain note names to mean notes in
    # the octave BELOW middle C, so we need some constant, and MIDI
    # numbers were a convenient choice.

    std_tuning = (64, 59, 55, 50, 45, 40)
    drop_d = (64, 59, 55, 50, 45, 38)
    half_down = (63, 58, 54, 49, 44, 39)
    whole_down = (62, 57, 53, 48, 43, 38)

    lilypond_notes = \
        ("c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b")


    def __init__(self, pdf=True, midi=False, bpm=120):
        self._staves = []
        self._pdf = pdf
        self._midi = midi
        self._bpm = bpm

    def add_staff(self, staff):
        assert type(staff) is Staff
        self._staves.append(staff)

    def num_staves(self):
        return len(self._staves)

    def get_tempo(self):
        return self._bpm

    def lily_str(self):
        """Return the entire song in LilyPond syntax as a string."""
        subs = {}

        if self._pdf:
            subs["LAYOUT"] = "\\layout{}"
        else:
            subs["LAYOUT"] = ""
        if self._midi:
            subs["MIDI"] = "\\midi{}"
        else:
            subs["MIDI"] = ""

        blocks = [staff.notes_str(i) for i, staff in enumerate(self._staves)]
        subs["NOTE_BLOCKS"] = "".join(blocks)
        staves = [staff.staff_str(i) for i, staff in enumerate(self._staves)]
        subs["STAVES"] = "".join(staves)

        f = open("template.ly")
        temp_str = f.read()
        f.close()
        return Template(temp_str).substitute(subs)


def _pitch_to_lily(pitch):
    octave = (pitch - Song.C_2)/12 # This is why we need C_2
    degree = pitch % 12 # C is 0, B is 11.
    name = Song.lilypond_notes[degree] # The note's letter name

    if octave < 0:
        return name + abs(octave)*","
    else:
        return name + octave*"'"


class Staff(object):

    def __init__(self, tab=True, standard=False, tuning=Song.std_tuning):
        self._notes = []
        self._tuning = tuning
        self._tab = tab
        self._std = standard

    def add_note(self, note):
        """Add a note to the end of this staff."""
        self._notes.append(note)

    def add_notes(self, notes):
        """Add multiple notes to the end of this staff."""
        self._notes.extend(notes)

    def num_notes(self):
        """Return the number of notes in this staff."""
        return len(self._notes)

    def staff_str(self, index):
        ascii_A = ord("A")
        subs = {}

        if self._std and self._tab:
            subs["STAFFGROUP"] = "\\new StaffGroup "
        else:
            subs["STAFFGROUP"] = ""

        if self._std:
            subs["STAFF"] = "\\new Staff{\\transpose c c' {\\music%c}}"%(index + ascii_A)
        else:
            subs["STAFF"] = ""
        if self._tab:
            subs["TABSTAFF"] = \
                "\\new TabStaff %s{\\music%c}"%(self.tune_str(), index + ascii_A)
        else:
            subs["TABSTAFF"] = ""

        f = open("staff_template.ly")
        temp_str = f.read()
        f.close()
        return Template(temp_str).substitute(subs)

    def notes_str(self, index):
        ascii_A = ord("A")
        subs = {}

        subs["MUSIC"] = "music%c"%(index + ascii_A)
        note_list = [n.lilypondify(self._tuning)+" " for n in self._notes]
        subs["NOTES"] = "".join(note_list)

        f = open("notes_template.ly")
        temp_str = f.read()
        f.close()
        return Template(temp_str).substitute(subs)

    def tune_str(self):
        note_list = [_pitch_to_lily(p) for p in reversed(self._tuning)]
        pitches = " ".join(note_list)
        return "\\with {stringTunings = \\stringTuning <%s>}"%pitches


class Chord(object):

    def __init__(self):
        self._notes = []
        self._strings = set()

    def add_note(self, note):
        assert type(note) is Note
        string = note.get_string()
        assert string not in self._strings
        self._notes.append(note)
        self._strings.add(string)

    def lilypondify(self, tuning):
        duration = self._notes[0].get_duration()
        notes_list = [n.lilypondify(tuning, False)+" " for n in self._notes]
        return "< " + "".join(notes_list) + ">" + str(duration)


class TimeChange(object):

    def __init__(self, top, bottom):
        self._top = top
        self._bot = bottom

    def get_top(self):
        return self._top

    def get_bot(self):
        return self._bot

    def lilypondify(self, tuning):
        return "\\time %d/%d"%(self.get_top(), self.get_bot())


class TempoChange(object):

    def __init__(self, beat, bpm):
        self._beat = beat
        self._bpm = bpm

    def get_beat(self):
        return self._beat

    def get_bpm(self):
        return self._bpm

    def lilypondify(self, tuning):
        return "\\tempo %d = %d"%(self.get_beat(), self.get_bpm())


class Note(object):

    values = (1, 2, 4, 8, 16, 32, 64)

    def __init__(self, fret, string, duration, dotted=False):
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

    def lilypondify(self, tuning, write_duration=True, force_string=True):
        """Return the pitch of a note in LilyPond syntax.

        """
        if self.get_fret >= 0:
            pitch = self._pitchify(tuning)
            name = _pitch_to_lily(pitch)
        else:
            name = "r" # negative frets correspond to rests here

        if write_duration:
            duration = self.get_duration()
            suff_list = [str(duration)]
            if self.is_dotted():
                suff_list.append(".")
        else:
            suff_list = []

        if not name == "r": # a note doesn't really have a string if it's a rest
            string = self.get_string()
            suff_list.append("\\"+str(string))
        suffix = "".join(suff_list)

        return name + suffix

    def _pitchify(self, tuning):
        string = self.get_string() - 1
        return tuning[string] + self.get_fret()


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
