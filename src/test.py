from parser import *

s = song.parseFile("./test2.tc")[0]

writer = ir.LilyWriter(s)
writer.write_ly("./test2.ly")
