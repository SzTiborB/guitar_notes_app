import mido
import queue

print(mido.get_input_names())
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

note_queue = queue.Queue()

def keyboard_handling_init():
    with mido.open_input(mido.get_input_names()[0]) as keyboard:
        print("MIDI figyelése...")

        for msg in keyboard:
            msg : mido.Message
            if msg.type == "note_on":
                if msg.velocity != 0:
                    note = NOTE_DICT[msg.note % 12]
                    octave = msg.note // 12
                    note_ID = str(note) +"_"+ str(octave)
                    print(f"Hang: {note_ID}")
                    note_queue.put(note_ID)
                