import tkinter as tk
from tkinter import ttk
import piano_methods as pmt

root = tk.Tk()
root.title("Piano keyboard")
root.geometry("1400x700")
NOTES_DICT ={
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

#A KEYBOARD TERÜLETE----------------------------
WIDTH = 1300
HEIGHT = 200
keyboard = tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="white")
keyboard.pack(pady=20)

clicked_notes_piano = []
clicked_notes_guitar = []

#region- keyboard init
#DIMENSONS
keyboard_left = 20
keyboard_right = WIDTH-20
keyboard_dark_bottom = (3/5)*HEIGHT
#NOTE_ DIM
white_key_width = 40
dark_key_width = white_key_width/1.5
white_key_width=(keyboard_right-keyboard_left)/(4*7)
print(white_key_width)



#LINE DRAWING
#borders
keyboard.create_line(keyboard_left,0,keyboard_left,HEIGHT,width=3)
keyboard.create_line(keyboard_right,0,keyboard_right,HEIGHT,width=3)
keyboard.create_line(keyboard_left,HEIGHT,keyboard_right,HEIGHT,width=3)
#keys
keyboard_white_borders = {}
keyboard_dark_borders = {}
keyboard_ocatve_borders = [keyboard_left]
ocatve_border = keyboard_left
for j in range(4):
    keyboard_white_borders[j]=[ocatve_border]
    keyboard_dark_borders[j]=[]
    for i in range(7):
        x=white_key_width*(i+1)+keyboard_ocatve_borders[-1]
        ocatve_border = x #ha a ciklus véget ér akkor a legjobboldalibb border lesz
        if i in [0,1,3,4,5]:
            #white key
            keyboard.create_line(x,keyboard_dark_bottom,x,HEIGHT,width=2)
            #dark:
            dark_left_x=x-dark_key_width/2
            dark_rigth_x=x+dark_key_width/2
            # keyboard.create_line(dark_left_x,0,dark_left_x,keyboard_dark_bottom,width=2)
            # keyboard.create_line(dark_rigth_x,0,dark_rigth_x,keyboard_dark_bottom,width=2)
            # keyboard.create_line(dark_left_x,keyboard_dark_bottom,dark_rigth_x,keyboard_dark_bottom,width=3)
            keyboard.create_rectangle(dark_left_x,0,dark_rigth_x,keyboard_dark_bottom,fill="#949494",outline="black",width=2)
           
            keyboard_dark_borders[j].append([dark_left_x,dark_rigth_x]) 
        else:
            keyboard.create_line(x,0,x,HEIGHT,width=2)
        
        
        keyboard_white_borders[j].append(x)
    keyboard_ocatve_borders.append(ocatve_border)
#endregion
#----------------------------------------------



#GITÁRNYAK TERÜLETE-----------
#region
WIDTH_GUITAR = WIDTH
HEIGHT_GUITAR = 300
fretboard = tk.Canvas(root,width=WIDTH_GUITAR,height=HEIGHT_GUITAR,bg="white")
fretboard.pack()

guitar_neck_top_y = 20
guitar_neck_bottom_y = HEIGHT_GUITAR-guitar_neck_top_y
guitar_neck_nut = 100
guitar_neck_max_x= 1200

#NECK BORDERS
fretboard.create_line(0,guitar_neck_top_y,WIDTH,guitar_neck_top_y,width=3)
fretboard.create_line(0,guitar_neck_bottom_y,WIDTH,guitar_neck_bottom_y,width=3)
#NUT
fretboard.create_line(100, guitar_neck_top_y, 100, guitar_neck_bottom_y,width=3)

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
fret_position = [0,100] #további könnyebb hozzáférhetőséghez
i= 1
for fret_num,dist in fret_dist.items():
    x=left_fretboard_end+dist*fwc
    fretboard.create_line(x, top_fretboard_end, x, bottom_fretboard_end,width=3,fill="#545352")
    fret_position.append(x)
    i += 1

def fret_circle_single(fret_number):
    if fret_number<10:
        r=12
    else:
        r=10
    x=(fret_position[fret_number]+fret_position[fret_number+1])/2
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
    x=(fret_position[fret_number]+fret_position[fret_number+1])/2
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

#A HÚROK KATTINTÁSÁNAK (régebben pirossal jelölt) határai
string_border = [guitar_neck_top_y]
for i in range(len(string_position)-1):
    border = (string_position[i]+string_position[i+1])/2
    string_border.append(border)
