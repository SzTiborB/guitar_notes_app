import random
import tkinter as tk
from tkinter import ttk
import sound_methods as sound
import time

FRET_INDEX_FREQ = {
    0:  82.41,     # E2
    1:  87.31,     # F2
    2:  92.50,     # F#2
    3:  98.00,     # G2
    4:  103.83,    # G#2
    5:  110.00,    # A2
    6:  116.54,    # A#2
    7:  123.47,    # B2
    8:  130.81,    # C3
    9:  138.59,    # C#3
    10: 146.83,    # D3
    11: 155.56,    # D#3

    12: 164.81,    # E3
    13: 174.61,    # F3
    14: 185.00,    # F#3
    15: 196.00,    # G3
    16: 207.65,    # G#3
    17: 220.00,    # A3
    18: 233.08,    # A#3
    19: 246.94,    # B3
    20: 261.63,    # C4
    21: 277.18,    # C#4
    22: 293.66,    # D4
    23: 311.13,    # D#4

    24: 329.63,    # E4
    25: 349.23,    # F4
    26: 369.99,    # F#4
    27: 392.00,    # G4
    28: 415.30,    # G#4
    29: 440.00,    # A4
    30: 466.16,    # A#4
    31: 493.88,    # B4
    32: 523.25,    # C5
    33: 554.37,    # C#5
    34: 587.33,    # D5
    35: 622.25,    # D#5

    36: 659.25,    # E5
    37: 698.46,    # F5
    38: 739.99,    # F#5
    39: 783.99,    # G5
    40: 830.61,    # G#5
    41: 880.00,    # A5
    42: 932.33,    # A#5
    43: 987.77,    # B5
    44: 1046.50,   # C6
    45: 1108.73,   # C#6
    46: 1174.66,   # D6
    47: 1244.51,   # D#6

    48: 1318.51    # E6
}

FRET_INDEX_NOTES = {
    0:  "E2",
    1:  "F2",
    2:  "F#2",
    3:  "G2",
    4:  "G#2",
    5:  "A2",
    6:  "A#2",
    7:  "B2",
    8:  "C3",
    9:  "C#3",
    10: "D3",
    11: "D#3",

    12: "E3",
    13: "F3",
    14: "F#3",
    15: "G3",
    16: "G#3",
    17: "A3",
    18: "A#3",
    19: "B3",
    20: "C4",
    21: "C#4",
    22: "D4",
    23: "D#4",

    24: "E4",
    25: "F4",
    26: "F#4",
    27: "G4",
    28: "G#4",
    29: "A4",
    30: "A#4",
    31: "B4",
    32: "C5",
    33: "C#5",
    34: "D5",
    35: "D#5",

    36: "E5",
    37: "F5",
    38: "F#5",
    39: "G5",
    40: "G#5",
    41: "A5",
    42: "A#5",
    43: "B5",
    44: "C6",
    45: "C#6",
    46: "D6",
    47: "D#6",

    48: "E6"
}

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

