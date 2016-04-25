from __future__ import print_function
import intermediate as ir
from pyparsing import nums, oneOf, Word, Literal, Suppress, Optional
from pyparsing import ZeroOrMore, Group, OneOrMore, LineEnd, Keyword

def evalPhrase(s, l, t):
    def fillDuration(duration, dotted):
        dur = duration
        dot = dotted
        notes = []
        string = t.string

        for n in t[:-1]:
            if n.duration:
                dur = n.duration
                if n.dotted:
                    dot = True
                else:
                    dot = False
            note = ir.Note(n.fret, t.string, dur, dot)
            notes.append(note)

        return notes, dur, dot

    return fillDuration

def evalIsolatedRest(s, l, t):
    def fillDuration(duration, dotted):
        if t[0]:
            dur = t[0].duration
            if t[0].dotted:
                dot = True
            else:
                dot = False
        else:
            dur = duration
            dot = dotted

        return ir.Note(t.fret, 6, dur, dot)

    return fillDuration

def evalChord(s, l, t):
    def fillDuration(duration, dotted):
        if t[0]:
            dur = t[0].duration
            if t[0].dotted:
                dot = True
            else:
                dot = False
        else:
            dur = duration
            dot = dotted

        notes = [ir.Note(n.fret, n.string, dur, dot) for n in t[1:]]
        chord = ir.Chord()
        for n in notes:
            chord.add_note(n)

        return [chord], dur, dot

    return fillDuration

def evalTime(s, l, t):
    def fillDuration(duration, dotted):
        time = ir.TimeChange(t[0], t[1])
        return [time], duration, dotted

    return fillDuration

def evalTempo(s, l, t):
    def fillDuration(duration, dotted):
        tempo = ir.TempoChange(t.beat, t.bpm)
        return [tempo], duration, dotted

    return fillDuration

def evalStaff(s, l, t):
    opts = t[0]
    staff = ir.Staff(tab=opts.tab[0], standard=opts.std[0], tuning=opts.tune[0])
    notes = []
    dur = 4
    dot = False
    for f in t[1:]:
        next_part = f(dur, dot)
        notes.extend(next_part[0])
        dur = next_part[1]
        dot = next_part[2]
    staff.add_notes(notes)
    return staff

def evalSong(s, l, t):
    opts = t[0]
    song = ir.Song(pdf=opts.pdf[0], midi=opts.midi[0])
    for staff in t[1:]:
        song.add_staff(staff)
    return song

bool_map = { "true": True, "false": False }
dur_map = { "w": 1, "h": 2, "q": 4, "e": 8, "s": 16, "t": 32, "sx": 64 }

# Defining keywords and literals
# tf := "true" | "false"
# number := {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}+
# colon := ":"
# slash := "/"
# dash := "-"
# note_start := "notes " ## Not exactly correct, but close enough
# staff_start := "staff "
# pdf_tag := "pdf "
# midi_tag := "midi "
# tux_tag := "tux "
tf = oneOf("true false").setParseAction(lambda s, l, t: bool_map[t[0]])
number = Word(nums).setParseAction(lambda s, l, t: int(t[0]))
colon = Literal(":").suppress()
slash = Literal("/").suppress()
dash = Literal("-").suppress()
equals = Literal("=").suppress()
lparen = Literal("(").suppress()
rparen = Literal(")").suppress()
note_start = Keyword("notes").suppress()
time_tag = Keyword("time").suppress()
tempo_tag = Keyword("tempo").suppress()
staff_tag = Keyword("staff").suppress()
tab_tag = Keyword("tab").suppress()
std_tag = Keyword("notation").suppress()
tune_tag = Keyword("tuning").suppress()
pdf_tag = Keyword("pdf").suppress()
midi_tag = Keyword("midi").suppress()
tux_tag = Keyword("tux").suppress()
newline = LineEnd().suppress()

std_tune = Keyword("standard").setParseAction(lambda s, l, t: ir.Song.std_tuning)
dropd = Keyword("dropd").setParseAction(lambda s, l, t: ir.Song.drop_d)
tuning = (std_tune | dropd)

# Note-related production rules
# dotted := "d"
# duration := "w" | "h" | "q" | "e" | "s" | "t" | "sx"
# full_dur := duration dotted? colon
# fret := number
# note := full_dur? fret
dotted = Literal("d")("dotted").setParseAction(lambda s, l, t: True)
duration = oneOf("w h q e s t sx").setParseAction(lambda s, l, t: dur_map[t[0]])("duration")
full_dur = (duration + Optional(dotted) + colon)
fret = number("fret")
rest = Literal("r").setParseAction(lambda s, l, t: -1)("fret")
iso_rest = (Group(Optional(full_dur)) + rest).setParseAction(evalIsolatedRest)
note = (Optional(full_dur) + (fret | rest))

# Production rules related to groups of notes
# note_seq := note (dash note)*
# string := number
# phrase := note_seq slash string
note_seq = Group(note) + ZeroOrMore(dash + Group(note))
string = number("string")
phrase = (note_seq + slash + string).setParseAction(evalPhrase)

# Production rules related to chords
# chord_note := fret slash string
# chord := full_dur? lparen chord_note+ rparen
chord_note = (fret + slash + string)
chord = (Group(Optional(full_dur)) + lparen \
        + OneOrMore(Group(chord_note)) + rparen).setParseAction(evalChord)

# Scope-related production rules
# note_env := note_start phrase+
# time_change := time_tag equals number slash number
# tab_opt := (tab_tag equals tf)?
# std_opt := (std_tag equals tf)?
# staff := staff_start staff_opt (note_env | time_change | tempo_change)+
note_env = note_start + OneOrMore(phrase | chord | iso_rest) + newline
time_change = (time_tag + equals + number + slash + number \
        + newline).setParseAction(evalTime)
tempo_change = (tempo_tag + colon +  duration("beat") + equals + number("bpm") \
        + newline).setParseAction(evalTempo)
tab_opt = Optional(tab_tag + equals + tf, True)("tab")
std_opt = Optional(std_tag + equals + tf, False)("std")
tune_opt = Optional(tune_tag + equals + tuning, ir.Song.std_tuning)("tune")
staff_opt = tab_opt & std_opt & tune_opt
staff = (staff_tag + Group(staff_opt) \
    + OneOrMore(note_env| time_change |  tempo_change)).setParseAction(evalStaff)

# production rules for global options
# pdf_opt := (pdf_tag equals tf)?
# midi_opt := (midi_tag equals tf)?
# tux_opt := (tux_tag equals tf)?
pdf_opt = Optional(pdf_tag + equals + tf + newline, True)("pdf")
midi_opt = Optional(midi_tag + equals + tf + newline, False)("midi")
tux_opt = Optional(tux_tag + equals + tf + newline, False)("tux")
global_opt = pdf_opt & midi_opt & tux_opt

song = (Group(global_opt) + staff).setParseAction(evalSong)
