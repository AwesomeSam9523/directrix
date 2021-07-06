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

def savedata():
    with open('data/data.json', 'w') as file:
        file.write(json.dumps(root.data, indent=2))

    with open('data/accounts.json', 'w') as acc:
        acc.write(json.dumps(root.accountsdata, indent=2))

    with open('data/statements.json', 'w') as st:
        st.write(json.dumps(root.statements, indent=2))

def create_login():
    username = login_field.get()
    password = password_field.get()
    status.configure(text="")
    status.place(x=x(85), y=y(562))
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
            if root.accountsdata[acc]["pswd"] == password:
                dashboard(root.accountsdata[acc], (login_field, password_field, submit_login, submit_create, status))
            else:
                status.configure(text="Incorrect Password!", fg="#FF0000")
                return
            found = True
            break
    if not found:
        status.configure(text="Username doesn't exist!", fg="#FF0000")

def showhomepage(*args):
    login_field.place(x=x(95), y=y(350))
    login_field.focus_set()
    password_field.place(x=x(95), y=y(490))
    submit_login.place(x=x(85), y=y(600))
    submit_create.place(x=x(300), y=y(600))
    for i in args:
        i.place_forget()

    dashbg = Image.open("data/images/bg.png")
    dashbg = dashbg.resize(root.wm_maxsize())
    root.bgimg = ImageTk.PhotoImage(dashbg)
    bg_canvas.itemconfig(root.rootbgimage, image=root.bgimg)

    password_field.delete(0, END)
    login_field.delete(0, END)
    cacheid = root.cache.get("id")
    if cacheid is not None:
        root.cache["skip"] = False
        cacheupdate()
        login_field.insert(0, cacheid)
        password_field.focus_set()
    else: login_field.focus_set()

def finalsubmit(fname, lname, email, age, pan, gender, aadhar, add1, add2, pswd, cpswd, **kwargs):
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
        create_popup(0, "Please make sure all the fields are filled!")
        return

    if (not namecheck.search(g_fname)) or (not namecheck.search(g_lname)):
        create_popup(0, "Invalid Name! Use of only alphabets is allowed")
        return

    if ("@" not in g_email) or ("." not in g_email):
        create_popup(0, "Invalid mail id! Please re-check")
        return

    try: g_age = int(g_age)
    except:
        create_popup(0, "Age must be numeric only!")
        return

    if (len(g_pan) != 10) or (not pancheck.search(g_pan)):
        create_popup(0, "Invalid PAN number!")
        return

    if len(g_aadhar) != 12:
        create_popup(0, "Invalid Aadhar number!")
        return

    try: g_aadhar = int(g_aadhar)
    except:
        create_popup(0, "Invalid Aadhar number!")
        return

    if not pswdcheck.search(g_pswd):
        create_popup(0, "Password should meet following criteria:\n"
                     "- Minimum 8 characters\n"
                     "- Must contain 1 uppercase letter\n"
                     "- Must contain 1 lowercase letter\n"
                     "- Must contain 1 symbol\n"
                     "- Must contain 1 digit")
        return

    if g_cpswd != g_pswd:
        create_popup(0, "Passwords do not match!")
        return

    userid = random.randint(10 ** 10, 10 ** 11)
    root.accountsdata[str(userid)] = {"pswd": g_pswd, "email": g_email, "address": f"{g_add1}, {g_add2}", "age": g_age, "gender": g_gender,
                                      "pan": g_pan, "aadhar": g_aadhar, "name":f"{g_fname} {g_lname}", "id":str(userid)}
    root.data[str(userid)] = {"balance":0}
    savedata()
    dashboard(root.accountsdata[str(userid)], kwargs["ele"])

def create_popup(pt, text):
    if pt == 0:
        messagebox.showerror("Error", text)
    else:
        messagebox.showinfo("Success", text)

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
    cancel.configure(command=partial(showhomepage, fname, lname, email, age, pan, male, female, other, aadhar, add1, add2, pswd,
                                     cpswd, final, cancel))
    final.configure(command=partial(finalsubmit, fname, lname, email, age, pan, gender, aadhar, add1, add2, pswd, cpswd,
                                    ele=(fname, lname, email, age, pan, male, female, other, aadhar, add1, add2, pswd, cpswd, final, cancel)))

