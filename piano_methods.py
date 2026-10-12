import tkinter as tk
from tkinter import ttk
import midi_handling
import threading


class Piano():

    def __init__(self,root):
        #A KEYBOARD TERÜLETE----------------------------
        WIDTH = 1300
        HEIGHT = 200
        self.HEIGHT = 200
        self.clicked_notes_piano = []
        self.NOTES_DICT ={
                0:"C",
                1:"D",
                2:"E",
                3:"F",
                4:"G",
                5:"A",
                6:"B",
                10:"C#",
                11:"D#",
                12:"F#",
                13:"G#",
                14:"A#"}
        self.keyboard = tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="white")
        self.keyboard.pack(pady=20)

        #region- keyboard init
        #DIMENSONS
        keyboard_left = 20
        keyboard_right = WIDTH-20
        self.keyboard_dark_bottom = (3/5)*HEIGHT
        #NOTE_ DIM
        white_key_width = 40
        dark_key_width = white_key_width/1.5
        white_key_width=(keyboard_right-keyboard_left)/(4*7)

        #GOMBOK TERÜLETE----------
        #létrehozás
        self.button_board = tk.Frame(root,width=WIDTH,height=HEIGHT,bg="white")
        self.button_board.pack(pady=20,fill="x")

        #grid létrehozása és konfigurálása
        self.button_board.rowconfigure(0, weight=1) #3 sor
        self.button_board.rowconfigure(1, weight=1)
        self.button_board.rowconfigure(2, weight=1)
        self.button_board.columnconfigure(0, weight=1) # 2 oszlop
        self.button_board.columnconfigure(1, weight=4)
        self.button_board.columnconfigure(2, weight=1)
        self.left_1 = tk.Frame(self.button_board)
        self.middle_1 = tk.Frame(self.button_board)
        self.right_1 = tk.Frame(self.button_board)
        self.left_2 = tk.Frame(self.button_board)
        self.middle_2 = tk.Frame(self.button_board)
        self.right_2 = tk.Frame(self.button_board)
        self.left_3 = tk.Frame(self.button_board)
        self.middle_3 = tk.Frame(self.button_board)
        self.right_3 = tk.Frame(self.button_board)
        self.left_1.grid(row=0, column=0, sticky="nsew")
        self.middle_1.grid(row=0, column=1, sticky="nsew")
        self.right_1.grid(row=0,column=2,sticky="nsew")
        self.left_2.grid(row=1, column=0, sticky="nsew")
        self.middle_2.grid(row=1, column=1, sticky="nsew")
        self.right_2.grid(row=1,column=2,sticky="nsew")
        self.left_3.grid(row=2, column=0, sticky="nsew")
        self.middle_3.grid(row=2, column=1, sticky="nsew")
        self.right_3.grid(row=2,column=2,sticky="nsew")

        #grid elemei gombok-labelek-checkboxok
        checkbox = tk.Checkbutton(self.left_1,text="Hangok mutatása")
        checkbox.pack()

        self.note_label = tk.Label(self.middle_1,text="C#4",font=("Arial", 25))
        self.note_label.place(relx=0.5,rely=0.5,anchor="center")

        self.note_label_right = tk.Label(self.right_1,text="  ",font=("Arial", 25)) #jobb oldalra egy label
        self.note_label_right.pack()


     
        #GOMBOK TERÜLETE##################



        #LINE DRAWING
        #borders
        self.keyboard.create_line(keyboard_left,0,keyboard_left,HEIGHT,width=3)
        self.keyboard.create_line(keyboard_right,0,keyboard_right,HEIGHT,width=3)
        self.keyboard.create_line(keyboard_left,HEIGHT,keyboard_right,HEIGHT,width=3)
        #keys
        self.keyboard_white_borders = {}
        self.keyboard_dark_borders = {}
        self.keyboard_ocatve_borders = [keyboard_left]
        ocatve_border = keyboard_left
        for j in range(4):
            self.keyboard_white_borders[j]=[ocatve_border]
            self.keyboard_dark_borders[j]=[]
            for i in range(7):
                x=white_key_width*(i+1)+self.keyboard_ocatve_borders[-1]
                ocatve_border = x #ha a ciklus véget ér akkor a legjobboldalibb border lesz
                if i in [0,1,3,4,5]:
                    #white key
                    self.keyboard.create_line(x,self.keyboard_dark_bottom,x,HEIGHT,width=2)
                    #dark:
                    dark_left_x=x-dark_key_width/2
                    dark_rigth_x=x+dark_key_width/2
                    # keyboard.create_line(dark_left_x,0,dark_left_x,keyboard_dark_bottom,width=2)
                    # keyboard.create_line(dark_rigth_x,0,dark_rigth_x,keyboard_dark_bottom,width=2)
                    # keyboard.create_line(dark_left_x,keyboard_dark_bottom,dark_rigth_x,keyboard_dark_bottom,width=3)
                    self.keyboard.create_rectangle(dark_left_x,0,dark_rigth_x,self.keyboard_dark_bottom,
                                                   fill="#949494",outline="black",width=2)
                
                    self.keyboard_dark_borders[j].append([dark_left_x,dark_rigth_x]) 
                else:
                    self.keyboard.create_line(x,0,x,HEIGHT,width=2)
                
                
                self.keyboard_white_borders[j].append(x)
            self.keyboard_ocatve_borders.append(ocatve_border)
        #endregion
        #----------------------------------------------


    def draw_note_in_circle(self,center_x,center_y,note_text,radius=12,fill="green",tag = "clicked_notes" ):
        r=radius
        self.keyboard.create_oval(center_x-r, center_y-r,center_x+r, center_y+r,fill=fill,outline="black",width=2,
                                                        tags=tag)
        self.keyboard.create_text(center_x, center_y,text=note_text,fill="white",anchor="center", font=("Arial", 10),
                                                    tags=tag)


    def parse_noteID(self,note_ID):
        note,octave = note_ID.split("_")
        if "#" in note:
            is_sharp = True
        else:
            is_sharp = False
        octave = int(octave)
        return  {"note": note, "is_sharp":is_sharp,"octave":octave}


    def update_keyboard(self,note_ID): # A HANGOK BERAZJOLÁSÁRA
        self.clicked_notes_piano.append(note_ID)
        note_ID_dict = self.parse_noteID(note_ID)
        oktav= note_ID_dict["octave"]-2 #A noteID a tényleges oktávot használja, de for ciklushoz ezt igazítani kell
        note =note_ID_dict["note"]
        is_sharp =note_ID_dict["is_sharp"]

        if is_sharp == False:
            note_index = next(key for key, value in self.NOTES_DICT.items() if value == note) #az adott note száma
            center_x=(self.keyboard_white_borders[oktav][note_index]+self.keyboard_white_borders[oktav][note_index+1])/2
            center_y=(self.keyboard_dark_bottom+self.HEIGHT)/2 
        else:
            note_index = next(key for key, value in self.NOTES_DICT.items() if value == note)-10 # a sharp-ok kódolása miatt
            center_x=(self.keyboard_dark_borders[oktav][note_index][0]+self.keyboard_dark_borders[oktav][note_index][1])/2
            center_y = (0+self.keyboard_dark_bottom)*(2/3) #keyboard_top és dark_bottom 2/3-a
        self.draw_note_in_circle(center_x,center_y,note,tag=note_ID)


