import tkinter as tk
from tkinter import ttk
import methods as mt
root = tk.Tk()
root.title("Guitar Trainer")
root.geometry("1400x600")

# -------------------------
# Gitárnyak területe
# -------------------------
#AZ ALAP FRETBOARD
WIDTH = 1300
HEIGHT = 300
fretboard = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="white"
)
#FELRAJZOLJA A GITÁRT, FRET ÉS STRING POZÍCIÓKAT ELTÁROLJUK -> kattintások-hangokhoz rendelése
fret_position,string_position=mt.guitar_init(WIDTH,HEIGHT,fretboard)
fretboard.pack(pady=20)
#-------------------------



# -------------------------
# Gombok területe
# -------------------------
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)
ttk.Button(button_frame, text="Notes").grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Intervals").grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="New question").grid(row=0, column=2, padx=10)
#--------------------------




#--------------------------
# KATTINTÁS ÉRZÉKELÉS
#--------------------------
def fretboard_click(event):
    print("x:", event.x)
    print("y:", event.y)
    string,fret =which_string_and_fret(event.x,event.y)
    which_note(string,fret)

fretboard.bind("<Button-1>", fretboard_click)
#-------------------------

def which_string_and_fret(x,y):

    #FRET ------------
    fret_done = False
    if x < 100:
        clicked_fret = 0
        fret_done=True
    elif x >1280:
        clicked_fret = False
        fret_done=True
    for fret,position in fret_position.items():
        if fret_done == False:
            if x < position:
                clicked_fret=fret
                fret_done = True
    #print(f"Kattintott: {clicked_fret}")
    #--------------------------

    #STRING
    string_done = False # kicsit sajátos számozással csináltam meg a húrokat lol
    if y > 280 | y<20:
        clicked_string = False
        string_done = True
    for string,position in string_position.items():
        if string_done == False:
            if y < position:
                clicked_string = string
                string_done = True
    print(f"{clicked_string}. húron  {clicked_fret} fret")
    return clicked_string,clicked_string

def which_note(string,fret):
    notes = {
    0: "E",
    1: "F",
    2: "F# - Gb",
    3: "G",
    4: "G# - Ab",
    5: "A",
    6: "A# - Bb",
    7: "B",
    8: "C",
    9: "C# - Db",
    10: "D",
    11: "D# - Eb"}

    #húrokkénti hangok eltolása:
    if string == 5:
        note_offset = 0
    elif string == 4:
        note_offset = 5
    elif string == 3:
        note_offset =10
    elif string == 2:
        note_offset = 15
    elif string == 1:
        note_offset = 19
    elif string == 0:
        note_offset =24
    print(f"A fret: {fret}, {note_offset}")
    #AZ E húron ez hanyadik fret lenne?
    fret_value = fret+note_offset
    print(f"A fret value: {fret_value}")
    note = notes[fret_value%12]
    print(f"A hang: {note}")



for fret,position in fret_position.items():
    print(fret,position)

root.mainloop()