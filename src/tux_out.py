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
beat = factory.newBeat()
meas_man.addBeat(measure, beat)

# inp = TGInputStream()
# inp.init(song_manager.getFactory(), BufferedInputStream(FileInputStream(File('Untitled.tg'))))

# song = inp.readSong()
# print song.getTrack(0).stringCount()
# print song.getTrack(0).getMeasure(0).countBeats()


out = TGOutputStream()
out.init(song_man.getFactory(), BufferedOutputStream(FileOutputStream(File('foo.tg'))))

out.writeSong(song)