def restore_root():
    if root.fs:
        root.attributes('-fullscreen', False)
        root.fs = False
        restore["text"] = "Maximize"
        restore.place(x=(root.x - x(115)), y=y(2))
        close.place(x=(root.x - x(47)), y=y(2))
        root.cache["fs"] = False
    else:
        root.attributes('-fullscreen', True)
        root.fs = True
        restore["text"] = "Restore"
        restore.place(x=(root.x - x(95)), y=y(2))
        close.place(x=(root.x - x(42)), y=y(2))
        root.cache["fs"] = True
    cacheupdate()

def dashboard(data, *args):
    for i in args[0]:
        i.place_forget()
    root.cache["id"] = data["id"]
    root.cache["skip"] = True
    cacheupdate()
    dashbg = Image.open("data/images/dashboard.png")
    dashbg = dashbg.resize(root.wm_maxsize())
    root.bgimg = ImageTk.PhotoImage(dashbg)
    bg_canvas.itemconfig(root.rootbgimage, image=root.bgimg)

    #=========== ACTUAL DASHBOARD ==============

    topframe = Frame(root, width=root.wm_maxsize()[0], height=80, bg="#B576FF")
    topframe.place(x=0, y=y(25))

    userimg = Image.open("data/images/user.png").resize((x(40), y(40))).convert("RGB")
    userimg = ImageTk.PhotoImage(userimg)
    userimage = Label(root, image=userimg)
    userimage.image = userimg
    userimage.place(x=x(27), y=y(40))

    welcome = Label(topframe, text=f"Welcome, {data['name']}!", font=("Arial", 20), bg="#B576FF")
    welcome.place(x=x(85), y=(20))

    yourdash = Label(root, text=f"Your Dashboard", font=("Arial", x(35), "bold"), bg="white")
    yourdash.place(x=x(595), y=(160))

    depimg = Image.open("data/images/deposit.PNG").resize((x(150), y(150)))
    depimg = ImageTk.PhotoImage(depimg)
    depositbtn = Button(root, text="Deposit", compound=TOP, image=depimg, font=("Arial", 13, "bold"), bg="white",
                        command=partial(deposit, data["id"]))
    depositbtn.place(x=x(400), y=y(300))
    depositbtn.image = depimg

    withimg = Image.open("data/images/withdraw.png").resize((x(150), y(150)))
    withimg = ImageTk.PhotoImage(withimg)
    withbtn = Button(root, text="Withdraw", compound=TOP, image=withimg, font=("Arial", 13, "bold"), bg="white",
                     command=partial(withdraw, data["id"]))
    withbtn.place(x=x(600), y=y(300))
    withbtn.image = withimg

    loanimg = Image.open("data/images/loan.jpg").resize((x(150), y(150)))
    loanimg = ImageTk.PhotoImage(loanimg)
    loanbtn = Button(root, text="Loan", compound=TOP, image=loanimg, font=("Arial", 13, "bold"), bg="white")
    loanbtn.place(x=x(800), y=y(300))
    loanbtn.image = loanimg

    statementsimg = Image.open("data/images/statements.png").resize((x(150), y(150)))
    statementsimg = ImageTk.PhotoImage(statementsimg)
    statementsbtn = Button(root, text="View Statement", compound=TOP, bg="white", image=statementsimg, font=("Arial", 13, "bold"))
    statementsbtn.place(x=x(1000), y=y(300))
    statementsbtn.image = statementsimg

    viewaccimg = Image.open("data/images/viewacc.png").resize((x(150), y(150)))
    viewaccimg = ImageTk.PhotoImage(viewaccimg)
    viewaccbtn = Button(root, text="My Account", compound=TOP, image=viewaccimg, font=("Arial", 13, "bold"), bg="white")
    viewaccbtn.place(x=x(400), y=y(520))
    viewaccbtn.image = viewaccimg

    fdimg = Image.open("data/images/fixeddep.png").resize((x(150), y(150)))
    fdimg = ImageTk.PhotoImage(fdimg)
    fdbtn = Button(root, text="Fixed Deposit", compound=TOP, image=fdimg, font=("Arial", 13, "bold"), bg="white")
    fdbtn.place(x=x(600), y=y(520))
    fdbtn.image = fdimg

    chpswdimg = Image.open("data/images/passwd.png").resize((x(150), y(150)))
    chpswdimg = ImageTk.PhotoImage(chpswdimg)
    chpswdbtn = Button(root, text="Change Pswd.", compound=TOP, image=chpswdimg, font=("Arial", 13, "bold"), bg="white")
    chpswdbtn.place(x=x(800), y=y(520))
    chpswdbtn.image = chpswdimg

    logoutimg = Image.open("data/images/logout.png").resize((x(150), y(150)))
    logoutimg = ImageTk.PhotoImage(logoutimg)
    logoutbtn = Button(root, text="Logout", compound=TOP, image=logoutimg, font=("Arial", 13, "bold"), bg="white")
    logoutbtn.place(x=x(1000), y=y(520))
    logoutbtn.image = logoutimg
    logoutbtn.configure(command=partial(showhomepage, userimage, welcome, yourdash, depositbtn, withbtn, loanbtn,
                                       statementsbtn, viewaccbtn, fdbtn, chpswdbtn, logoutbtn, topframe))

