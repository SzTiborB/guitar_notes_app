import tkinter as tk
from tkinter import ttk
import random
import time


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
        #oktáv a keyboard handling-hez
        self.octave_keyboard_midi_offset = 0

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

    #HA A NOTE_ A KEYBOARDRA KLIKKELÉSBŐL ÉRKEZETT
    def update_keyboard_from_click(self,note_ID): # A HANGOK BERAZJOLÁSÁRA
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

    #A MIDI OKTÁVJAI NEM MINDIG STIMMELNEK, EZT KEZELENDŐ
    def update_keyboard_from_midi(self,note_ID,color="green"):
        self.clicked_notes_piano.append(note_ID)
        note_ID_dict = self.parse_noteID(note_ID)
        oktav=  note_ID_dict["octave"]-self.octave_keyboard_midi_offset########################################
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
        self.draw_note_in_circle(center_x,center_y,note,fill=color)

    def remove_notes_in_circle(self):
        self.keyboard.delete("clicked_notes")


class Piano_Scale_Game:
    def __init__(self,piano,root,already_completed_scales):
        piano:Piano
        #EHHEZ A PIANO KEYBOARD-HOZ TARTOZIK A JÁTÉK
        self.piano_object = piano
        WIDTH = 1300
        HEIGHT = 200
        #jatekhoz valtozok
        self.guessed_notes =[]
        self.done_scales = 0
        self.already_completed_scales = already_completed_scales #json file-ból betöltve


        #GOMBOK TERÜLETE----------
        #létrehozás
        self.button_board = tk.Frame(root,width=WIDTH,height=HEIGHT,bg="white")
        self.button_board.pack(pady=20,fill="x")

        #grid létrehozása és konfigurálása
        self.button_board.rowconfigure(0, weight=1) #3 sor
        self.button_board.rowconfigure(1, weight=1)
        self.button_board.rowconfigure(2, weight=1)
        self.button_board.columnconfigure(0, weight=1,minsize=200) # 2 oszlop
        self.button_board.columnconfigure(1, weight=4)
        self.button_board.columnconfigure(2, weight=1,minsize=200)
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
        #felső sor
        self.octave_keyboard_offset = tk.IntVar(value=0)
        spinbox = tk.Spinbox(self.right_1,from_=-3,to=3,
                             textvariable=self.octave_keyboard_offset,width=4,font=("Arial", 15))
        spinbox.pack(ipadx=10, ipady=10)
        self.scale_label = tk.Label(self.middle_1,text="",font=("Arial", 25))
        self.scale_label.pack()

        #középső sor
        self.show_scale_steps_var = tk.BooleanVar(value=False)
        scale_step_checkbox = tk.Checkbutton(self.left_2,text="Don't show scale steps",
                                    variable=self.show_scale_steps_var,command=self.on_scalestep_checkbox_changed)
        scale_step_checkbox.pack(pady=60)
        self.scale_steps_label = tk.Label(self.middle_2,text="",font=("Arial", 25))
        self.scale_steps_label.pack(pady=50)

        #alsó sor
        self.reset_button = tk.Button(self.middle_3,text="Reset",command=self.reset_game)
        self.reset_button.pack()
        self.done_scales_label = tk.Label(self.left_3,text=f"Scales done: {self.done_scales}",font=("Arial", 10))
        self.done_scales_label.pack()
        self.already_completed_scales_label =tk.Label(self.left_3,text=f"Alltime: {self.already_completed_scales}",
                                                      font=("Arial", 10))
        self.already_completed_scales_label.pack(pady=5)
        #GOMBOK TERÜLETE##################

        #méretváltozások letiltása -> innentől kezdve nem méretez automatikusan
        self.left_1.grid_propagate(False)
        self.middle_1.grid_propagate(False)
        self.right_1.grid_propagate(False)
        self.left_2.grid_propagate(False)
        self.middle_2.grid_propagate(False)
        self.right_2.grid_propagate(False)
        self.left_3.grid_propagate(False)
        self.middle_3.grid_propagate(False)
        self.right_3.grid_propagate(False)


        #RANDOM SKÁLA
        self.generate_random_scale()
        # self.random_scale_name = random_scale_name
        # self.random_scale_notes = random_scale_notes
        # self.random_scale_wh_steps = random_scale_wh_steps
        
        self.update_label_texts()
        
        
    def on_scalestep_checkbox_changed(self):
        print(f"valtozo: {self.octave_keyboard_offset.get()}")
        if self.show_scale_steps_var.get():
            self.scale_steps_label.config(text="")
        else:
            self.scale_steps_label.config(text=self.random_scale_wh_steps)


    def generate_random_scale(self):
        #skálák
        MUSIC_SCALES = {
            "Ionian (Major)":       ["W W H W W W H",  [2,2,1,2,2,2,1]],
            "Dorian":               ["W H W W W H W",  [2,1,2,2,2,1,2]],
            "Phrygian":             ["H W W W H W W",  [1,2,2,2,1,2,2]],
            "Lydian":               ["W W W H W W H",  [2,2,2,1,2,2,1]],
            "Mixolydian":           ["W W H W W H W",  [2,2,1,2,2,1,2]],
            "Aeolian (Natural Minor)":["W H W W H W W", [2,1,2,2,1,2,2]],
            "Locrian":              ["H W W H W W W",  [1,2,2,1,2,2,2]],

            "Harmonic Minor":       ["W H W W H WH H", [2,1,2,2,1,3,1]],
            "Melodic Minor":        ["W H W W W W H",  [2,1,2,2,2,2,1]],

            "Major Pentatonic":     ["W W WH W WH",     [2,2,3,2,3]],
            "Minor Pentatonic":     ["WH W W WH W",     [3,2,2,3,2]],

            "Blues":                ["WH W H H WH W",   [3,2,1,1,3,2]],

            "Whole Tone":           ["W W W W W W",     [2,2,2,2,2,2]],

            "Arabic":               ["H WH H W H WH H", [1,3,1,2,1,3,1]]
        }
        random_scale_weights = [
            100,  # Ionian (Major)
            3,   # Dorian
            3,   # Phrygian
            3,   # Lydian
            3,   # Mixolydian
            100,  # Aeolian (Natural Minor)
            3,   # Locrian
            3,   # Harmonic Minor
            3,   # Melodic Minor
            2,   # Major Pentatonic
            2,   # Minor Pentatonic
            2,   # Blues
            1,   # Whole Tone
            1    # Arabic
        ]
        random_scale = random.choices(list(MUSIC_SCALES.keys()),weights=random_scale_weights,k=1)[0] # a random skála (string)
        #hangok
        NOTE_DICT = {
            0: "C",
            1: "C#",
            2: "D",
            3: "D#",
            4: "E",
            5: "F",
            6: "F#",
            7: "G",
            8: "G#",
            9: "A",
            10: "A#",
            11: "B"
        }
        random_note_index = random.choices(list(NOTE_DICT.keys()),k=1)[0] # a random note indexe(int)
        random_note = NOTE_DICT[random_note_index] # a random note (string)
        random_scale_name = random_note+" - "+random_scale
        random_scale_wh_steps = MUSIC_SCALES[random_scale][0]
        random_scale_note_indexes = [random_note_index]
        for step_index in MUSIC_SCALES[random_scale][1]:
            random_scale_note_indexes.append(random_scale_note_indexes[-1]+step_index)
        random_scale_notes = []
        for note_index in random_scale_note_indexes:
            random_scale_notes.append(NOTE_DICT[(note_index%12)])


        print(f"A skala: {random_scale_name}") 
        print(f"A skala hangjai: {random_scale_notes}")
        print(f"A skala lepeskozei: {random_scale_wh_steps}")
        self.random_scale_name = random_scale_name
        self.random_scale_notes = random_scale_notes
        self.random_scale_wh_steps = random_scale_wh_steps
        # random_scale_notes -> ['A', 'A#', 'C', 'D', 'E', 'F', 'G', 'A']
        # random_scale_wh_steps -> "H W W W H W W"
    

    def update_label_texts(self):
        self.scale_label.config(text=self.random_scale_name)
        if self.show_scale_steps_var == False:
            self.scale_steps_label.config(text=self.random_scale_wh_steps)
        self.done_scales_label.config(text=f"Scales done: {self.done_scales}")
        self.already_completed_scales_label.config(
            text=f"Alltime: {self.already_completed_scales}")

    def set_piano_keyboard_offset(self,piano):
        piano : Piano
        piano.octave_keyboard_midi_offset = self.octave_keyboard_offset.get() + 3
        #print(f"Jelenlegi oktav: {self.octave_keyboard_offset.get()}")

    def parse_noteID(self,note_ID):
        note,octave = note_ID.split("_")
        if "#" in note:
            is_sharp = True
        else:
            is_sharp = False
        octave = int(octave)
        return  {"note": note, "is_sharp":is_sharp,"octave":octave}

    def is_note_in_random_scale(self,piano,guessed_noteID):
        noteID_dict = self.parse_noteID(guessed_noteID)
        note = noteID_dict["note"]
        piano : Piano
        print(f"guessed_note: {note}")
        if note in self.random_scale_notes:
            piano.update_keyboard_from_midi(guessed_noteID,color="green")
            if note not in self.guessed_notes:
                self.guessed_notes.append(note)
            #HA AZ UTOLSÓ (oktáv note) LEÜTJÜK A BILLENTYŰN:
            elif len(self.random_scale_notes)-len(self.guessed_notes) == 1 and note == self.random_scale_notes[0]:
                self.guessed_notes.append(note)
        else:
            piano.update_keyboard_from_midi(guessed_noteID,color="red")

    def reset_game(self):
        self.guessed_notes = []
        self.piano_object.remove_notes_in_circle()
        self.generate_random_scale()
        self.update_label_texts()


    #EZ FUSSON LE MINDEN CLICK/KEYBOARD LEUTESNEL
    def key_pressed(self,note_ID,piano):
        piano : Piano
        self.set_piano_keyboard_offset(piano)
        self.is_note_in_random_scale(guessed_noteID=note_ID,piano=piano) #note-bogyók berajzolása
        print(f"len guessed: {len(self.guessed_notes)}")
        print(f"len scale: {len(self.random_scale_notes)}")

        #HA A MINDEN NOTE_-OT ELTALÁLTUNK:
        if len(self.guessed_notes) == len(self.random_scale_notes):
            self.done_scales += 1
            self.already_completed_scales +=1
            self.scale_label.config(text="Correct")
            self.scale_label.update() #MANUALIS TKINTER UPDATE
            time.sleep(1)
            self.guessed_notes = []
            self.generate_random_scale()
            self.update_label_texts()
            self.piano_object.remove_notes_in_circle()


