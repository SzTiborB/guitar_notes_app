import tkinter as tk
import piano_methods as pmet
import threading
import json
import os

def interval_game_start(synth_connected,menu_window):


    game_window = tk.Toplevel(menu_window)

    piano = pmet.Piano(root=game_window)
    interval_game = pmet.Piano_Interval_Game(piano=piano,root=game_window,random_interval_count=3)




    #BEZÁRÁSKOR MENTSE KI AZ ÖSSZES LEJÁTSZOTT SKÁLÁT
    def on_closing():
        print("Colsing window")


    game_window.protocol("WM_DELETE_WINDOW", on_closing)