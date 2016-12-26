
import typing
import os, os.path
import midi

#from music21 import *
import music21

datadir = "/Users/a14139/workspace/mml/midis/midi/classic"

def create_midi_from_piano_roll(piano_roll):
    pass

def parse_with_music21(filename):
    score = music21.converter.parse(filename)
    print(score)
    key = score.analyze('key')
    #    print key.tonic.name, key.mode
    #if key.mode == "major":
    #    halfSteps = majors[key.tonic.name]

    #elif key.mode == "minor":
    #    halfSteps = minors[key.tonic.name]

    #newscore = score.transpose(halfSteps)
    #key = newscore.analyze('key')
    #print key.tonic.name, key.mode
    newFileName = "C_" + file
    newscore.write('midi',newFileName)


if __name__ == "__main__":
    path = "/Users/a14139/workspace/mml/midis/midi/classic"
    files = [ os.path.join(path, f)  for f in os.listdir(path)]
    print(files)

    pattern = midi.read_midifile(files[0])
    print(pattern)

    # midi0 = pretty_midi.PrettyMIDI(files[0])
    # piano_roll = midi0.get_piano_roll()

    #piano_program = pretty_midi.instrument_name_to_program('piano')
    #piano = pretty_midi.Instrument(program=piano_program)
    #piano.notes.append()
    pass
