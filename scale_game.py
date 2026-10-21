import tkinter as tk
import piano_methods as pmet
import threading
import json
import os

def scale_game_start(synth_connected,menu_window):


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

    game_window = tk.Toplevel(menu_window)

    piano = pmet.Piano(root=game_window)
    scale_game = pmet.Piano_Scale_Game(piano=piano,root=game_window,
                                       already_completed_scales=completed_scales)


    #függvények
    def keyboard_click(event):
        note_ID = piano.click_on_keyboard(event=event)
        print(f"NOTEEEEEE: {note_ID}")
        scale_game.key_pressed(note_ID=note_ID,piano=piano)


    if synth_connected == True:
        #SZINTETIZATOR KEZELESE: ---------------
        print("INDUL A MANDULA")
        import midi_handling
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
            game_window.after(10, check_midi)
        #Szintetizator kezelése####################

        #MIDI queue figyelésének az elindítása
        check_midi()

    else:
        print("PIANO KLIKKELÉS KELL IDE")
        piano.keyboard.bind("<Button-1>", keyboard_click)

    #BEZÁRÁSKOR MENTSE KI AZ ÖSSZES LEJÁTSZOTT SKÁLÁT
    def on_closing():
        print("Colsing window")
        completed_scales = scale_game.already_completed_scales
        
        #save to json
        data["completed_scales"] = completed_scales
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        game_window.destroy()

    game_window.protocol("WM_DELETE_WINDOW", on_closing)
  