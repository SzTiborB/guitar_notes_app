import random
import tkinter as tk
from tkinter import ttk

def guitar_init(WIDTH,HEIGHT,fretboard):
    guitar_neck_top_y = 20
    guitar_neck_bottom_y = HEIGHT-guitar_neck_top_y
    guitar_neck_nut = 100
    guitar_neck_max_x= 1200

    #NECK BORDERS
    fretboard.create_line(0,guitar_neck_top_y,WIDTH,guitar_neck_top_y,width=5)
    fretboard.create_line(0,guitar_neck_bottom_y,WIDTH,guitar_neck_bottom_y,width=5)
    #NUT
    fretboard.create_line(100, 20, 100, 280,width=5)

    #fretboard határai:
    left_fretboard_end = guitar_neck_nut
    right_fretboard_end = WIDTH
    top_fretboard_end = guitar_neck_top_y
    bottom_fretboard_end = guitar_neck_bottom_y

    #fret-ek kreálása:
    fretboard_width = right_fretboard_end-left_fretboard_end-20 #ne a kép legszélén legyen a 24.fret
    #fret-ek egymástól távolsága:
    fret_dist = {
        1: 1.347,
        2: 2.618,
        3: 3.819,
        4: 4.951,
        5: 6.020,
        6: 7.029,
        7: 7.982,
        8: 8.881,
        9: 9.730,
        10: 10.531,
        11: 11.287,
        12: 12.000,
        13: 12.674,
        14: 13.309,
        15: 13.909,
        16: 14.476,
        17: 15.010,
        18: 15.515,
        19: 15.991,
        20: 16.441,
        21: 16.865,
        22: 17.265,
        23: 17.643,
        24: 18.000
    }
    #fret-window konstans
    fwc = fretboard_width/fret_dist[24]

    #FRET-EK NYAKRA HELYEZÉSE
    fret_position = {} #további könnyebb hozzáférhetőséghez
    i= 1
    for fret_num,dist in fret_dist.items():
        x=left_fretboard_end+dist*fwc
        fretboard.create_line(x, top_fretboard_end, x, bottom_fretboard_end,width=3,fill="#545352")
        fret_position[i]=x
        i += 1

    def fret_circle_single(fret_number):
        if fret_number<10:
            r=12
        else:
            r=10
        x=(fret_position[fret_number-1]+fret_position[fret_number])/2
        y=(top_fretboard_end+bottom_fretboard_end)/2
        fretboard.create_oval(
            x-r, y-r,
            x+r, y+r,
            fill="black",
            outline="black",
            width=2
        )
    def fret_circle_double(fret_number):
        r=10
        x=(fret_position[fret_number-1]+fret_position[fret_number])/2
        middle_y=(top_fretboard_end+bottom_fretboard_end)/2
        top_y = (middle_y+top_fretboard_end)/2
        bottom_y=(middle_y+bottom_fretboard_end)/2
        fretboard.create_oval(
            x-r, top_y-r-5,
            x+r, top_y+r-5,
            fill="black",
            outline="black",
            width=2
        )
        fretboard.create_oval(
            x-r, bottom_y-r+5,
            x+r, bottom_y+r+5,
            fill="black",
            outline="black",
            width=2
        )
    fret_circle_single(3)
    fret_circle_single(5)
    fret_circle_single(7)
    fret_circle_single(9)
    fret_circle_double(12)
    fret_circle_single(15)
    fret_circle_single(17)
    fret_circle_single(19)
    fret_circle_single(21)
    fret_circle_double(24)

    #A húrok elég sajátosan vannak elhelyezve a gitáron (szélső húr eléggé a szélén):
    top_fretboard_end = top_fretboard_end+20
    bottom_fretboard_end = bottom_fretboard_end-20
    #HÚRNEVEK RÁRAKÁSA
    def stringname(string_num):
        if string_num == 0:
            string_name = "e"
        elif string_num == 1:
            string_name = "B"
        elif string_num == 2:
            string_name = "G"
        elif string_num == 3:
            string_name = "D"
        elif string_num == 4:
            string_name ="A"
        elif string_num == 5:
            string_name ="E"
        fretboard.create_text(60, top_fretboard_end+(bottom_fretboard_end-top_fretboard_end)*((string_num)/5),
            text=string_name,
            fill="black",
            anchor="e", #a betű tetejének a közepe illesztődik
            font=("Arial", 20, "bold")
        )
        #Húr rárakása
        y =top_fretboard_end+(bottom_fretboard_end-top_fretboard_end)*((string_num)/5)
        fretboard.create_line(left_fretboard_end, y, right_fretboard_end, y,width=3,fill="#a3a3a3")
        return y
    string_position = {}
    for i in range(6):
        string_pos=stringname(i)
        string_position[i]=string_pos



    #vonal kreálás
    fretboard.create_line(100, 20, 100, 280,width=5)


    #kör középponttal
    # fretboard.create_oval(
    #     x-r, y-r,
    #     x+r, y+r,
    #     fill="red",
    #     outline="black",
    #     width=2
    # )

    #betűk rárakása
    # fretboard.create_text(
    #     50, top_fretboard_end,
    #     text="E",
    #     fill="black",
    #     anchor="n", #a betű tetejének a közepe illesztődik
    #     font=("Arial", 20, "bold")
    # )
    return fret_position,string_position



    #NOTE_
    note = string_list[clicked_string].note(clicked_fret)
    if detailed_return == False:
        return note
    elif detailed_return == True:
        return note,clicked_string,clicked_fret

