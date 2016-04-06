import jnius_config
jnius_config.set_classpath('./tuxguitar-lib-1.3.2.jar')
from jnius import autoclass

TGSongManager = autoclass('org.herac.tuxguitar.song.managers.TGSongManager')
TGOutputStream = autoclass('org.herac.tuxguitar.io.tg.TGOutputStream')
TGInputStream = autoclass('org.herac.tuxguitar.io.tg.TGInputStream')
FileOutputStream = autoclass('java.io.FileOutputStream')
FileInputStream = autoclass('java.io.FileInputStream')
BufferedInputStream = autoclass('java.io.BufferedInputStream')
BufferedOutputStream = autoclass('java.io.BufferedOutputStream')
File = autoclass('java.io.File')

song_man = TGSongManager()
meas_man = song_man.getMeasureManager()
track_man = song_man.getTrackManager()
factory = song_man.getFactory()


song = song_man.newSong()
measure = track_man.getFirstMeasure(song.getTrack(0))

inp = TGInputStream()
inp.init(song_man.getFactory(), BufferedInputStream(FileInputStream(File('Untitled.tg'))))

song2 = inp.readSong()
measure2 = track_man.getFirstMeasure(song2.getTrack(0))
beat2 = meas_man.getFirstBeat(measure2.getBeats())
print beat2.getVoice(0).getNote(0).getVelocity()
beat = beat2.clone(song_man.getFactory())

meas_man.addBeat(measure, beat)

# out = TGOutputStream()
# out.init(song_man.getFactory(), BufferedOutputStream(FileOutputStream(File('foo.tg'))))

# out.writeSong(song)
