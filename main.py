# Directric Bank
# Refer README.md for features and contributions

#create acc- random.randint(10**9, 10**10)
import random
import time, json, re
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageFont, ImageDraw, ImageTk
from functools import partial

namecheck = re.compile('^[a-z]+$', re.IGNORECASE)
pancheck = re.compile('^[a-z0-9]+$', re.IGNORECASE)
pswdcheck = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

def x(value):
    return int((root.wm_maxsize()[0]/1536)*value)

def y(value):
    return int((root.wm_maxsize()[1]/864)*value)

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
                dashboard(root.accountsdata[acc])
            else:
                status.configure(text="Incorrect Password!", fg="#FF0000")
                return
            found = True
            break
    if not found:
        status.configure(text="Username doesn't exist!", fg="#FF0000")

def cancelcreate(*args):
    login_field.place(x=x(95), y=y(350))
    login_field.focus_set()
    password_field.place(x=x(95), y=y(490))
    submit_login.place(x=x(85), y=y(600))
    submit_create.place(x=x(300), y=y(600))
    status.place(x=x(85), y=y(562))
    for i in args:
        i.place_forget()

    dashbg = Image.open("data/images/bg.png")
    dashbg = dashbg.resize(root.wm_maxsize())
    root.bgimg = ImageTk.PhotoImage(dashbg)
    bg_canvas.itemconfig(root.rootbgimage, image=root.bgimg)

def finalsubmit(fname, lname, email, age, pan, gender, aadhar, add1, add2, pswd, cpswd):
    g_fname = fname.get().replace(" ", "")
    g_lname = lname.get().replace(" ", "")
    g_email = email.get().replace(" ", "")
    g_age = age.get().replace(" ", "")
    g_pan = pan.get().replace(" ", "")
    g_gender = gender.get()
    g_aadhar = aadhar.get().replace(" ", "")
    g_add1 = add1.get()
    g_add2 = add2.get()
    g_pswd = pswd.get()
    g_cpswd = cpswd.get()

    if any([g_fname == "", g_lname == "", g_email == "", g_age == "", g_pan == "", g_gender == "", g_aadhar == "",
            g_add1 == "", g_add2 == "", g_pswd == "", g_cpswd == ""]):
        create_popup("Please make sure all the fields are filled!")
        return

    if (not namecheck.search(g_fname)) or (not namecheck.search(g_lname)):
        create_popup("Invalid Name! Use of only alphabets is allowed")
        return

    if ("@" not in g_email) or ("." not in g_email):
        create_popup("Invalid mail id! Please re-check")
        return

    try: g_age = int(g_age)
    except:
        create_popup("Age must be numeric only!")
        return

    if (len(g_pan) != 10) or (not pancheck.search(g_pan)):
        create_popup("Invalid PAN number!")
        return

    if len(g_aadhar) != 12:
        create_popup("Invalid Aadhar number!")
    try: g_aadhar = int(g_aadhar)
    except:
        create_popup("Invalid Aadhar number!")
        return

    if not pswdcheck.search(g_pswd):
        create_popup("Password should meet following criteria:\n"
                     "- Minimum 8 characters\n"
                     "- Must contain 1 uppercase letter\n"
                     "- Must contain 1 lowercase letter\n"
                     "- Must contain 1 symbol\n"
                     "- Must contain 1 digit")
        return

    if g_cpswd != g_pswd:
        create_popup("Passwords do not match!")
        return

def create_popup(text):
    messagebox.showwarning("Error", text)

def submit_data():
    login_field.place_forget()
    password_field.place_forget()
    submit_login.place_forget()
    submit_create.place_forget()
    status.place_forget()

    dashbg = Image.open("data/images/create_account.png")
    dashbg = dashbg.resize(root.wm_maxsize())
    root.bgimg = ImageTk.PhotoImage(dashbg)
    bg_canvas.itemconfig(root.rootbgimage, image=root.bgimg)

    fname = Entry(root, width=x(20), font=("Helvetica", 22))
    fname.place(x=x(400), y=y(164))
    lname = Entry(root, width=x(20), font=("Helvetica", 22))
    lname.place(x=x(1060), y=y(164))
    email = Entry(root, width=x(25), font=("Helvetica", 22))
    email.place(x=x(400), y=y(238))
    age = Entry(root, width=x(5), font=("Helvetica", 22))
    age.place(x=x(1060), y=y(238))
    pan = Entry(root, width=x(25), font=("Helvetica", 22))
    pan.place(x=x(400), y=y(312))
    gender = StringVar()
    male = Radiobutton(root, text="Male", variable=gender, value="M", font=("Helvetica", 20), bg="#ffffff")
    male.place(x=x(1060), y=y(305))
    female = Radiobutton(root, text="Female", variable=gender, value="F", font=("Helvetica", 20), bg="#ffffff")
    female.place(x=x(1160), y=y(305))
    other = Radiobutton(root, text="Other", variable=gender, value="O", font=("Helvetica", 20), bg="#ffffff")
    other.place(x=x(1290), y=y(305))
    aadhar = Entry(root, width=x(25), font=("Helvetica", 22))
    aadhar.place(x=x(400), y=y(386))
    add1 = Entry(root, width=x(30), font=("Helvetica", 22))
    add1.place(x=x(400), y=y(460))
    add2 = Entry(root, width=x(30), font=("Helvetica", 22))
    add2.place(x=x(400), y=y(534))
    pswd = Entry(root, width=x(25), font=("Helvetica", 22), show="*")
    pswd.place(x=x(540), y=y(662))
    cpswd = Entry(root, width=x(25), font=("Helvetica", 22), show="*")
    cpswd.place(x=x(540), y=y(736))

    final = Button(root, text="Open Account", font=("Arial", 22), width=x(14), bg="#37FF4E")
    final.place(x=x(1030), y=y(690))
    cancel = Button(root, text="Cancel", font=("Arial", 22), width=x(11), bg="#FF4E3F")
    cancel.place(x=x(1290), y=y(690))
    cancel.configure(command=partial(cancelcreate, fname, lname, email, age, pan, male, female, other, aadhar, add1, add2, pswd,
                        cpswd, final, cancel))
    final.configure(command=partial(finalsubmit, fname, lname, email, age, pan, gender, aadhar, add1, add2, pswd, cpswd))
    return
    usen = input('Pls enter a username: ')
    pas = input('Pls enter a password: ')
    email = input('Pls enter your email: ')
    add = input('Pls enter your address: ')
    age = int(input('Pls enter your age: '))
    gn = input('Pls enter your gender: ')
    mno= input('Pls enter your mobile number: ')
    pan= input('Pls enter your pan number: ')
    acn = input('Pls enter your aadhar card number: ')

    userid = random.randint(10**10, 10**11)
    root.accountsdata[str(userid)] = {"password":pas, "email":email, "address":add, "age":age, "Gender":gn, "MOBILE NUMBER": mno, "PAN NO.":pan, "AADHAR CARD NO.":acn}
    with open('data/accounts.json', 'w') as file:
        file.write(root.accountsdata)

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

