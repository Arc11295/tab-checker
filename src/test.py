from parser import *

s = song.parseFile("./test.tc")[0]

writer = ir.LilyWriter(s)
writer.write_ly("./test.ly")