def clicked_fret_index(x,y,fret_position,string_list,detailed_return=False):
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


    #FRET
    fret_index = string_list[clicked_string].fret_index(clicked_fret)
    if detailed_return == False:
        return fret_index
    elif detailed_return == True:
        return fret_index,clicked_string,clicked_fret
    
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

    def fret_index(self,fret):
        fret_index =(fret+self.open_note)
        return fret_index

    def note_from_fretindex(self,fret_index,notation="both"):
        note_index = (fret_index) %12
        if notation == "sharp":
            return self.notes_sharp[note_index]

        elif notation == "flat":
            return self.notes_flat[note_index]
        else:
            return self.notes[note_index]

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
    NOTE_COUNT_WITH_OCTAVE = {
    "E2": 1,"F2": 1,"F#2": 1,"G2": 1,"G#2": 1,
    "A2": 2,"A#2": 2,"B2": 2,"C3": 2,"C#3": 2,
    "D3": 3,"D#3": 3,"E3": 3,"F3": 3,"F#3": 3,"G3": 4,
    "G#3": 4,"A3": 4,"A#3": 4,"B3": 5,"C4": 5,
    "C#4": 5,"D4": 5,"D#4": 5,"E4": 6,"F4": 5,
    "F#4": 5,"G4": 5,"G#4": 5,"A4": 5,"A#4": 4,
    "B4": 4,"C5": 4,"C#5": 4,"D5": 4,
    "D#5": 3,"E5": 3,"F5": 3,"F#5": 3,
    "G5": 3,"G#5": 2,"A5": 2,"A#5": 2,
    "B5": 2,"C6": 1,"C#6": 1,"D6": 1,
    "D#6": 1,"E6": 1}

    def __init__(self,root,string_list):
        self.random_note = FRET_INDEX_NOTES[random.randint(0,48)]
        self.string_list = string_list
        #AZ ABLAK VÁLTOZÓI?
        self.fret_positions=None
        self.string_positions=None
        self.note_game_window = None
        self.note_game_fretboard = None
        #KIFEJEZETTEN A JÁTÉK VÁLTOZÓI
        self.guessed_note_count = 0
        self.note_count = self.NOTE_COUNT_WITH_OCTAVE[self.random_note]
        #AHHOZ HOGY TÖBB KATTINTOTT NOTE_-OT LEHESSEN KEZELNI
        self.already_clicked_note = []
        #CHORDS-ok lejátszásához
        self.chord_notes =[]

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

        # create_index_tag -> egy stringet csinál amiben a STRING ÉS FRET benne van így egyértelműen
        # azonosítható a lefogott fret
        fret_index, clicked_string,clicked_fret=clicked_fret_index(event.x,event.y,fret_position=self.fret_position,
                                                                    string_list=self.string_list,detailed_return=True)
        note = FRET_INDEX_NOTES[fret_index]
            
        tag = self.create_index_tag(fret_index,clicked_string)
        print(f"random_note: {self.random_note} - clicked_note: {note}")
        print(f"A tag: {tag}")

        if tag not in self.already_clicked_note: #----------IF ----------
            self.already_clicked_note.append(tag)
            self.chord_notes.append(fret_index)

            y=self.string_position[clicked_string]
            r=12
            if clicked_fret == 0:
                x=80
            elif clicked_fret == 1:
                x=(self.fret_position[1]+100)/2
            else:
                x=(self.fret_position[clicked_fret]+self.fret_position[clicked_fret-1])/2

            if note == self.random_note: #HA JÓ A LENYOMOTT FRET
                self.note_game_fretboard.create_oval(x-r, y-r,x+r, y+r,fill="green",outline="black",width=2,
                                                     tags=tag)
                self.guessed_note_count += 1
                self.ntgame_how_many_notes_label.config(text=f"Notes found:{self.guessed_note_count}/{self.note_count}")
                sound.play_chord(self.chord_notes)
            else: #HA ROSSZ
                self.note_game_fretboard.create_oval(x-r, y-r,x+r, y+r,fill="red",outline="black",width=2,
                                                     tags=tag)
                sound.play_chord(self.chord_notes)
            #NOTE_ BELEÍRÁSA
            note_text = self.string_list[clicked_string].note(clicked_fret,notation="sharp")
            self.note_game_fretboard.create_text(x, y,text=note_text,fill="white",anchor="center", font=("Arial", 12),
                                                 tags=tag)

            
        else:
            self.already_clicked_note.remove(tag)
            self.note_game_fretboard.delete(self.create_index_tag(fret_index,clicked_string))
            self.chord_notes.remove(fret_index)
            print(f"{self.create_index_tag(fret_index,clicked_string)}")
        #------------------------------------------------------------------------------- IF END -----------


        #-------------- HA SIKERÜLT ---------------
        if self.guessed_note_count == self.note_count:
            self.ntgame_label.config(text=" YOU WIN ")
            self.note_game_window.update_idletasks()
            time.sleep(2)
            #------- RESET THE GAME
            for item in self.already_clicked_note:
                self.note_game_fretboard.delete(item)
            self.random_note = FRET_INDEX_NOTES[random.randint(0,48)]
            self.already_clicked_note = []
            self.guessed_note_count = 0
            self.note_count = self.NOTE_COUNT_WITH_OCTAVE[self.random_note]
            self.chord_notes =[]
        #-----------HA SIKERÜLT END -------------





    def create_index_tag(self,fret_index,clicked_string):
        text = "guessed_note_"+str(fret_index)+"_"+str(clicked_string)
        return text