string_border.append(guitar_neck_bottom_y)

# for border in string_border:
#     print(f"border: {border}")
#     fretboard.create_line(100,border,300,border,width=2,fill="red")

guitar_borders = {"fret":fret_position,  
                  "string":string_border}
#endregion
#---------------------------
#GITÁRNYAK FONTOS VÁLTOZÓI
print(fret_position)
print(string_border)





#print(keyboard_white_borders)
#print(keyboard_dark_borders)
#print(keyboard_ocatve_borders)



#-----------------------------
# FÜGGVÉNYEK

def draw_note_in_circle(center_x,center_y,note_text,radius=12,fill="green",tag = "clicked_notes" ):
    r=radius
    keyboard.create_oval(center_x-r, center_y-r,center_x+r, center_y+r,fill=fill,outline="black",width=2,
                                                     tags=tag)
    keyboard.create_text(center_x, center_y,text=note_text,fill="white",anchor="center", font=("Arial", 10),
                                                 tags=tag)

def draw_note_in_circle_guitar(center_x,center_y,note_text,radius=12,fill="green"):
    r=radius
    fretboard.create_oval(center_x-r, center_y-r,center_x+r, center_y+r,fill=fill,outline="black",width=2,
                                                     tags="clicked_notes")
    fretboard.create_text(center_x, center_y,text=note_text,fill="white",anchor="center", font=("Arial", 10),
                                                 tags="clicked_notes")
    
def keyboard_click(event):
    
    #OKTAV CHECK 
    for i in range(len(keyboard_ocatve_borders)-1):
         if event.x > keyboard_ocatve_borders[i] and event.x <= keyboard_ocatve_borders[i+1]:
            oktav = i # AZ OKTÁV 0-val kezdődik

    #NOTE_ CHECK
    is_clicked_dark = False
    if event.y <= keyboard_dark_bottom: # HA LEHETSÉGES HOGY FEKETÉT ÜTÜNK
        for i in range(len(keyboard_dark_borders[oktav])):
            if event.x > keyboard_dark_borders[oktav][i][0] and event.x < keyboard_dark_borders[oktav][i][1]:
                clicked_note =NOTES_DICT[i+10] #szimplán csak a notes_dict kódolása miatt
                is_clicked_dark = True
                note_ID = clicked_note+"_"+str(oktav+2)
                
    #HA NEM FEKETÉT ÜTÖTTÜNK LE
    if is_clicked_dark == False:
        for i in range(len(keyboard_white_borders[oktav])-1):
            if event.x > keyboard_white_borders[oktav][i] and event.x < keyboard_white_borders[oktav][i+1]:
                clicked_note = NOTES_DICT[i]
                note_ID = clicked_note+"_"+str(oktav+2)
                print(note_ID)

    #MEGNÉZZÜK HOGY HOZZÁADNI VAGY TÖRÖLNI KELL A NOTE_-OT
    if note_ID not in clicked_notes_piano:
        update_keyboard(note_ID)
        update_fretboard(note_ID)
    elif note_ID in clicked_notes_piano:
        keyboard.delete(note_ID)
        clicked_notes_piano.remove(note_ID)


def fretboard_click(event):

    #clicked string:
    string_borders = guitar_borders["string"]
    for i in range(len(string_borders)-1):
        if event.y > string_borders[i] and event.y< string_borders[i+1]:
            clicked_string = i

    #clicked fret:
    fret_borders = guitar_borders["fret"]
    for i in range(len(fret_borders)-1):
        if event.x > fret_borders[i] and event.x < fret_borders[i+1]:
            clicked_fret = i

    # A fret offset string alapján
    fret_offsets = {5:0,4:5,3:10,2:15,1:19,0:24} 
    note_indexes = {0: "E",1: "F",2: "F#",3: "G",4: "G#",5: "A",6: "A#",7: "B",8: "C",9: "C#",10: "D",11: "D#"}
    guitar_ocatve_borders = {0:8,1:20,2:32,3:44,4:56}
    clicked_fret_w_offset = clicked_fret+fret_offsets[clicked_string]
    clicked_note=note_indexes[(clicked_fret_w_offset)%12]
    for i in range(len(guitar_ocatve_borders)):
        if clicked_fret_w_offset < guitar_ocatve_borders[i]:
            oktav = i+2
            break
    note_ID = clicked_note+"_"+str(oktav)

    update_keyboard(note_ID)
    update_fretboard(note_ID,clicked_string=clicked_string)

