import tkinter as tk
import piano_methods as pmet
import threading
import json
import os

def interval_game_start(synth_connected,menu_window):


    game_window = tk.Toplevel(menu_window)

    piano = pmet.Piano(root=game_window)
    interval_game = pmet.Piano_Interval_Game(piano=piano,root=game_window,random_interval_count=3)

        #függvények
    def keyboard_click(event):
        note_ID = piano.click_on_keyboard(event=event)
        print(f"NOTEEEEEE: {note_ID}")
        interval_game.key_pressed(note_ID=note_ID)

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
                interval_game.key_pressed(note_ID=note_ID,piano=piano)

                print("Főprogram megkapta:", note_ID)
            game_window.after(10, check_midi)
        #Szintetizator kezelése####################

        #MIDI queue figyelésének az elindítása
        check_midi()

    else:
        print("PIANO KLIKKELÉS KELL IDE")
        piano.keyboard.bind("<Button-1>", keyboard_click)




    #BEZÁRÁSKOR 
    def on_closing():
        print("Colsing window")
        game_window.destroy()

    game_window.protocol("WM_DELETE_WINDOW", on_closing)