import numpy as np
import sounddevice as sd
import time
import os

SAMPLE_RATE = 44100

def pluck(frequency, duration=2):
    N = int(SAMPLE_RATE / frequency)

    buffer = np.random.uniform(-1, 1, N)
    samples = np.zeros(int(SAMPLE_RATE * duration))

    for i in range(len(samples)):
        samples[i] = buffer[i % N]

        next_sample = 0.996 * 0.5 * (
            buffer[i % N] +
            buffer[(i + 1) % N]
        )

        buffer[i % N] = next_sample

    return samples

#region - distortions
# def distortion(sound, gain=8):
#     return np.tanh(gain * sound)
# def lowpass(sound, alpha=0.2):
#     output = np.zeros_like(sound)
#     output[0] = sound[0]
#     for i in range(1, len(sound)):
#         output[i] = (
#             alpha * sound[i]
#             + (1 - alpha) * output[i-1]
#         )
#     return output
#endregion

def play_chord(fret_indexes, duration=2):
    chord = np.zeros(int(SAMPLE_RATE * duration))
    for fret_index in fret_indexes:
        string_sound = sound_cache[fret_index]
        chord += string_sound
    # hangerő normalizálása
    chord /= len(fret_indexes)
    sd.stop()  #előző hang leállítása
    sd.play(chord, SAMPLE_RATE)
    

CACHE_FILE = "sound_cache.npz"
if os.path.exists(CACHE_FILE):
    print("Loading sound cache...")
    loaded_cache = np.load(CACHE_FILE)
    sound_cache = {
        int(key): loaded_cache[key]
        for key in loaded_cache.files
    }
else:
    print("Generating sound cache...")
    sound_cache = {
        0:  pluck(82.41),      # E2
        1:  pluck(87.31),      # F2
        2:  pluck(92.50),      # F#2
        3:  pluck(98.00),      # G2
        4:  pluck(103.83),     # G#2
        5:  pluck(110.00),     # A2
        6:  pluck(116.54),     # A#2
        7:  pluck(123.47),     # B2
        8:  pluck(130.81),     # C3
        9:  pluck(138.59),     # C#3
        10: pluck(146.83),     # D3
        11: pluck(155.56),     # D#3

        12: pluck(164.81),     # E3
        13: pluck(174.61),     # F3
        14: pluck(185.00),     # F#3
        15: pluck(196.00),     # G3
        16: pluck(207.65),     # G#3
        17: pluck(220.00),     # A3
        18: pluck(233.08),     # A#3
        19: pluck(246.94),     # B3
        20: pluck(261.63),     # C4
        21: pluck(277.18),     # C#4
        22: pluck(293.66),     # D4
        23: pluck(311.13),     # D#4

        24: pluck(329.63),     # E4
        25: pluck(349.23),     # F4
        26: pluck(369.99),     # F#4
        27: pluck(392.00),     # G4
        28: pluck(415.30),     # G#4
        29: pluck(440.00),     # A4
        30: pluck(466.16),     # A#4
        31: pluck(493.88),     # B4
        32: pluck(523.25),     # C5
        33: pluck(554.37),     # C#5
        34: pluck(587.33),     # D5
        35: pluck(622.25),     # D#5

        36: pluck(659.25),     # E5
        37: pluck(698.46),     # F5
        38: pluck(739.99),     # F#5
        39: pluck(783.99),     # G5
        40: pluck(830.61),     # G#5
        41: pluck(880.00),     # A5
        42: pluck(932.33),     # A#5
        43: pluck(987.77),     # B5
        44: pluck(1046.50),    # C6
        45: pluck(1108.73),    # C#6
        46: pluck(1174.66),    # D6
        47: pluck(1244.51),    # D#6
        48: pluck(1318.51)     # E6
    }
    np.savez(
        CACHE_FILE,
        **{str(key): value for key, value in sound_cache.items()}
    )