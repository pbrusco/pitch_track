#!/usr/bin/env python
# coding=utf-8
from __future__ import division

import wave
import numpy as np
import struct


def load_from_wav(filename):
    f = wave.open(filename, 'r')
    frames = f.getnframes()
    dt = np.dtype("int16")
    data = np.frombuffer(f.readframes(nframes=frames), dtype=dt)
    sample_rate = f.getframerate()
    info = f.getparams()
    duration = frames / float(sample_rate)
    print(info)
    return data, frames, sample_rate, duration


def save_as_wav(data, sampleRate=44100.0, filename="sin.wav"):
    wavef = wave.open(filename, 'w')
    wavef.setnchannels(1)  # mono
    wavef.setsampwidth(2)
    wavef.setframerate(sampleRate)
    signal = []
    values_max = max(abs(data))
    for v in data:
        scaling_16bits = 32767 / values_max
        value = int(v * scaling_16bits)
        data = struct.pack('<h', value)
        wavef.writeframesraw(data)
        signal.append(value)
    wavef.close()
    return filename