def withdraw(userid):
    picon = ImageTk.PhotoImage(Image.open("data/images/withdraw_icon.png"))
    popup = Toplevel(root)
    popup.iconphoto(False, picon)
    popup.grab_set()
    popup.resizable(0, 0)
    a0 = int(root.wm_maxsize()[0])
    a1 = int(root.wm_maxsize()[1])
    popup.geometry(f"{int(a0/3)}x{int(a1/3)}+{int(a0/3)}+{int(a1/3)}")
    popup.configure(bg="white")
    popup.title("Directrix- Withdraw Money")
    popup.focus_set()

    witht = Label(popup, text="Withdraw Money", font=("Arial", 30, "bold", "underline"), bg="white")
    witht.place(x=x(115), y=y(5))

    curbal = Label(popup, text="Your current balance is:", font=("Arial", 22), bg="white")
    curbal.place(x=x(15), y=y(70))

    var = root.data.get(str(userid))
    balance = var.get('balance')

    bal = Label(popup, text=f"{balance} INR", font=("Calibri", 22, "bold"), bg="white")
    bal.place(x=x(325), y=y(69))

    lab = Label(popup, text="Enter Amount:", font=("Arial", 22), bg="white")
    lab.place(x=x(15), y=y(125))
    ent = Entry(popup, font=("Arial", 22), bg="white", width=x(15))
    ent.place(x=x(210), y=y(127))

    lab2 = Label(popup, text="Reason (Opt):", font=("Arial", 22), bg="white")
    lab2.place(x=x(15), y=y(165))
    txt = Text(popup, font=("Calibri", 20), bg="white", width=x(17), height=y(2))
    txt.place(x=x(210), y=y(167))

    btn = Button(popup, text="Withdraw", font=("Arial", 15), bg="#FFCF61",
                 command=partial(withdraw_process, userid, ent, txt, balance, popup))
    btn.place(x=x(140), y=y(240))
    btn2 = Button(popup, text=" Cancel ", font=("Arial", 15), bg="#FF5959", command=popup.destroy)
    btn2.place(x=x(250), y=y(240))

def withdraw_process(userid, ent, txt, balance, popup):
    withd = ent.get().replace(" ", "")
    reason = txt.get("0.0", END)
    if withd == "":
        create_popup(0, "Amount cannot be empty")
        return
    try: withd = int(withd)
    except:
        create_popup(0, "The amount should be numbers only!")
        return
    if withd > balance:
        create_popup(0, 'Insufficient Balance')
    elif withd == 0:
        create_popup(0, 'Cannot withdraw 0 money')
    else:
        nam = balance - withd
        root.data[str(userid)] = {"balance":nam}
        savedata()
        popup.destroy()
        create_popup(1, "Withdraw Successful!")

