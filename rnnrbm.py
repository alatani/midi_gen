# original: https://github.com/lisa-lab/DeepLearningTutorials/blob/master/code/rnnrbm.py#L18

from __future__ import print_function

import typing
import numpy

try:
    import pylab
except ImportError:
    print ("pylab isn't available. If you use its functionality, it will crash.")
    print("It can be installed with 'pip install -q Pillow'")

from midi.utils import midiread, midiwrite




class MidiIO:
    '''Simple class to train an RNN-RBM from MIDI files and to generate sample
    sequences.'''

    def __init__(self, pitch_range=(21, 109), dt=0.05):
        '''
        r : (integer, integer) tuple
            Specifies the pitch range of the piano-roll in MIDI note numbers,
            including r[0] but not r[1], such that r[1]-r[0] is the number of
            visible units of the RBM at a given time step. The default (21,
            109) corresponds to the full range of piano (88 notes).
        dt : float
            Sampling period when converting the MIDI files into piano-rolls, or
            equivalently the time difference between consecutive time steps.'''

        self.pitch_range = pitch_range
        self.dt = dt


    def fromMidi(self, file, batch_size=100, num_epochs=200):
        data = midiread(file, self.pitch_range, self.dt).piano_roll.astype(theano.config.floatX)
        return data


    def writeMidiFromPianoRoll(self, piano_roll, filename):
        '''Generate a sample sequence, plot the resulting piano-roll and save
        it as a MIDI file.
        filename : string
            A MIDI file will be created at this location.
        show : boolean
            If True, a piano-roll of the generated sequence will be shown.'''
        midiwrite(filename, piano_roll, self.r, self.dt)



    def showPianoRoll(self, piano_roll):
        extent = (0, self.dt * len(piano_roll)) + self.r
        pylab.figure()
        pylab.imshow(piano_roll.T, origin='lower', aspect='auto',
                     interpolation='nearest', cmap=pylab.cm.gray_r,
                     extent=extent)
        pylab.xlabel('time (s)')
        pylab.ylabel('MIDI note number')
        pylab.title('generated piano-roll')


if __name__ == '__main__':
    model = test_rnnrbm()
    model.generate('sample1.mid')
    model.generate('sample2.mid')
    pylab.show()