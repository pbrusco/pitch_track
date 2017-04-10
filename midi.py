#!/usr/bin/env python
# coding=utf-8
from __future__ import division

import music21
import math
from pyknon.genmidi import Midi
from pyknon.music import Note, Rest
import numpy as np


def to_midi(freq):
    if np.isnan(freq):
        return freq
    else:
        return int((12 / math.log(2)) * math.log(freq / 27.5) + 21)


def compact(midi_notes, step):
    notes_times = zip(midi_notes, [step] * len(midi_notes))
    res = []
    last_note = None
    for (n, t) in notes_times:
        if last_note == n:
            nf, tf = res[-1]
            res[-1] = (nf, tf + t)
        else:
            res.append((n, t))
        last_note = n
    return res


def from_pitch_track(times, pitch, sample_rate, filename="tmp.midi"):
    midi_notes = [to_midi(x) for x in pitch]
    notes = compact(midi_notes, step=(times[1] - times[0]) / sample_rate / 2)
    track0 = [Note(x, 0, round(t, 4)) if not np.isnan(x) else Rest(dur=round(t, 4)) for x, t in notes]
    m = Midi(1, tempo=90)
    m.seq_notes(track0, track=0)

    m.write(filename)
    return filename


def playMidi(filename):
    mf = music21.midi.MidiFile()
    mf.open(filename)
    mf.read()
    mf.close()
    s = music21.midi.translate.midiFileToStream(mf)
    s.show('midi')
    return s


def show_score(midi_filename="tmp.midi", output_filename="lily.png"):
    music21.environment.UserSettings()['lilypondPath'] = '/usr/bin/lilypond'
    music21.environment.set('pdfPath', '/usr/bin/musescore')
    music21.environment.set('graphicsPath', '/usr/bin/musescore')
    s = music21.converter.parse(midi_filename)
    return s.write(output_filename)
