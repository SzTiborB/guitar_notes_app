import tkinter as tk
import piano_methods as pmet
import threading
import midi_handling

def scale_game_start():
    root = tk.Tk()
    root.title("Piano scale game")
    root.geometry("1400x700")

    piano = pmet.Piano(root=root)
    scale_game = pmet.Piano_Scale_Game(piano=piano,root=root)



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

    root.mainloop()