def dashboard(data):
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
    userimg = ImageTk.PhotoImage(userimg)
    userimage = Canvas(root, width=x(50), height=y(50))
    userimage.create_image(0, 0, image=userimg, anchor="nw")
    userimage.place(x=x(25), y=y(40))

    welcome = Label(topframe, text=f"Welcome, {data['name']}!", font=("Arial", 20), bg="#B576FF")
    welcome.place(x=x(85), y=(20))

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

mainbg = Frame(root, width=root.wm_maxsize()[0], height=25)
mainbg.place(x=x(0), y=y(0))
close = Button(mainbg, text="Close", command=root.destroy)
close.place(x=(root.x- x(42)), y=y(2))
restore = Button(mainbg, text="Restore", command=restore_root)
restore.place(x=(root.x- x(93)), y=y(2))

login_field = Entry(root, width=x(25), font=("Helvetica", 22))
login_field.place(x=x(95), y=y(350))
login_field.focus_set()

password_field = Entry(root, width=x(25), font=("Helvetica", 22), show="*")
password_field.place(x=x(95), y=y(490))

submit_login = Button(root, text="Login", font=("Arial", 18), width=x(14), bg="#62E1FF", command=create_login)
submit_login.place(x=x(85), y=y(600))

submit_create = Button(root, text="Create Account", font=("Arial", 18), width=x(14), bg="#62E1FF", command=submit_data)
submit_create.place(x=x(300), y=y(600))

status = Label(root, font=("Helvetica", 16), bg="#ffffff", fg="#FF0000")
status.place(x=x(85), y=y(562))

with open("data/accounts.json", "r") as f:
    root.accountsdata = json.load(f)

with open("data/data.json", "r") as f:
    root.data = json.load(f)

def withdraw():
    userid = 8567375658
    var = root.data.get(str(userid))
    balance = var.get('balance')
    withd = int(input('Please enter the amount you want to withdraw = '))
    if withd > balance:
        print('!!! Insufficient Balance !!!')
    else:
        nam = balance - withd
        root.data[str(userid)] = {"balance":nam}
        savecode()

def savecode():
    with open('data/data.json', 'w') as file:
        file.write(json.dumps(root.data, indent=2))


def deposit():
    userid = 8567375658
    var = root.data.get(str(userid))
    balance = var.get('balance')
    dep = int(input("AMOUNT"))
    alloted = balance*(.25)
    if dep < alloted:
        n_balance = dep + balance
        print("THE AMOUNT HAS BEEN DEPOSITED YOUR NEW CURRENT BALANCE IS",n_balance)
        root.data[str(userid)] = {"balance": n_balance}
        savecode()
    elif dep > alloted :
        print("THE AMOUNT YOU WANT TO DEPOSIT IS LARGER THAN ALLOWED PLEASE REFER TO OUR TERMS AND CONDITIONS FOR FURTHER INFORMATION")


with open('data/data.json', 'w') as file:
    file.write(json.dumps(root.data,indent=2))

def loan():
    userid = 8567375658
    var = root.data.get(str(userid))
    balance = var.get('balance')
    exp = int(input("AMOUNT EXPECTED:"))
    inc = int(input("ANNUAL INCOME:"))
    credit_score = int(input("CREDIT SCORE:"))
    if credit_score < 700 :
        print("NOT ELIGIBLE BECAUSE YOUR CREDIT SCORE IS LESS")
    else :
        print("ELIGIBLE")
    job     = input("YOUR OCCUPATION")
    reason  = input("PURPOSE")
    by_when = input("BY WHEN DO YOU REQUIRE THE AMOUNT:")
    confirm_c = (inc/12)*(0.25)
    interet = (exp*(0.25))/24
    if confirm_c*(0.20) > interet:
        print("CONFIRMED")
    else :
        print("NOT CONFIRMED BECAUSE THE AMOUNT EXPECTED IS TOO LARGE")


root.mainloop()

