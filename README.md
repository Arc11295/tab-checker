# tab-checker
I've used GNU [LilyPond](lilypond.org) as a backend for PDF/MIDI outputs. I looked into using a library component provided by [TuxGuitar](www.tuxguitar.com.ar) to output files readable by the TuxGuitar application itself, but the library didn't have any kind of documentation and had a lot of code, so I didn't make that much progress. The syntax is mostly taken from another DSL, [VexTab](http://www.vexflow.com/vextab/), but I wrote everything in this repository myself.

## Requirements
In order to use this DSL, you need Python 2.7 and the latest version of GNU LilyPond (download Python [here](https://www.python.ord/downloads/) and LilyPond [here](lilypond.org/website/download.html) or use your favorite package manager). The parser also requires the module pyparsing, which is available through PyPI. 

## Running sample programs
There are some sample programs included in the directory `src/examples`. You can "run" them by running the script `src/example.py`. If you leave the script as-is, it will run the program called `simple.tc`. To run a different sample program, replace its name with the name of the program you want to run in the line in `example.py` that starts `example_name...`. This will output a file called `test.ly`. To get a pdf or midi (depending on the program you ran), run that output file through
LilyPond (e.g. by typing `lilypond test.ly` in a terminal). It might also be useful to look at the [final report](https://github.com/Arc11295/project/blob/master/documents/final.md) I wrote for the class this project was a part of since there's a section that walks through these example programs step-by-step.
