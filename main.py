# Directric Bank
# Refer README.md for features and contributions

#create acc- random.randint(10**9, 10**10)
import time, json
from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk
import csv

def x(value):
    return int((1536/root.wm_maxsize()[0])*value)

def y(value):
    return int((864/root.wm_maxsize()[1])*value)

def create_login():
    username = login_field.get()
    password = password_field.get()
    status.configure(text="")
    if username == "":
        status.configure(text="Username cannot be blank!")
        return
    if password == "":
        status.configure(text="Password cannot be blank!")
        return
    if len(username.split(" ")) != 1 or len(password.split(" ")) != 1:
        status.configure(text="Username/Password cannot contain spaces")
        return

    found = False
    for acc in root.accountsdata.keys():
        if acc == username.lower():
            if root.accountsdata[acc]["password"] == password:
                dashboard()
            else:
                status.configure(text="Incorrect Password!", fg="#FF0000")
                return
            found = True
            break
    if not found:
        status.configure(text="Username doesn't exist!", fg="#FF0000")

def create_acc():
    import csv
    from csv import writer

    fields = ['Username', 'Password']

    usen = input('Pls enter a username: ')
    pas = input('Pls enter a password: ')
    List = ['usen', 'pas']

    with open('data/login.csv', 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)

        # writing headers (field names)
        writer.writeheader()

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(List)

        # Close the file object
        f_object.close()



def restore_root():
    if root.fs:
        root.attributes('-fullscreen', False)
        root.fs = False
        restore["text"] = "Maximize"
        restore.place(x=x(root.x - x(110)), y=y(2))
        close.place(x=x(root.x - x(47)), y=y(2))
    else:
        root.attributes('-fullscreen', True)
        root.fs = True
        restore["text"] = "Restore"
        restore.place(x=x(root.x - x(93)), y=y(2))
        close.place(x=x(root.x - x(42)), y=y(2))

def dashboard():
    login_field.place_forget()
    password_field.place_forget()
    submit_login.place_forget()
    submit_create.place_forget()
    status.place_forget()
    dashbg = Image.open("data/images/dashboard.png")
    dashbg = dashbg.resize(root.wm_maxsize())
    root.bgimg = ImageTk.PhotoImage(dashbg)
    bg_canvas.itemconfig(root.rootbgimage, image=root.bgimg)

    #=========== ACTUAL DASHBOARD ==============

    topframe = Frame(root, width=root.wm_maxsize()[0], height=80, bg="#B576FF")
    topframe.place(x=0, y=y(25))

    userimg = Image.open("data/images/user.png").resize((x(40), y(40)))

root = Tk()
root.geometry(f"{root.wm_maxsize()[0]}x{root.wm_maxsize()[1]}")
root.x = root.wm_maxsize()[0]
root.y = root.wm_maxsize()[1]
root.attributes('-fullscreen', True)
root.fs = True
bg = Image.open("data/images/bg.png")
bg = bg.resize(root.wm_maxsize())
root.bgimg = ImageTk.PhotoImage(bg)

bg_canvas = Canvas(root, width=root.x, height=root.wm_maxsize()[1])
bg_canvas.place(x=x(0), y=y(0))
root.rootbgimage = bg_canvas.create_image(0, 0, image=root.bgimg, anchor="nw")
print(root.rootbgimage, type(root.rootbgimage))

mainbg = Frame(root, width=root.wm_maxsize()[0], height=25)
mainbg.place(x=x(0), y=y(0))

close = Button(mainbg, text="Close", command=root.destroy)
close.place(x=x(root.x- x(42)), y=y(2))
restore = Button(mainbg, text="Restore", command=restore_root)
restore.place(x=x(root.x- x(93)), y=y(2))

login_field = Entry(root, width=25, font=("Helvetica", 22))
login_field.place(x=x(95), y=y(350))
login_field.focus_set()

password_field = Entry(root, width=25, font=("Helvetica", 22), show="*")
password_field.place(x=x(95), y=y(490))

submit_login = Button(root, text="Login", font=("Arial", 18), width=x(14), bg="#62E1FF", command=create_login)
submit_login.place(x=x(85), y=y(600))

submit_create = Button(root, text="Create Account", font=("Arial", 18), width=x(14), bg="#62E1FF")
submit_create.place(x=x(300), y=y(600))

status = Label(root, font=("Helvetica", 16), bg="#ffffff", fg="#FF0000")
status.place(x=x(85), y=y(562))

with open("data/accounts.json", "r") as f:
    root.accountsdata = json.load(f)

root.mainloop()