from __future__ import print_function
import intermediate as ir
from pyparsing import nums, oneOf, Word, Literal, Suppress, Optional
from pyparsing import ZeroOrMore, Group, OneOrMore, LineEnd, Keyword

def evalPhrase(s, l, t):
    duration = 4 #TODO: make this not a magic number
    dotted = False
    notes = []
    string = t.string

    for n in t[:-1]:
        if n.duration:
            duration = n.duration
            if n.dotted:
                dotted = True
            else:
                dotted = False
        note = ir.Note(n.fret, t.string, duration, dotted)
        notes.append(note)

    return notes

def evalSong(s, l, t):
    opts = t[0]
    song = ir.Song(pdf=opts.pdf, midi=opts.midi)
    for n in t[1:]:
        song.add_note(n)
    return song

bool_map = { "true": True, "false": False }
dur_map = { "w": 1, "h": 2, "q": 4, "e": 8, "s": 16, "t": 32, "sx": 64 }

# Defining character set
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
note_start = Keyword("notes").suppress()
staff_start = Keyword("staff").suppress()
pdf_tag = Keyword("pdf").suppress()
midi_tag = Keyword("midi").suppress()
tux_tag = Keyword("tux").suppress()
newline = LineEnd().suppress()

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
note = (Optional(full_dur) + fret)

# Production rules related to groups of notes
# note_seq := note (dash note)*
# string := number
# phrase := note_seq slash string
note_seq = Group(note) + ZeroOrMore(dash + Group(note))
string = number("string")
phrase = (note_seq + slash + string).setParseAction(evalPhrase)

# Scope-related production rules
# note_env := note_start phrase+
# staff := staff_start note_env+
note_env = note_start + OneOrMore(phrase) + newline
staff = staff_start + newline + OneOrMore(note_env)

pdf_opt = Optional(pdf_tag + equals + tf + newline, True)("pdf")
midi_opt = Optional(midi_tag + equals + tf + newline, False)("midi")
tux_opt = Optional(tux_tag + equals + tf + newline, False)("tux")
global_opt = pdf_opt & midi_opt & tux_opt

song = (Group(global_opt) + staff).setParseAction(evalSong)