class Piano_Interval_Game:

    def __init__(self):
        pass

    def generate_random_intervals(self,interval_count):
        interval_dict = {
        1: "minor 2nd",
        2: "Major 2nd",
        3: "minor 3rd / aug 2nd",
        4: "Major 3rd",
        5: "Perfect 4th",
        6: "diminished 5th / Tritone",
        7: "Perfect 5th",
        8: "minor 6th / aug 5th",
        9: "Major 6th",
        10: "minor 7th",
        11: "Major 7th",
        12: "Octave"}

        NOTE_DICT = {
            0: "C",
            1: "C#",
            2: "D",
            3: "D#",
            4: "E",
            5: "F",
            6: "F#",
            7: "G",
            8: "G#",
            9: "A",
            10: "A#",
            11: "B"
        }

        random_intervals = sorted(random.sample(range(1, 13), interval_count))
        print(random_intervals)
        random_root_note_index = random.randint(0,11)
        random_root_note = NOTE_DICT[random_root_note_index%12]
        random_interval_indexes = [random_root_note_index]
        for interval in random_intervals:
            random_interval_indexes.append(random_root_note_index+interval)
        random_interval_notes = []
        for index in random_interval_indexes:
            note = NOTE_DICT[index%12]
            random_interval_notes.append(note)
        random_interval_labels = []
        #for---> interval label

        print(f"ROOT: {random_root_note}")
        print(f"Intervals: {random_interval_indexes}")
        print(f"ALL NOTES: {random_interval_notes}")
        

    
test_object=Piano_Interval_Game()
test_object.generate_random_intervals(3)        