def deposit(userid):
    picon = ImageTk.PhotoImage(Image.open("data/images/deposit_icon.png"))
    popup = Toplevel(root)
    popup.iconphoto(False, picon)
    popup.grab_set()
    popup.resizable(0, 0)
    a0 = int(root.wm_maxsize()[0])
    a1 = int(root.wm_maxsize()[1])
    popup.geometry(f"{int(a0 / 3)}x{int(a1 / 3)}+{int(a0 / 3)}+{int(a1 / 3)}")
    popup.configure(bg="white")
    popup.title("Directrix- Deposit Money")
    popup.focus_set()

    witht = Label(popup, text="Deposit Money", font=("Arial", 30, "bold", "underline"), bg="white")
    witht.place(x=x(115), y=y(5))

    curbal = Label(popup, text="Your current balance is:", font=("Arial", 22), bg="white")
    curbal.place(x=x(15), y=y(70))

    var = root.data.get(str(userid))
    balance = var.get('balance')

    bal = Label(popup, text=f"{balance} INR", font=("Calibri", 22, "bold"), bg="white")
    bal.place(x=x(325), y=y(69))

    lab = Label(popup, text="Enter Amount:", font=("Arial", 22), bg="white")
    lab.place(x=x(15), y=y(125))
    ent = Entry(popup, font=("Arial", 22), bg="white", width=x(15))
    ent.place(x=x(210), y=y(127))

    lab2 = Label(popup, text="Reason (Opt):", font=("Arial", 22), bg="white")
    lab2.place(x=x(15), y=y(165))
    txt = Text(popup, font=("Calibri", 20), bg="white", width=x(17), height=y(2))
    txt.place(x=x(210), y=y(167))

    btn = Button(popup, text="Deposit", font=("Arial", 15), bg="#FFCF61",
                 command=partial(deposit_process, userid, ent, txt, balance, popup))
    btn.place(x=x(150), y=y(240))
    btn2 = Button(popup, text=" Cancel ", font=("Arial", 15), bg="#FF5959", command=popup.destroy)
    btn2.place(x=x(240), y=y(240))

def deposit_process(userid, ent, txt, balance, popup):
    dep = ent.get().replace(" ", "")
    reason = txt.get("0.0", END)
    if dep == "":
        create_popup(0, "Amount cannot be empty")
        return
    try: dep = int(dep)
    except:
        create_popup(0, "The amount should be numbers only!")
        return
    alloted = balance*0.25
    if dep < alloted:
        n_balance = dep + balance
        create_popup(1, f"The amount is successfully deposited")
        root.data[str(userid)] = {"balance": n_balance}
        savedata()

    elif dep > alloted :
        create_popup(0, "The amount you want to deposit is larger than allowed.\nPlease refer to out TnC for further information")

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

def cacheupdate():
    with open("data/cache.json", "w") as f:
        f.write(json.dumps(root.cache, indent=2))

def createstatements(userid, amount, t):
    prev = root.statements.get(str(userid), [])
    prev.append({"type": t, "amt": amount})
    savedata()
    
root = Tk()
root.resizable(0, 0)
root.title("Directrix Bank")
root.geometry(f"{root.wm_maxsize()[0]}x{root.wm_maxsize()[1]}")
root.x = root.wm_maxsize()[0]
root.y = root.wm_maxsize()[1]
root.attributes('-fullscreen', True)
root.fs = True
bg = Image.open("data/images/bg.png")
bg = bg.resize(root.wm_maxsize())
root.bgimg = ImageTk.PhotoImage(bg)

with open("data/accounts.json", "r") as f:
    root.accountsdata = json.load(f)

with open("data/data.json", "r") as f:
    root.data = json.load(f)

with open("data/statements.json", "r") as f:
    root.statements = json.load(f)

with open("data/cache.json", "r") as f:
    root.cache = json.load(f)

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

password_field = Entry(root, width=x(25), font=("Helvetica", 22), show="*")
password_field.place(x=x(95), y=y(490))
cacheid = root.cache.get("id")
if cacheid is not None:
    login_field.insert(0, cacheid)
    password_field.focus_set()
else: login_field.focus_set()

submit_login = Button(root, text="Login", font=("Arial", 18), width=x(14), bg="#62E1FF", command=create_login)
submit_login.place(x=x(85), y=y(600))

submit_create = Button(root, text="Create Account", font=("Arial", 18), width=x(14), bg="#62E1FF", command=submit_data)
submit_create.place(x=x(300), y=y(600))

status = Label(root, font=("Helvetica", 16), bg="#ffffff", fg="#FF0000")

fs = root.cache.setdefault("fs", True)
if not fs: restore_root()
cacheupdate()

if root.cache.get("skip", False):
    dashboard(root.accountsdata[str(cacheid)], (login_field, password_field, submit_login, submit_create, status))

root.mainloop()