class FreeChordGame:
    WIDTH = 1300
    HEIGHT = 300
    NOTE_COUNT_WITH_OCTAVE = {
    "E2": 1,"F2": 1,"F#2": 1,"G2": 1,"G#2": 1,
    "A2": 2,"A#2": 2,"B2": 2,"C3": 2,"C#3": 2,
    "D3": 3,"D#3": 3,"E3": 3,"F3": 3,"F#3": 3,"G3": 4,
    "G#3": 4,"A3": 4,"A#3": 4,"B3": 5,"C4": 5,
    "C#4": 5,"D4": 5,"D#4": 5,"E4": 6,"F4": 5,
    "F#4": 5,"G4": 5,"G#4": 5,"A4": 5,"A#4": 4,
    "B4": 4,"C5": 4,"C#5": 4,"D5": 4,
    "D#5": 3,"E5": 3,"F5": 3,"F#5": 3,
    "G5": 3,"G#5": 2,"A5": 2,"A#5": 2,
    "B5": 2,"C6": 1,"C#6": 1,"D6": 1,
    "D#6": 1,"E6": 1}

    def __init__(self,root,string_list):
        self.string_list = string_list
        #AZ ABLAK VÁLTOZÓI?
        self.fret_positions=None
        self.string_positions=None
        self.note_game_window = None
        self.note_game_fretboard = None

        #AHHOZ HOGY TÖBB KATTINTOTT NOTE_-OT LEHESSEN KEZELNI
        self.already_clicked_note = []
        #CHORDS-ok lejátszásához
        self.chord_notes =[]

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
        self.ntgame_label = ttk.Label(ntgame_button_frame,text=f"Clicked note: {""}",font=("Arial", 30))
        self.ntgame_label.grid(row=0, column=0,pady=20)
        
        self.play_chord_button = ttk.Button(ntgame_button_frame,text="Play the chord",command=self.play_chord)
        self.play_chord_button.grid(row=1,column=0,pady=10)

        self.note_game_fretboard.bind("<Button-1>", self.fretboard_click)

    def play_chord(self):
        if len(self.chord_notes) >0:
            sound.play_chord(self.chord_notes)

    def fretboard_click(self,event):

        # create_index_tag -> egy stringet csinál amiben a STRING ÉS FRET benne van így egyértelműen
        # azonosítható a lefogott fret
        fret_index, clicked_string,clicked_fret=clicked_fret_index(event.x,event.y,fret_position=self.fret_position,
                                                                    string_list=self.string_list,detailed_return=True)
        note = FRET_INDEX_NOTES[fret_index]
            
        tag = self.create_index_tag(fret_index,clicked_string)

        if tag not in self.already_clicked_note: #----------IF ----------
            self.already_clicked_note.append(tag)
            self.chord_notes.append(fret_index)

            y=self.string_position[clicked_string]
            r=12
            if clicked_fret == 0:
                x=80
            elif clicked_fret == 1:
                x=(self.fret_position[1]+100)/2
            else:
                x=(self.fret_position[clicked_fret]+self.fret_position[clicked_fret-1])/2

            #ZÖLD BOGYÓ
            self.note_game_fretboard.create_oval(x-r, y-r,x+r, y+r,fill="green",outline="black",width=2,
                                                    tags=tag)
            #NOTE_ BELEÍRÁSA
            note_text = self.string_list[clicked_string].note(clicked_fret,notation="sharp")
            self.note_game_fretboard.create_text(x, y,text=note_text,fill="white",anchor="center", font=("Arial", 12),
                                                 tags=tag)
            self.ntgame_label.config(text=f"Clicked note: {note_text}")

            #EGY HANG LEJÁTSZÁSA LEHELYEZÉSKOR
            sound.play_chord([fret_index])


            
        else:
            self.already_clicked_note.remove(tag)
            self.note_game_fretboard.delete(self.create_index_tag(fret_index,clicked_string))
            self.chord_notes.remove(fret_index)
            print(f"{self.create_index_tag(fret_index,clicked_string)}")
        #------------------------------------------------------------------------------- IF END -----------


    def create_index_tag(self,fret_index,clicked_string):
        text = "guessed_note_"+str(fret_index)+"_"+str(clicked_string)
        return text
