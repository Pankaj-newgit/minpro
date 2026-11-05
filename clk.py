from tkinter import Tk, Label
from time import strftime

root = Tk()
clock = Label(root, font=("Arial", 48), padx=20, pady=10)
clock.pack()

def update():
    clock.config(text=strftime("%H:%M:%S"))
    root.after(1000, update)

update()
root.mainloop()