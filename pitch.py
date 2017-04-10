#!/usr/bin/env python
# coding=utf-8
from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.mlab import find
import numpy.fft

import scipy.signal
import signal_processing


def freq_from_autocorr(sig, sample_rate, max_freq=1000, show_plot=False):
    corr = signal_processing.autocorrelation(sig)
    min_period = int(sample_rate * (1 / max_freq))

    # primer minimo:
    d = np.diff(corr)
    try:
        start = find(d > 0)[0]
    except:
        return np.nan

    start = max(start, min_period)

    # pasando ese primer minimo, buscamos el maximo
    peak = np.argmax(corr[start:]) + start

    if show_plot:
        plt.plot(corr, "-r", label=u"correlación")
        plt.ylim([-2, 2])
        plt.title("correlation")
        plt.scatter(peak, corr[peak], s=200, color="green", label="maximo")
        plt.scatter(start, corr[start], s=200, color="blue", label="busca desde")
        plt.legend()
    return sample_rate / peak


def freq_from_zcr(sig, sample_rate, max_freq=1000):
    # Find all indices right before a rising-edge zero crossing
    indices = find((sig[1:] >= 0) & (sig[:-1] < 0))

    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - sig[i] / (sig[i + 1] - sig[i]) for i in indices]

    return sample_rate / np.mean(np.diff(crossings))


def freq_from_fft(sig, sample_rate, max_freq):
    """
    Estimate frequency from peak of FFT
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * scipy.signal.blackmanharris(len(sig))
    f = numpy.fft.rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f))  # Just use this for less-accurate, naive version

    # Convert to equivalent frequency
    return sample_rate * i / len(windowed)


def track(signal, method, step, sample_rate, min_pitch=50, max_pitch=1000, silence_threshold=0):
    step_in_frames = int(step * sample_rate)

    window_length = int((1 / min_pitch) * 2 * sample_rate)
    pitch = []
    times = []
    for start in range(0, len(signal) - window_length, step_in_frames):
        s = signal[start:start + window_length]
        rms = signal_processing.rms(s)

        if np.isnan(rms) or rms < silence_threshold:
            pitch.append(np.nan)
        else:
            f0 = method(s, sample_rate, max_pitch)
            pitch.append(f0)

        times.append(start)
    times = np.array(times)
    pitch = np.array(pitch)

    return times, pitch


def smooth_pitch(pitch_track, window, poly_order=2):
    return scipy.signal.savgol_filter(pitch_track, window, poly_order)
