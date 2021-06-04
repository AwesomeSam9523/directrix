# Directric Bank
# Refer README.md for features and contributions

from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageFont, ImageDraw

def close_root():
    root.destroy()

def restore_root():
    if root.fs:
        root.attributes('-fullscreen', False)
        root.fs = False
        restore["text"] = "Maximize"
    else:
        root.attributes('-fullscreen', True)
        root.fs = True
        restore["text"] = "Restore"

root = Tk()
root.geometry(f"{root.wm_maxsize()[0]}x{root.wm_maxsize()[1]}")
root.attributes('-fullscreen', True)
root.fs = True

style = Style()
style.configure('Frame1.TFrame', background="#FF8F00")
style.configure('TButton', background="#FF8F00")

title = Frame(root, style="Frame1.TFrame")
title.grid(row=0, column=0, columnspan = 100, sticky="E")

close = Button(title, text="Close", command=close_root)
close.grid(row=0, column=1, sticky="E")

restore = Button(title, text="Restore", command=restore_root)
restore.grid(row=0, column=0, sticky="W")

root.mainloop()