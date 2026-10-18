import tkinter as tk
import piano_methods as pmet
import threading
import midi_handling
import json
import os

def scale_game_start():

    #json file kezelés----------
    filename = "compledet_scales.json"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
    else:
        data = {
            "completed_scales": 0
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    completed_scales = data["completed_scales"]
    print(completed_scales)
    # json###################


    root = tk.Tk()
    root.title("Piano scale game")
    root.geometry("1400x700")

    piano = pmet.Piano(root=root)
    scale_game = pmet.Piano_Scale_Game(piano=piano,root=root,
                                       already_completed_scales=completed_scales)




    #SZINTETIZATOR KEZELESE: ---------------
    midi_thread = threading.Thread(
        target=midi_handling.keyboard_handling_init,
        daemon=True
    )
    midi_thread.start()
    def check_midi(): # A TKINTER  MAINLOOP UTÁN FUSSON LE
        if not midi_handling.note_queue.empty():
            note_ID = midi_handling.note_queue.get()


            # scale_game.set_piano_keyboard_offset(piano)
            # scale_game.is_note_in_random_scale(guessed_noteID=note_ID,piano=piano) #note-bogyók berajzolása
            scale_game.key_pressed(note_ID=note_ID,piano=piano)

            print("Főprogram megkapta:", note_ID)
        root.after(10, check_midi)
    #Szintetizator kezelése####################

    #MIDI queue figyelésének az elindítása
    check_midi()

    #BEZÁRÁSKOR MENTSE KI AZ ÖSSZES LEJÁTSZOTT SKÁLÁT
    def on_closing():
        print("Colsing window")
        completed_scales = scale_game.already_completed_scales
        
        #save to json
        data["completed_scales"] = completed_scales
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()