def clicked_note(x,y,fret_position,string_list,detailed_return=False):
    top_fretboard_border = string_list[0].y-20
    bottom_fretboard_border = string_list[-1].y+20
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

    
class GuitarString:
    notes = {
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
    notes_sharp = {
    0: "E",
    1: "F",
    2: "F#",
    3: "G",
    4: "G#",
    5: "A",
    6: "A#",
    7: "B",
    8: "C",
    9: "C#",
    10: "D",
    11: "D#"}
    notes_flat = {
    0: "E",
    1: "F",
    2: "Gb",
    3: "G",
    4: "Ab",
    5: "A",
    6: "Bb",
    7: "B",
    8: "C",
    9: "Db",
    10: "D",
    11: "Eb"}
    def __init__(self, name, y, open_note):
        self.name = name
        self.y = y
        self.open_note = open_note
        self.border_y = None

    def set_border_y(self,y):
        self.border_y=y
    
    def note(self,fret,notation="both"):
        note_index = (fret+self.open_note) %12
        if notation == "sharp":
            return self.notes_sharp[note_index]

        elif notation == "flat":
            return self.notes_flat[note_index]
        else:
            return self.notes[note_index]


class ClickTheNoteGame:
    WIDTH = 1300
    HEIGHT = 300
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
    NOTE_COUNT_LIST = {
    "E": 14,
    "F": 12,
    "F#-Gb": 12,
    "G": 13,
    "G#-Ab": 12,
    "A": 13,
    "A#-Bb": 12,
    "B": 13,
    "C": 12,
    "C#-Bb": 12,
    "D": 13,
    "D#-Eb": 12}

    def __init__(self,root,string_list):
        self.random_note = self.NOTES[random.randint(0,11)]
        self.string_list = string_list
        #AZ ABLAK VÁLTOZÓI?
        self.fret_positions=None
        self.string_positions=None
        self.note_game_window = None
        self.note_game_fretboard = None
        #KIFEJEZETTEN A JÁTÉK VÁLTOZÓI
        self.guessed_note_count = 0
        self.note_count = self.NOTE_COUNT_LIST[self.random_note]
        

        # GITÁROS ABLAK KREÁLÁSA
        self.note_game_window = tk.Toplevel(root)
        self.note_game_window.title("Find the Note")
        self.note_game_window.geometry("1400x600")
        self.note_game_fretboard = tk.Canvas(self.note_game_window,width=self.WIDTH,height=self.HEIGHT,bg="white")
        self.note_game_fretboard.pack(pady=20)
        self.fret_position,self.string_position=guitar_init(self.WIDTH,self.HEIGHT,self.note_game_fretboard)
        #ABLAKRA GOMBOK
        ntgame_button_frame = ttk.Frame(self.note_game_window)
        ntgame_button_frame.pack(pady=20)
        self.ntgame_label = ttk.Label(ntgame_button_frame,text=f"A hang:{self.random_note}",font=("Arial", 30))
        self.ntgame_label.grid(row=0, column=0,pady=20)
        self.ntgame_how_many_notes_label =ttk.Label(ntgame_button_frame,
            text=f"Notes found:0/{self.note_count}",font=("Arial", 20))
        self.ntgame_how_many_notes_label.grid(row=1,column=0,pady=20)

        self.note_game_fretboard.bind("<Button-1>", self.fretboard_click)

    def fretboard_click(self,event):
        print("Hello")
        note,clicked_string,clicked_fret=clicked_note(event.x,event.y,
                                                      fret_position=self.fret_position,
                                                      string_list=self.string_list,
                                                      detailed_return=True)
                
        #ntgame_label.config(text=f"A hang {note}")
        print(f"random_note: {self.random_note} - clicked_note: {note}")

        y=self.string_position[clicked_string]
        r=12
        if clicked_fret == 0:
            x=80
        elif clicked_fret == 1:
            x=(self.fret_position[1]+100)/2
        else:
            x=(self.fret_position[clicked_fret]+self.fret_position[clicked_fret-1])/2

        if note == self.random_note: #HA JÓ A LENYOMOTT FRET
            self.note_game_fretboard.create_oval(x-r, y-r,x+r, y+r,fill="green",outline="black",width=2,tags="guessed_note")
            self.guessed_note_count += 1
            self.ntgame_how_many_notes_label.config(text=f"Notes found:{self.guessed_note_count}/{self.note_count}")
        else: #HA ROSSZ
            self.note_game_fretboard.create_oval(x-r, y-r,x+r, y+r,fill="red",outline="black",width=2,tags="guessed_note")
        #NOTE_ BELEÍRÁSA
        note_text = self.string_list[clicked_string].note(clicked_fret,notation="sharp")
        self.note_game_fretboard.create_text(x, y,text=note_text,fill="white",anchor="center", font=("Arial", 12))