def reset_notes():
    keyboard.delete("clicked_notes")
    fretboard.delete("clicked_notes")

def parse_noteID(note_ID):
    note,octave = note_ID.split("_")
    if "#" in note:
        is_sharp = True
    else:
        is_sharp = False
    octave = int(octave)
    return  {"note": note, "is_sharp":is_sharp,"octave":octave}

def update_keyboard(note_ID): # A HANGOK BERAZJOLÁSÁRA
    clicked_notes_piano.append(note_ID)
    note_ID_dict = parse_noteID(note_ID)
    oktav= note_ID_dict["octave"]-2 #A noteID a tényleges oktávot használja, de for ciklushoz ezt igazítani kell
    note =note_ID_dict["note"]
    is_sharp =note_ID_dict["is_sharp"]

    if is_sharp == False:
        note_index = next(key for key, value in NOTES_DICT.items() if value == note) #az adott note száma
        center_x=(keyboard_white_borders[oktav][note_index]+keyboard_white_borders[oktav][note_index+1])/2
        center_y=(keyboard_dark_bottom+HEIGHT)/2 
    else:
        note_index = next(key for key, value in NOTES_DICT.items() if value == note)-10 # a sharp-ok kódolása miatt
        center_x=(keyboard_dark_borders[oktav][note_index][0]+keyboard_dark_borders[oktav][note_index][1])/2
        center_y = (0+keyboard_dark_bottom)*(2/3) #keyboard_top és dark_bottom 2/3-a
    draw_note_in_circle(center_x,center_y,note,tag=note_ID)

def update_fretboard(note_ID,clicked_string=None):
    #ha meg van adva melyik húrn játszottuk le (tehár ha a gitárra nyomtam és nem a pianoról érkezik az info)
    #akkor arra a húrra rakja rá a hangot
    note_ID_dict = parse_noteID(note_ID)
    oktav= note_ID_dict["octave"]-2 #A noteID a tényleges oktávot használja, de for ciklushoz ezt igazítani kell
    note =note_ID_dict["note"]
    is_sharp =note_ID_dict["is_sharp"]
    note_indexes = {-4:"C",-3:"C#",-2:"D",-1:"D#",0: "E",1: "F",2: "F#",3: "G",4: "G#",5: "A",6: "A#",7: "B"} # "F#" -> 2
    note_index_raw = next(key for key, value in note_indexes.items() if value == note)
    note_w_okt_offset = note_index_raw + 12*oktav
    string_fret_offsets = {5:0,4:5,3:10,2:15,1:19,0:24} 
    print(f"clicked_note: {note_w_okt_offset}")

    #WORK IN PROGRESS-----------
    #HA PIANO KATTINTÁS HOZOTT IDE MINKET
    if clicked_string == None:
        
        print("piano")
        #MELYIK HÚROKON HANYADIKKÉNT VAN RAJTA
        note_on_string_at_fret = {}
        for i in range(6):
            string_base = string_fret_offsets[i]
            if note_w_okt_offset >= string_base and note_w_okt_offset <= (string_base+24):
                note_on_string_at_fret[i]=note_w_okt_offset-string_base

    #DONE-----------
    #HA A GITÁRRA KATTINTOTTUNK AKKOR ARRA A HÚRRA TEGYE AMIRE KATTINTOTTUNK
    else:
        string_borders = guitar_borders["string"]
        fret_borders = guitar_borders["fret"]
        clicked_fret = note_w_okt_offset-string_fret_offsets[clicked_string]
        print(f"húr: {clicked_string}, fret {clicked_fret}")
        center_x = (fret_borders[clicked_fret]+fret_borders[clicked_fret+1])/2
        center_y= (string_borders[clicked_string]+string_borders[clicked_string+1])/2
        draw_note_in_circle_guitar(center_x=center_x,center_y=center_y,note_text=note)






#-------------------------------



#--------------------------------
# 2026.10.05 0:06: - fretbordra kattintva a noteok helyesen megjelennek a pianon
# következő cél: pianora kattintva fretboardon mejelennek a hangok
#------------------------------




# Gombok területe
keyboard.bind("<Button-1>", keyboard_click)
fretboard.bind("<Button-1>", fretboard_click)
button_frame = ttk.Frame(root)
button_frame.pack(pady=0)
guess_the_note_button = ttk.Button(button_frame,text="Reset notes",command=reset_notes)
guess_the_note_button.grid(row=1,column=1,pady=10)










root.mainloop()