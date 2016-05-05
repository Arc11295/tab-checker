from parser import *

example_name = "test2.tc"

s = song.parseFile("./examples/" + example_name)[0]

writer = ir.LilyWriter(s)
writer.write_ly("./test.ly")
