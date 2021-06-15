# Directric Bank
# Refer README.md for features and contributions
"""
Vatsy:

[
(col1, col2)
()
()
]

"""
def create_login(username, password):
    with open("data/login.csv", "r") as file:
        accounts = csv.reader(file)

def use_login(username, password):
    rows = []
    with open("data/login.csv", "r") as file:
        accounts = csv.DictReader(file)
        for acc in accounts:
            print(acc)


from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk
import csv

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

bg = Image.open("data/images/bg.png")
bg = bg.resize(root.wm_maxsize())
img = ImageTk.PhotoImage(bg)
bg_canvas = Canvas(root, width=root.wm_maxsize()[0],
                   height=root.wm_maxsize()[1])
bg_canvas.grid(row=0, column=0)
bg_canvas.create_image(0, 0, image=img, anchor="nw")

mainbg = Frame(root, bg="#72adfb")
mainbg.grid(row=0, column=0, sticky="NE", pady=3, padx=3)

close = Button(mainbg, text="Close", command=root.destroy)
close.grid(row=0, column=1, padx=3)
restore = Button(mainbg, text="Restore", command=restore_root)
restore.grid(row=0, column=0)

login_field = Entry()
use_login("user", "pass")
#root.mainloop()