#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import matplotlib.pyplot as plt
import signal_processing
import numpy as np


def pitch_track(signal, pitch_times, pitch_points, ymin=0, ymax=1000):
    fig, ax = plt.subplots()
    ax.plot(signal)

    ax2 = ax.twinx()
    ax2.plot(pitch_times, pitch_points, "r-*")
    ax2.set_ylim([ymin, ymax])
    ax2.set_ylabel("Freq (Hz)")


def wave(t0, tf, sample_rate, data, spectro=False, show_time=True):
    times, signal = signal_processing.data_between(t0, tf, data, sample_rate)
    if show_time:
        plt.plot(times, signal, "*-")
        plt.title("{} ms - {} muestras".format(round((tf - t0) * 1000, 4), len(times)))
        plt.xlabel('Tiempo (segundos)')
        plt.xlim([min(times), max(times)])
    else:
        plt.plot(np.arange(len(signal)), signal, "*-")
        plt.title("{} ms - {} muestras".format(round((tf - t0) * 1000, 4), len(times)))
        plt.xlabel('Muestra')
        plt.xlim([0, len(signal)])

    plt.ylabel("Amplitud (int16)")

    plt.figure()
    if spectro:
        S, freqs, bins, im = plt.specgram(data, NFFT=1024, Fs=sample_rate, noverlap=512)
        # Plot a spectrogram
        plt.ylim([0, 1000])
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.figure()
