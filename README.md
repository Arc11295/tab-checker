# tab-checker
I'll be using GNU [LilyPond](lilypond.org) as a backend for PDF/MIDI outputs, and a library provided by [TuxGuitar](www.tuxguitar.com.ar) to output files readable by the application itself.

## Requirements
In order to use this DSL, you need Python 2.7 and the latest version of GNU LilyPond (download Python [here](https://www.python.ord/downloads/) and LilyPond [here](lilypond.org/website/download.html) or use your favorite package manager).

## Running sample programs
There are some sample programs included in the directory `src/examples`. You can "run" them by running the script `src/example.py`. If you leave the script as-is, it will run the program called `simple.tc`. To run a different sample program, replace its name with the name of the program you want to run in the line in `example.py` that starts `example_name...`. This will output a file called `test.ly`. To get a pdf or midi (depending on the program you ran), run that output file through
LilyPond (e.g. by typing `lilypond test.ly` in a terminal).
