

import os, os.path

from midi.utils import midiread, midiwrite

datadir = "/Users/a14139/workspace/mml/midis/midi/classic"


def create_midi_from_piano_roll(piano_roll):
    pass


if __name__ == "__main__":
    path = "/Users/a14139/workspace/mml/midis/midi/classic"
    files = [ os.path.join(path, f)  for f in os.listdir(path)]
    midi0 = pretty_midi.PrettyMIDI(files[0])
    piano_roll = midi0.get_piano_roll()

    print type(piano_roll)
    print piano_roll

    #piano_program = pretty_midi.instrument_name_to_program('piano')
    #piano = pretty_midi.Instrument(program=piano_program)
    #piano.notes.append()
    pass
