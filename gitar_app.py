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
# ttk.Button(button_frame, text="Notes").grid(row=0, column=0, padx=10)
# ttk.Button(button_frame, text="Intervals").grid(row=0, column=1, padx=10)
# ttk.Button(button_frame, text="New question").grid(row=0, column=2, padx=10)

kezdo_label = ttk.Label(button_frame,text="A hang:",font=("Arial", 30))
kezdo_label.grid(row=0, column=0,pady=20)

#--------------------------




#--------------------------
# KATTINTÁS ÉRZÉKELÉS
#--------------------------
def fretboard_click(event):
    print("x:", event.x)
    print("y:", event.y)
    string,fret =which_string_and_fret(event.x,event.y)
    note =which_note(string,fret)
    kezdo_label.config(text=f"A hang {note}")

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
    if y > 280 or y<0:
        clicked_string = False
        string_done = True
    string_border = {0:62,1:106,2:150,3:194,4:238,5:280} #sokkal könyebb hardcode-olva
    for string,border in string_border.items():
        if string_done == False:
            if y < border:
                clicked_string = string
                string_done = True
        #PIROSSAL KIJELZÉS
        if string <5: #gitár szélére már ne rajzoljon
            fretboard.create_line(100, border, 1300, border,width=2,fill="red")
    print(string_border)
    return clicked_string,clicked_fret

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
    string_names = {
    0: "e",
    1: "B",
    2: "G",
    3: "D",
    4: "A",
    5: "E"
    }
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
    
    #AZ E húron ez hanyadik fret lenne?
    fret_value = fret+note_offset
    
    note = notes[fret_value%12]
    print(f"A hang: {note}")
    return note



for fret,position in fret_position.items():
    print(fret,position)

root.mainloop()