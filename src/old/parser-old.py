from __future__ import unicode_literals, print_function
from pypeg2 import *

class Bool(Keyword):
    grammar = Enum( K("true"), K("false") )

class Number(str):
    grammar = RegEx(r"\d+")

class Duration(str):
    grammar = Number, attr("dotted", optional(RegEx("d"))), ":"

class Fret(str):
    grammar = attr("duration", optional(Duration)), Number

class FretSeq(List):
    grammar = Fret, maybe_some("-", Fret)

class StringNum(str):
    grammar = Number

class Phrase(object):
    grammar = attr("frets", FretSeq), "/", attr("string", StringNum)

class Notes(List):
    grammar = K("notes"), some(Phrase), endl

class Staff(List):
    grammar = K("staff"), endl, some(Notes)
    # TODO: add staff options on the same line as staff keyword

class OptName(Keyword):
    grammar = Enum( K("pdf"), K("midi"), K("tux"))

class GlobalOption(object):
    grammar = attr("name", OptName), "=", attr("value", Bool)

class GlobalOptions(List):
    grammar = some(GlobalOption, endl)

class Song(List):
    grammar = optional(GlobalOptions), Staff
