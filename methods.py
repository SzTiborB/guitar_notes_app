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

