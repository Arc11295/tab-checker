from parser import *
import intermediate as ir

f = open("test.tc")
test = f.read()
f.close()

p = parse(test, Song)

block = p[0]

options = {}
if type(block) is GlobalOptions:
    for opt in block:
        if opt.value.name == "true":
            options[opt.name.name] = True
        else: #I've ensured that if it's not "true", it must be "false"
            options[opt.name.name] = False
    block = p[1]
    assert type(block) is Staff

print(options)

song = ir.Song()
duration = 4
dotted = False
for notes in block:
    for phrase in notes:
        string = int(phrase.string)
        frets = phrase.frets
        for fret in frets:
            d = fret.duration
            if d:
                duration = int(d)
                if d.dotted:
                    dotted = True
                else:
                    dotted = False
            note = ir.Note(int(fret), string, duration, dotted)
            song.add_note(note)

out = song.lily_str()
f = open("test.ly", "w")
f.write(out)
f.close()
