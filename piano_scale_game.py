import tkinter as tk
from tkinter import ttk
import midi_handling
import threading
import piano_methods as pmet
import random

root = tk.Tk()
root.title("Piano scale game")
root.geometry("1400x700")

#PIANO WINDOW KREÁLÁSA
piano_window = pmet.Piano(root=root)


#SKÁLÁK KEZELÉSE---------
#skálák
MUSIC_SCALES = {
    "Ionian (Major)":       ["W W H W W W H",  [2,2,1,2,2,2,1]],
    "Dorian":               ["W H W W W H W",  [2,1,2,2,2,1,2]],
    "Phrygian":             ["H W W W H W W",  [1,2,2,2,1,2,2]],
    "Lydian":               ["W W W H W W H",  [2,2,2,1,2,2,1]],
    "Mixolydian":           ["W W H W W H W",  [2,2,1,2,2,1,2]],
    "Aeolian (Natural Minor)":["W H W W H W W", [2,1,2,2,1,2,2]],
    "Locrian":              ["H W W H W W W",  [1,2,2,1,2,2,2]],

    "Harmonic Minor":       ["W H W W H WH H", [2,1,2,2,1,3,1]],
    "Melodic Minor":        ["W H W W W W H",  [2,1,2,2,2,2,1]],

    "Major Pentatonic":     ["W W WH W WH",     [2,2,3,2,3]],
    "Minor Pentatonic":     ["WH W W WH W",     [3,2,2,3,2]],

    "Blues":                ["WH W H H WH W",   [3,2,1,1,3,2]],

    "Whole Tone":           ["W W W W W W",     [2,2,2,2,2,2]],

    "Arabic":               ["H WH H W H WH H", [1,3,1,2,1,3,1]]
}
random_scale_weights = [
    20,  # Ionian (Major)
    3,   # Dorian
    3,   # Phrygian
    3,   # Lydian
    3,   # Mixolydian
    20,  # Aeolian (Natural Minor)
    3,   # Locrian
    3,   # Harmonic Minor
    3,   # Melodic Minor
    2,   # Major Pentatonic
    2,   # Minor Pentatonic
    2,   # Blues
    1,   # Whole Tone
    1    # Arabic
]
random_scale = random.choices(list(MUSIC_SCALES.keys()),weights=random_scale_weights,k=1)[0]
print(random_scale)
#hangok
NOTE_DICT = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B"
}
random_note_index = random.choices(list(NOTE_DICT.keys()),k=1)[0]
print(f"Steps: {MUSIC_SCALES[random_scale][0]}")
print(f"Steps with numbers: {MUSIC_SCALES[random_scale][1]}")
random_scale_note_indexes = [random_note_index]
for step_index in MUSIC_SCALES[random_scale][1]:
    random_scale_note_indexes.append(random_scale_note_indexes[-1]+step_index)
print(f"INDEXEKKEL: {random_scale_note_indexes}")



#Skálák kezelése###############



#SZINTETIZATOR KEZELESE: ---------------
midi_thread = threading.Thread(
    target=midi_handling.keyboard_handling_init,
    daemon=True
)
midi_thread.start()
def check_midi(): # A TKINTER  MAINLOOP UTÁN FUSSON LE
    if not midi_handling.note_queue.empty():
        note_ID = midi_handling.note_queue.get()
        piano_window.update_keyboard(note_ID) #note-bogyók berajzolása
        print("Főprogram megkapta:", note_ID)
    root.after(10, check_midi)
#Szintetizator kezelése####################




check_midi()
#OPEN WINDOW
root.mainloop()