import tkinter as tk
from tkinter import ttk
import methods as mt
import random
root = tk.Tk()
root.title("Guitar Trainer")
root.geometry("1400x600")
NOTES= {
    0: "E",
    1: "F",
    2: "F#-Gb",
    3: "G",
    4: "G#-Ab",
    5: "A",
    6: "A#-Bb",
    7: "B",
    8: "C",
    9: "C#-Db",
    10: "D",
    11: "D#-Eb"}

# -------------------------
# Gitárnyak területe
# -------------------------
#AZ ALAP FRETBOARD
WIDTH = 1300
HEIGHT = 300
fretboard = tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="white")

#FELRAJZOLJA A GITÁRT, FRET ÉS STRING POZÍCIÓKAT ELTÁROLJUK -> kattintások-hangokhoz rendelése
fret_position,string_position=mt.guitar_init(WIDTH,HEIGHT,fretboard)
fretboard.pack(pady=20)
#-------------------------





#-------------------------------
# GOMB FÜGGVÉNYEK
#-----------------------------
def switch1_changed():
    if switch1_var.get():
        #print("ON")
        write_notes_on_fretboard()
        # pl. összes hang megjelenítése
    else:
        #print("Off")
        fretboard.delete("note_in_circle")
        # pl. hangok eltüntetése

def fretboard_click(event):
    #print("x:", event.x)
    #print("y:", event.y)
    note=clicked_note(event.x,event.y)
    
    kezdo_label.config(text=f"A hang {note}")
fretboard.bind("<Button-1>", fretboard_click)

#-------------------------------------------------------------------------------------------------
def start_note_game():
    note_game = mt.ClickTheNoteGame(root=root,string_list=string_list)

def free_chord_game():
    chord_game = mt.FreeChordGame(root=root,string_list=string_list)
#---------------------------------------------------------------------------------------------------------





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

#BUTTON
guess_the_note_button = ttk.Button(button_frame,text="Find the note game",command=start_note_game)
guess_the_note_button.grid(row=1,column=1,pady=20)
chords_game_button = ttk.Button(button_frame,text="Free Chord game",command=free_chord_game)
chords_game_button.grid(row=2,column=1,pady=20)
# SWITCH
switch1_var = tk.BooleanVar(value=False)
switch1 = ttk.Checkbutton(button_frame,text="Show notes on fretboard",
                         variable=switch1_var,command=switch1_changed)
switch1.grid(row=1,column=0,pady=20)
#--------------------------







#----------------------------------
# GITÁR HÚROK LÉTREHOZÁSA CLASS-szal
#region
string_list = []
string_e = mt.GuitarString("e",string_position[0],24)
string_B = mt.GuitarString("B",string_position[1],19)
string_G = mt.GuitarString("G",string_position[2],15)
string_D = mt.GuitarString("D",string_position[3],10)
string_A = mt.GuitarString("D",string_position[4],5)
string_E = mt.GuitarString("E",string_position[5],0)
string_list.append(string_e)
string_list.append(string_B)
string_list.append(string_G)
string_list.append(string_D)
string_list.append(string_A)
string_list.append(string_E)

# A GITÁR HANGOK KATTINTÁS-ÉRZÉKELÉSÉNEK PIROS HATÁRAI
top_fretboard_border = string_list[0].y-20
bottom_fretboard_border = string_list[-1].y+20
for i in range(len(string_list)-1):
    border_y=(string_list[i].y+string_list[i+1].y)/2
    string_list[i].set_border_y(border_y)
    fretboard.create_line(100, border_y, 1300, border_y,width=2,fill="red")
string_list[5].set_border_y(bottom_fretboard_border)
#endregion
#----------------------------------------------------


#-----------------------------------
# FÜGGVÉNYEK
#----------------------------------


def clicked_note(x,y,detailed_return=False):

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
    string_done = False
    if y < top_fretboard_border:
        clicked_string = None
        string_done = True
    elif y > bottom_fretboard_border:
        clicked_string = None
        string_done = True
    if string_done == False:
        for i in range(len(string_list)):
            if y < string_list[i].border_y:
                clicked_string = i
                break
    #--------------------

    #NOTE_
    note = string_list[clicked_string].note(clicked_fret)
    if detailed_return == False:
        return note
    elif detailed_return == True:
        return note,clicked_string,clicked_fret

def write_notes_on_fretboard():
    for string in string_list:
        string : mt.GuitarString
        for j in range(24):
            i=j+1
            note = string.note(i,notation="sharp")
            y=string.y
            if i == 1:
                elozo_fret = 100
                kovetkezo_fret = fret_position[1]
                x=(kovetkezo_fret+elozo_fret)/2
            else:
                elozo_fret = fret_position[i-1]
                kovetkezo_fret=fret_position[i]
                x=(elozo_fret+kovetkezo_fret)/2
            r=10
            fretboard.create_oval(
            x-r, y-r,
            x+r, y+r,
            fill="white",
            outline="black",
            width=2,
            tags="note_in_circle"
        )
            fretboard.create_text(x, y,
                        text=note,
                        fill="black",
                        anchor="center", #a betű tetejének a közepe illesztődik
                        font=("Arial", 10, "bold"),
                        tags= "note_in_circle"
                    )
#--------------------------------


            
root.mainloop()