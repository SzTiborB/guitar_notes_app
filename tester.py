import tkinter as tk
import scale_game
import interval_game


root = tk.Tk()
root.title("Piano Trainer")
root.geometry("800x600")

#FÜGGVÉNYEK
def scale_game_start(synth_connected):
    synth_connected = synth_connected.get()
    scale_game.scale_game_start(synth_connected,menu_window=root)
def interval_game_start(synth_connected):
    interval_game.interval_game_start(synth_connected,menu_window=root)

#TIBLE LABELEK
title = tk.Label(root,text="Piano Trainer",font=("Arial", 32, "bold"))
title.pack(pady=50)


# FRAME A JÁTÉKOKNAK
game_button_frame = tk.Frame(root)
game_button_frame.pack(pady=20)
#GOMBOK-------------
synth_connected = tk.BooleanVar(value=True)  # alapból beikszelt
synth_checkbox = tk.Checkbutton(game_button_frame,text="Synth connected",variable=synth_connected)
scale_game_button = tk.Button(game_button_frame,text="Scale Game",font=("Arial", 12),
    width=20,height=3,command=lambda: scale_game_start(synth_connected))
interval_game_button = tk.Button(game_button_frame,text="Interval Game",font=("Arial", 12),
                   width=20,height=3,command=lambda: interval_game_start(synth_connected))
game_3 = tk.Button(game_button_frame,text="game_3",font=("Arial", 12),
                   width=20,height=3)
game_4 = tk.Button(game_button_frame,text="game_4",font=("Arial", 12),
                   width=20,height=3)
game_5 = tk.Button(game_button_frame,text="game_5",font=("Arial", 12),
                   width=20,height=3)
game_6 = tk.Button(game_button_frame,text="game_6",font=("Arial", 12),
                   width=20,height=3)
# GRID
synth_checkbox.grid(row=0,column=0,columnspan=2,pady=10)
scale_game_button.grid(row=1,column=0,padx=15,pady=15)
interval_game_button.grid(row=1,column=1,padx=15,pady=15)
game_3.grid(row=2,column=0,padx=15,pady=15)
game_4.grid(row=2,column=1,padx=15,pady=15)
game_5.grid(row=3,column=0,padx=15,pady=15)
game_6.grid(row=3,column=1,padx=15,pady=15)



exit_button = tk.Button(
    game_button_frame,
    text="Exit",
    font=("Arial", 16),
    width=15,
    command=root.destroy
)
exit_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=30
)





    
root.mainloop()