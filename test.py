import tkinter as tk
import piano_methods as pmet

root = tk.Tk()
root.title("Piano scale game")
root.geometry("1400x700")

piano = pmet.Piano(root=root)
scale_game = pmet.Piano_Scale_Game(piano=piano,root=root)

root.mainloop()