# Directric Bank
# Refer README.md for features and contributions

import random, datetime
import time, json, re
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
from prettytable import PrettyTable

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

    with open('data/fd.json', 'w') as fd:
        fd.write(json.dumps(root.fd, indent=2))

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

    if " " in g_pswd:
        create_popup(0, "Password cannot contain a space!")
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

    fname = Entry(root, width=x(20), font=("Helvetica", x(22)))
    fname.place(x=x(400), y=y(164))
    lname = Entry(root, width=x(20), font=("Helvetica", x(22)))
    lname.place(x=x(1060), y=y(164))
    email = Entry(root, width=x(25), font=("Helvetica", x(22)))
    email.place(x=x(400), y=y(238))
    age = Entry(root, width=x(5), font=("Helvetica", x(22)))
    age.place(x=x(1060), y=y(238))
    pan = Entry(root, width=x(25), font=("Helvetica", x(22)))
    pan.place(x=x(400), y=y(312))
    gender = StringVar()
    male = Radiobutton(root, text="Male", variable=gender, value="M", font=("Helvetica", x(20)), bg="#ffffff")
    male.place(x=x(1060), y=y(305))
    female = Radiobutton(root, text="Female", variable=gender, value="F", font=("Helvetica", x(20)), bg="#ffffff")
    female.place(x=x(1160), y=y(305))
    other = Radiobutton(root, text="Other", variable=gender, value="O", font=("Helvetica", x(20)), bg="#ffffff")
    other.place(x=x(1290), y=y(305))
    aadhar = Entry(root, width=x(25), font=("Helvetica", x(22)))
    aadhar.place(x=x(400), y=y(386))
    add1 = Entry(root, width=x(30), font=("Helvetica", x(22)))
    add1.place(x=x(400), y=y(460))
    add2 = Entry(root, width=x(30), font=("Helvetica", x(22)))
    add2.place(x=x(400), y=y(534))
    pswd = Entry(root, width=x(25), font=("Helvetica", x(22)), show="*")
    pswd.place(x=x(540), y=y(662))
    cpswd = Entry(root, width=x(25), font=("Helvetica", x(22)), show="*")
    cpswd.place(x=x(540), y=y(736))

    final = Button(root, text="Open Account", font=("Arial", x(22)), width=x(14), bg="#37FF4E")
    final.place(x=x(1030), y=y(690))
    cancel = Button(root, text="Cancel", font=("Arial", x(22)), width=x(11), bg="#FF4E3F")
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

    welcome = Label(topframe, text=f"Welcome, {data['name']}!", font=("Arial", x(20)), bg="#B576FF")
    welcome.place(x=x(85), y=(20))

    yourdash = Label(root, text=f"Your Dashboard", font=("Arial", x(35), "bold"), bg="white")
    yourdash.place(x=x(595), y=(160))

    depimg = Image.open("data/images/deposit.PNG").resize((x(150), y(150)))
    depimg = ImageTk.PhotoImage(depimg)
    depositbtn = Button(root, text="Deposit", compound=TOP, image=depimg, font=("Arial", x(13), "bold"), bg="white",
                        command=partial(deposit, data["id"]))
    depositbtn.place(x=x(400), y=y(300))
    depositbtn.image = depimg

    withimg = Image.open("data/images/withdraw.png").resize((x(150), y(150)))
    withimg = ImageTk.PhotoImage(withimg)
    withbtn = Button(root, text="Withdraw", compound=TOP, image=withimg, font=("Arial", x(13), "bold"), bg="white",
                     command=partial(withdraw, data["id"]))
    withbtn.place(x=x(600), y=y(300))
    withbtn.image = withimg

    loanimg = Image.open("data/images/loan.jpg").resize((x(150), y(150)))
    loanimg = ImageTk.PhotoImage(loanimg)
    loanbtn = Button(root, text="Loan", compound=TOP, image=loanimg, font=("Arial", x(13), "bold"), bg="white",
                     command=partial(loan, data["id"]))
    loanbtn.place(x=x(800), y=y(300))
    loanbtn.image = loanimg

    statementsimg = Image.open("data/images/statements.png").resize((x(150), y(150)))
    statementsimg = ImageTk.PhotoImage(statementsimg)
    statementsbtn = Button(root, text="View Statement", compound=TOP, bg="white", image=statementsimg, font=("Arial", x(13), "bold"),
                           command=partial(showstatement, data["id"]))
    statementsbtn.place(x=x(1000), y=y(300))
    statementsbtn.image = statementsimg

    viewaccimg = Image.open("data/images/viewacc.png").resize((x(150), y(150)))
    viewaccimg = ImageTk.PhotoImage(viewaccimg)
    viewaccbtn = Button(root, text="My Account", compound=TOP, image=viewaccimg, font=("Arial", x(13), "bold"), bg="white",
                        command=partial(my_acc, data["id"]))
    viewaccbtn.place(x=x(400), y=y(520))
    viewaccbtn.image = viewaccimg

    fdimg = Image.open("data/images/fixeddep.png").resize((x(150), y(150)))
    fdimg = ImageTk.PhotoImage(fdimg)
    fdbtn = Button(root, text="Fixed Deposit", compound=TOP, image=fdimg, font=("Arial", x(13), "bold"), bg="white",
                   command=partial(fdp, data["id"]))
    fdbtn.place(x=x(600), y=y(520))
    fdbtn.image = fdimg

    chpswdimg = Image.open("data/images/passwd.png").resize((x(150), y(150)))
    chpswdimg = ImageTk.PhotoImage(chpswdimg)
    chpswdbtn = Button(root, text="Change Pswd.", compound=TOP, image=chpswdimg, font=("Arial", x(13), "bold"), bg="white",
                       command=partial(changepass, data["id"]))
    chpswdbtn.place(x=x(800), y=y(520))
    chpswdbtn.image = chpswdimg

    logoutimg = Image.open("data/images/logout.png").resize((x(150), y(150)))
    logoutimg = ImageTk.PhotoImage(logoutimg)
    logoutbtn = Button(root, text="Logout", compound=TOP, image=logoutimg, font=("Arial", x(13), "bold"), bg="white")
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

    witht = Label(popup, text="Withdraw Money", font=("Arial", x(30), "bold", "underline"), bg="white")
    witht.place(x=x(115), y=y(5))

    curbal = Label(popup, text="Your current balance is:", font=("Arial", x(22)), bg="white")
    curbal.place(x=x(15), y=y(70))

    var = root.data.get(str(userid))
    balance = var.get('balance')

    bal = Label(popup, text=f"{balance} INR", font=("Calibri", x(22), "bold"), bg="white")
    bal.place(x=x(325), y=y(69))

    lab = Label(popup, text="Enter Amount:", font=("Arial", x(22)), bg="white")
    lab.place(x=x(15), y=y(125))
    ent = Entry(popup, font=("Arial", x(22)), bg="white", width=x(15))
    ent.place(x=x(210), y=y(127))

    lab2 = Label(popup, text="Reason (Opt):", font=("Arial", x(22)), bg="white")
    lab2.place(x=x(15), y=y(165))
    txt = Text(popup, font=("Calibri", x(20)), bg="white", width=x(17), height=y(2))
    txt.place(x=x(210), y=y(167))

    btn = Button(popup, text="Withdraw", font=("Arial", x(15)), bg="#FFCF61",
                 command=partial(withdraw_process, userid, ent, txt, balance, popup))
    btn.place(x=x(140), y=y(240))
    btn2 = Button(popup, text=" Cancel ", font=("Arial", x(15)), bg="#FF5959", command=popup.destroy)
    btn2.place(x=x(250), y=y(240))

def withdraw_process(userid, ent, txt, balance, popup):
    withd = ent.get().replace(" ", "")
    reason = txt.get("0.0", END)
    if len(reason) > 15:
        create_popup(0, "Explain the reason in less than 15 characters")
        return
    if withd == "":
        create_popup(0, "Amount cannot be empty")
        return
    try: withd = int(withd)
    except:
        create_popup(0, "The amount should be numbers only!")
        return
    if withd > balance:
        create_popup(0, 'Insufficient Balance')
        return
    elif withd == 0:
        create_popup(0, 'Cannot withdraw 0 money')
        return
    elif withd < 0:
        create_popup(0, "The amount cannot be negative")
        return
    else:
        nam = balance - withd
        root.data[str(userid)] = {"balance":nam}
        createstatements(userid, withd, "D", reason)
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

    witht = Label(popup, text="Deposit Money", font=("Arial", x(30), "bold", "underline"), bg="white")
    witht.place(x=x(115), y=y(5))

    curbal = Label(popup, text="Your current balance is:", font=("Arial", x(22)), bg="white")
    curbal.place(x=x(15), y=y(70))

    var = root.data.get(str(userid))
    balance = var.get('balance')

    bal = Label(popup, text=f"{balance} INR", font=("Calibri", x(22), "bold"), bg="white")
    bal.place(x=x(325), y=y(69))

    lab = Label(popup, text="Enter Amount:", font=("Arial", x(22)), bg="white")
    lab.place(x=x(15), y=y(125))
    ent = Entry(popup, font=("Arial", x(22)), bg="white", width=x(15))
    ent.place(x=x(210), y=y(127))

    lab2 = Label(popup, text="Reason (Opt):", font=("Arial", x(22)), bg="white")
    lab2.place(x=x(15), y=y(165))
    txt = Text(popup, font=("Calibri", 20), bg="white", width=x(17), height=y(2))
    txt.place(x=x(210), y=y(167))

    btn = Button(popup, text="Deposit", font=("Arial", x(15)), bg="#FFCF61",
                 command=partial(deposit_process, userid, ent, txt, balance, popup))
    btn.place(x=x(150), y=y(240))
    btn2 = Button(popup, text=" Cancel ", font=("Arial", x(15)), bg="#FF5959", command=popup.destroy)
    btn2.place(x=x(240), y=y(240))

def deposit_process(userid, ent, txt, balance, popup):
    dep = ent.get().replace(" ", "")
    reason = txt.get("0.0", END)
    if len(reason) > 15:
        create_popup(0, "Explain the reason in less than 15 characters")
        return
    if dep == "":
        create_popup(0, "Amount cannot be empty")
        return
    try: dep = int(dep)
    except:
        create_popup(0, "The amount should be numbers only!")
        return
    if dep == 0:
        create_popup(0, 'Cannot deposit 0 money')
        return
    elif dep < 0:
        create_popup(0, "The amount cannot be negative")
        return
    alloted = 100000
    if dep > alloted:
        create_popup(0, "The amount you want to deposit is larger than allowed.\nPlease refer to out TnC for further information")
        return

    n_balance = dep + balance
    root.data[str(userid)] = {"balance": n_balance}
    createstatements(userid, dep, "C", reason)
    popup.destroy()
    create_popup(1, f"The amount is successfully deposited")

fd_plans = [
    {"amt": 25000, "time": 12, "rate": 5.75, "payout": 1561, "mat": 26561},  # (0)
    {"amt": 25000, "time": 24, "rate": 6.20, "payout": 3196, "mat": 28196},  # (1)
    {"amt": 25000, "time": 36, "rate": 6.60, "payout": 5284, "mat": 30284},  # (2)
    {"amt": 50000, "time": 12, "rate": 5.75, "payout": 2875, "mat": 52875},  # (3)
    {"amt": 50000, "time": 24, "rate": 6.20, "payout": 6392, "mat": 56392},  # (4)
    {"amt": 50000, "time": 36, "rate": 6.60, "payout": 10568, "mat": 60568},  # (5)
    {"amt": 100000, "time": 12, "rate": 5.75, "payout": 5750, "mat": 105750},  # (6)
    {"amt": 100000, "time": 24, "rate": 6.20, "payout": 12784, "mat": 112784},  # (7)
    {"amt": 100000, "time": 36, "rate": 6.60, "payout": 21136, "mat": 121136},  # (8)
]

def fdp(userid):

    def fdstart():
        index = fdindex.get()
        if 0 <= index <= len(fd_plans):
            data = fd_plans[index]
            data.update({'start': time.time()})
            root.fd[str(userid)] = data
            savedata()
            popup.destroy()
            create_popup(1, "Success!")
            fdp(userid)
        else:
            create_popup(0, "Please select an option!")

    picon = ImageTk.PhotoImage(Image.open("data/images/fixeddep_icon.png"))
    popup = Toplevel(root)
    popup.iconphoto(False, picon)
    popup.grab_set()
    popup.resizable(0, 0)
    a0 = int(root.wm_maxsize()[0])
    a1 = int(root.wm_maxsize()[1])
    fw = a0 / 2.1
    fh = a1 / 2.1
    popup.geometry(f"{int(fw)}x{int(fh)}+{int(a0/2 - fw/2)}+{int(a1/2 - fh/2)}")
    popup.configure(bg="white")
    popup.title("Directrix- Fixed Deposit")
    popup.focus_set()

    if str(userid) in root.fd.keys():
        var = root.fd.get(str(userid))
        time_ = var.get('start')  # aaj se start hua hai
        dt_object = datetime.datetime.fromtimestamp(time_).date()
        dt_object = str(dt_object).split("-")
        dt_object.reverse()
        dt_object = ".".join(dt_object)
        dt_object2 = datetime.datetime.fromtimestamp((var['time'] * 30 * 24 * 60 * 60) + time_).date()
        dt_object2 = str(dt_object2).split("-")
        dt_object2.reverse()
        dt_object2 = ".".join(dt_object2)

        fdamt = Label(popup, text=f"Fixed Deposit Details", font=("Arial", x(27), "bold", "underline"), bg="white")
        fdamt.place(x=x(200), y=y(5))

        fdamt = Label(popup, text=f"Investement Amount: ₹{var['amt']}/-", font=("Arial", x(22)), bg="white")
        fdamt.place(x=x(15), y=y(75))
        fdten = Label(popup, text=f"Investement Tenure: {var['time']} months", font=("Arial", x(22)), bg="white")
        fdten.place(x=x(15), y=y(115))
        fdrate = Label(popup, text=f"Interest Rate: {var['rate']}%", font=("Arial", x(22)), bg="white")
        fdrate.place(x=x(15), y=y(155))
        fdpay = Label(popup, text=f"Interest Payout: ₹{var['payout']}/-", font=("Arial", x(22)), bg="white")
        fdpay.place(x=x(15), y=y(195))
        fdmat = Label(popup, text=f"Maturity Amount: ₹{var['mat']}", font=("Arial", x(22)), bg="white")
        fdmat.place(x=x(15), y=y(235))
        fdstart = Label(popup, text=f"Start Date: {dt_object}", font=("Arial", x(22)), bg="white")
        fdstart.place(x=x(15), y=y(292))
        fdend = Label(popup, text=f"End Date: {dt_object2}", font=("Arial", x(22)), bg="white")
        fdend.place(x=x(380), y=y(292))
        close = Button(popup, text="Close", font=("Arial", x(15)), bg="#FFCF61",
                               command=popup.destroy)
        close.place(x=x(320), y=y(350))
        return

    a0 = int(root.wm_maxsize()[0])
    a1 = int(root.wm_maxsize()[1])
    fw = a0 / 1.7
    fh = a1 / 1.8
    popup.geometry(f"{int(fw)}x{int(fh)}+{int(a0 / 2 - fw / 2)}+{int(a1 / 2 - fh / 2)}")
    fdindex = IntVar(value=10)
    pdata = PrettyTable()
    pdata.field_names = ["S.No.", "Investm.", "Tenure", "Rate", "Payout", "Maturity"]
    txt = Text(popup, font=("Courier New", x(18)), bg="white", width=x(67), height=y(15))
    txt.place(x=x(52), y=y(70))
    fdwel = Label(popup, text=f"Choose F.D. Plan", font=("Arial", x(27), "bold", "underline"), bg="white")
    fdwel.place(x=x(300), y=y(5))

    yval = 150
    sno = 1
    for i in fd_plans:
        plan = Radiobutton(popup, text=f"", font=("Arial", x(15)), variable=fdindex, value=fd_plans.index(i),
                                 bg="#fff")
        plan.place(x=x(25), y=y(yval))
        pdata.add_row([sno, i["amt"], i["time"], f"{i['rate']}%", i["payout"], i["mat"]])
        sno += 1
        yval += y(27)

    acc = Button(popup, text="Start F.D.", font=("Arial", x(15)), bg="#81a9fd",
                   command=fdstart)
    acc.place(x=x(320), y=y(425))
    close = Button(popup, text="Cancel", font=("Arial", x(15)), bg="#FFCF61",
                   command=popup.destroy)
    close.place(x=x(430), y=y(425))
    txt.insert("0.0", pdata)
    txt.configure(state=DISABLED)

def loan(userid):
    userid = str(userid)
    if root.data[userid].get("loan") is None:
        create_popup(0, "You already have a loan active")
        return
    picon = ImageTk.PhotoImage(Image.open("data/images/loan_icon.png"))
    popup = Toplevel(root)
    popup.iconphoto(False, picon)
    popup.grab_set()
    popup.resizable(0, 0)
    a0 = int(root.wm_maxsize()[0])
    a1 = int(root.wm_maxsize()[1])
    fw = a0 / 2.0
    fh = a1 / 2.0
    popup.geometry(f"{int(fw)}x{int(fh)}+{int(a0 / 2 - fw / 2)}+{int(a1 / 2 - fh / 2)}")
    popup.configure(bg="white")
    popup.title("Directrix- Loan")
    popup.focus_set()
    userid = 56790311881
    userid = str(userid)
    loan_details = Label(popup, text=f"Loan Details", font=("Arial", x(27), "bold", "underline"), bg="white")
    loan_details.place(x=x(290), y=y(0))
    expected_ = Label(popup, text=f"Amount: ", font=("Arial", x(22)), bg="white")
    expected_.place(x=x(15), y=y(151))
    income_ = Label(popup, text=f"Income: ", font=("Arial", x(22)), bg="white")
    income_.place(x=x(15), y=y(100))
    reason_ = Label(popup, text=f"Reason: ", font=("Arial", x(22)), bg="white")
    reason_.place(x=x(15), y=y(241))
    job_ = Label(popup, text=f"Job: ", font=("Arial", x(22)), bg="white")
    job_.place(x=x(15), y=y(286))
    time_ = Label(popup, text=f"Time (in M):", font=("Arial", x(22)), bg="white")
    time_.place(x=x(15), y=y(331))

    expected = Entry(popup, width=x(20), font=("Helvetica", x(22)))
    expected.place(x=x(190), y=y(151))
    income = Entry(popup, width=x(20), font=("Helvetica", x(22)))
    income.place(x=x(190), y=y(100))
    reason = Entry(popup, width=x(20), font=("Helvetica", x(22)))
    reason.place(x=x(190), y=y(241))
    job = Entry(popup, width=x(20), font=("Helvetica", x(22)))
    job.place(x=x(190), y=y(286))
    time__ = Entry(popup, width=x(20), font=("Helvetica", x(22)))
    time__.place(x=x(190), y=y(331))

    sub = Button(popup, text="Submit", font=("Arial", x(15)), bg="#FFCF61",
                   command=partial(loan_process, income, expected, job, reason, time__, userid, popup))
    sub.place(x=x(275), y=y(380))
    close = Button(popup, text="Cancel", font=("Arial", x(15)), bg="#FFCF61",
                   command=popup.destroy)
    close.place(x=x(400), y=y(380))

def loan_process(income, expected, job, reason, time__, userid, popup):
    inc = income.get()
    if inc.replace(' ', '') == "":
        create_popup(0, "Amount cannot be empty")
    try:
        inc = int(float(inc))
    except:
        create_popup(0, "Amount is not integer")
        return
    if inc == 0:
        create_popup(0, "Amount cannot be 0")
        return
    if inc < 0:
        create_popup(0, "Amount cannot be negative")
        return

    exp = expected.get()
    if exp.replace(' ', '') == "":
        create_popup(0, "Amount cannot be empty")
        return
    try:
        exp = int(exp)
    except:
        create_popup(0, "Amount is not integer")
        return
    if exp == 0:
        create_popup(0, "Amount cannot be 0")
        return
    if exp < 0:
        create_popup(0, "Amount cannot be negative")
        return
    if exp >= (inc) * 7:
        create_popup(0, "Amount is too large")
        return

    reason = reason.get()
    if reason.replace(' ', '') == "":
        create_popup(0, "Reason cannot be empty")
        return
    if len(reason) > 25:
        create_popup(0, "Please give a genuine reason in less than 25 words")
        return

    job = job.get()
    if job.replace(' ', '') == "":
        create_popup(0, "Job cannot be empty")
        return
    if len(job) > 20:
        create_popup(0, "Please give a brief description about your occupation in less than 20 words")
        return

    till_when = time__.get()
    if till_when == "":
        create_popup(0, "Time period cannot be empty")
        return
    try:
        till_when = round(int(float(till_when)))  # roundoff
    except:
        create_popup(0, "Detail must be integer")
        return

    rate = .03
    confirm_c = (inc / 12) * rate
    c_inc = (inc / 12) * 0.20
    interest = exp * rate * till_when
    amount = exp + interest
    if c_inc > confirm_c:
        create_popup(1, "Loan has been confirmed")
    else:
        create_popup(0, "Invalid Details")
        return
    data = {"time": till_when, "exp": exp, "inc": inc, "reason": reason, "job": job, "interest": interest,
            "amt": amount, "rate": rate}
    root.data[str(userid)]["loan"] = data
    popup.destroy()
    savedata()

def cacheupdate():
    with open("data/cache.json", "w") as f:
        f.write(json.dumps(root.cache, indent=2))

def changepass(userid):
    picon = ImageTk.PhotoImage(Image.open("data/images/passwd_icon.png"))
    popup = Toplevel(root)
    popup.iconphoto(False, picon)
    popup.grab_set()
    popup.resizable(0, 0)
    a0 = int(root.wm_maxsize()[0])
    a1 = int(root.wm_maxsize()[1])
    popup.geometry(f"{int(a0 / 3)}x{int(a1 / 3)}+{int(a0 / 3)}+{int(a1 / 3)}")
    popup.configure(bg="white")
    popup.title("Directrix- Change Password")
    popup.focus_set()


    chp = Label(popup, text="Change Password", font=("Arial", x(30), "bold", "underline"), bg="white")
    chp.place(x=x(80), y=y(5))

    chp = Label(popup, text="Current Pass:", font=("Arial", x(20)), bg="white")
    chp.place(x=x(10), y=y(70))
    cur = Entry(popup, font=("Arial", x(18)), bg="white", show="*")
    cur.place(x=x(190), y=y(74))

    newp = Label(popup, text=f"New Pass:", font=("Arial", x(20)), bg="white")
    newp.place(x=x(10), y=y(140))
    new = Entry(popup, font=("Arial", x(18)), bg="white", show="*")
    new.place(x=x(190), y=y(140))

    conp = Label(popup, text="Confirm Pass:", font=("Arial", x(20)), bg="white")
    conp.place(x=x(10), y=y(180))
    con = Entry(popup, font=("Arial", x(18)), bg="white", show="*")
    con.place(x=x(190), y=y(180))

    btn = Button(popup, text="Change", font=("Arial", x(15)), bg="#FFCF61",
                 command=partial(passprocess, userid, cur, new, con, popup))
    btn.place(x=x(150), y=y(240))
    btn2 = Button(popup, text=" Cancel ", font=("Arial", x(15)), bg="#FF5959", command=popup.destroy)
    btn2.place(x=x(240), y=y(240))

def passprocess(userid, oldpass, newpass, confirmpass, popup):
    userid = str(userid)
    oldpass = oldpass.get().replace(" ", "")
    newpass = newpass.get()
    confirmpass = confirmpass.get()

    if root.accountsdata[userid]["pswd"] != oldpass:
        create_popup(0, "Current password is incorrect!")
        return

    if newpass == "":
        create_popup(0, "New password cannot be empty!")
        return

    if " " in newpass:
        create_popup(0, "Password cannot contain a space!")
        return

    if newpass != confirmpass:
        create_popup(0, "New password and Confirm password do not match!")
        return

    if not pswdcheck.search(newpass):
        create_popup(0, "Password should meet following criteria:\n"
                     "- Minimum 8 characters\n"
                     "- Must contain 1 uppercase letter\n"
                     "- Must contain 1 lowercase letter\n"
                     "- Must contain 1 symbol\n"
                     "- Must contain 1 digit")
        return
    root.accountsdata[userid]["pswd"] = confirmpass
    savedata()
    create_popup(1, "Password changed successfully!")
    popup.destroy()

def createstatements(userid, amount, t, reason):
    if reason == "\n": reason = "N.A."
    prev = root.statements.get(str(userid), [])
    prev.append({"type": t, "amt": amount, "r":reason.replace("\n", ""), "time":time.time()})
    root.statements[str(userid)] = prev
    savedata()

def my_acc(userid):
    picon = ImageTk.PhotoImage(Image.open("data/images/viewacc_icon.png"))
    popup = Toplevel(root)
    popup.iconphoto(False, picon)
    popup.grab_set()
    popup.resizable(0, 0)
    a0 = int(root.wm_maxsize()[0])
    a1 = int(root.wm_maxsize()[1])
    fw = a0 / 2
    fh = a1 / 1.56
    popup.geometry(f"{int(fw)}x{int(fh)}+{int(a0 / 2 - fw / 2)}+{int(a1 / 2 - fh / 2)}")
    popup.configure(bg="white")
    popup.title("Directrix- My Account")
    popup.focus_set()
    loan_, fd = True, True
    var = root.accountsdata.get(str(userid))
    userid = str(userid)
    name = var["name"]
    email = var["email"]
    email2 = email.split("@")[0]
    email_final = email[:3] + "*" * (len(email2) - 3)+ "@gmail.com"
    address = var["address"]
    age = var["age"]
    gender = var["gender"]
    va = root.data.get(str(userid))
    balance = va["balance"]
    if str(userid) in root.fd.keys():
        fd = True
    else:
        fd = False
    if root.data[userid].get("loan") is not None:
        loan_ = True
    else:
        loan_ = False
    v = root.statements.get(str(userid), [])
    root.statements[str(userid)] = v
    if len(v) != 0:
        a = v[-1]
        type = a["type"]
        amount = a["amt"]
        reason = a["r"]
        time = a["time"]
    else:
        type, amount, reason, time = "", "", "", ""

    acount_details = Label(popup, text=f"Account Details", font=("Arial", x(27), "bold", "underline"), bg="white")
    acount_details.place(x=x(260), y=y(0))
    name_ = Label(popup, text=f"Full Name: {name}", font=("Arial", x(22)), bg="white")
    name_.place(x=x(15), y=y(50))
    email_ = Label(popup, text=f"E-mail ID: {email_final} ", font=("Arial", x(22)), bg="white")
    email_.place(x=x(15), y=y(90))
    address_ = Label(popup, text=f"Address: {address} ", font=("Arial", x(22)), bg="white")
    address_.place(x=x(15), y=y(130))
    age_ = Label(popup, text=f"Age: {age}", font=("Arial", x(22)), bg="white")
    age_.place(x=x(15), y=y(170))
    gender_ = Label(popup, text=f"Gender: {gender} ", font=("Arial", x(22)), bg="white")
    gender_.place(x=x(15), y=y(210))
    accid = Label(popup, text=f"Account ID:{userid} ", font=("Arial", x(22)), bg="white")
    accid.place(x=x(15), y=y(250))
    bala = Label(popup, text=f"Balance:₹{balance} ", font=("Arial", x(22)), bg="white")
    bala.place(x=x(15), y=y(290))
    if loan_:
        loanT = Label(popup, text=f"Loan Taken: Yes", font=("Arial", x(22)), bg="white")
        loanT.place(x=x(15), y=y(330))
    else:
        loanf = Label(popup, text=f"Loan Taken: NO", font=("Arial", x(22)), bg="white")
        loanf.place(x=x(15), y=y(330))
    if fd:
        fdt = Label(popup, text=f"FD opted: Yes", font=("Arial", x(22)), bg="white")
        fdt.place(x=x(450), y=y(330))
    else:
        fdg = Label(popup, text=f"FD opted: No", font=("Arial", x(22)), bg="white")
        fdg.place(x=x(450), y=y(330))

    myTable = PrettyTable(["Type", "Amount", "Reason", "Date"])
    dt_object = datetime.datetime.fromtimestamp(time).date()
    dt_object = str(dt_object).split("-")
    dt_object.reverse()
    dt_object = ".".join(dt_object)
    type = "Credit" in type == "C" or "Debit"
    # Add rows
    myTable.add_row([type, amount, reason, dt_object])
    widget = Text(popup, font=("Courier New", x(17)), bg="white", width=x(60), height=y(6))
    widget.place(x=x(15), y=y(380))
    widget.configure(state=NORMAL)
    widget.delete("0.0", END)
    widget.insert("0.0", myTable)
    widget.configure(state=DISABLED)


    close = Button(popup, text="Close", font=("Arial", x(15)), bg="#FFCF61",
                   command=popup.destroy)
    close.place(x=x(335), y=y(510))

class BankStatement:
    def __init__(self, userid:int, txt:Text):
        self.sort = False
        self.pt = PrettyTable()
        self.pt.title = "Bank Statement(s)"
        self.pt.field_names = ["S.No.", "Type", "Amount", "Date", "Reason"]
        self.userid = str(userid)
        self.widget = txt
        self.allst = root.statements.get(self.userid, [])
        self.filters = {"amt":{"g":0, "l":0}, "old":0, "reason":{"type":0, "val":""}}
        self.sortval, self.reasonval, self.older = IntVar(), IntVar(), IntVar()
        self.gamtval, self.lamtval, self.reasonis, self.reasonhas = Entry(), Entry(), Entry(), Entry()

    def show(self):
        self.update()
        count = 1
        self.pt.clear_rows()
        sortval_ = self.sortval.get()
        amtfil = self.filters["amt"]
        rfil = self.filters["reason"]
        tfil = self.filters["old"]
        prerows = []
        for i in self.allst:
            if sortval_ != 0:
                if (sortval_ == 1 and i["type"] != "C") or (sortval_ == 2 and i["type"] != "D"): continue
            type_ = "Credit" if i["type"] == "C" else "Debit"

            amt = i["amt"]
            if amtfil["l"] == 0:
                if not amt > amtfil["g"]: continue
            else:
                if not amtfil["l"] > amt > amtfil["g"]: continue

            reas = i["r"]
            if rfil["type"] == 2:
                if reas.lower() != str(rfil["val"]).lower(): continue
            elif rfil["type"] == 1:
                if str(rfil["val"]).lower() not in reas.lower(): continue

            time_ = i.get("time", time.time())
            if time_ > (time.time() - tfil): continue

            dt_object = datetime.datetime.fromtimestamp(time_).date()
            dt_object = str(dt_object).split("-")
            dt_object.reverse()
            dt_object = ".".join(dt_object)
            prerows.append([count, type_, amt, dt_object, reas])
            count += 1

        prerows.reverse()
        for i in prerows: self.pt.add_row(i)
        self.insert(self.pt)

    def update(self):
        loamt = self.lamtval.get()
        if loamt == "":
            loamt = 0
        else:
            try: loamt = int(loamt)
            except: create_popup(0, "Amount should be integer"); loamt = 0

        gramt = self.gamtval.get()
        if gramt == "": gramt = 0
        else:
            try: gramt = int(gramt)
            except: create_popup(0, "Amount should be integer"); gramt = 0

        self.filters["amt"] = {"l":loamt, "g":gramt}

        reasonval = self.reasonval.get()

        if reasonval != 0:
            if reasonval == 1:
                val = self.reasonhas.get()
            else:
                val = self.reasonis.get()
            self.filters["reason"] = {"type":reasonval, "val":val}
        else:
            self.filters["reason"]["type"] = 0

        base = 2592000
        months = self.older.get()
        self.filters["old"] = base*months

    def insert(self, content):
        self.widget.configure(state=NORMAL)
        self.widget.delete("0.0", END)
        self.widget.insert("0.0", content)
        self.widget.configure(state=DISABLED)

    def resetfilters(self):
        self.gamtval.delete(0, END)
        self.lamtval.delete(0, END)
        self.reasonis.delete(0, END)
        self.reasonhas.delete(0, END)
        self.show()

def showstatement(userid):
    picon = ImageTk.PhotoImage(Image.open("data/images/statements_icon.png"))
    popup = Toplevel(root)
    popup.iconphoto(False, picon)
    popup.grab_set()
    popup.resizable(0, 0)
    a0 = int(root.wm_maxsize()[0])
    a1 = int(root.wm_maxsize()[1])
    fw = a0/1.47
    fh = a1/1.3
    popup.geometry(f"{int(fw)}x{int(fh)}+{int(a0/2 - fw/2)}+{int(a1/2 - fh/2)}")
    popup.configure(bg="white")
    popup.title("Directrix- Statement")
    popup.focus_set()

    txt = Text(popup, font=("Courier New", x(17)), bg="white", width=x(70), height=y(15))
    txt.place(x=x(15), y=y(8))

    pt = BankStatement(userid, txt)
    pt.show()

    sortby = Label(popup, text="Sort by:", font=("Arial", x(22)), bg="white")
    sortby.place(x=x(15), y=y(400))
    sorting = IntVar()
    sb_credits = Radiobutton(popup, text="Credits Only", font=("Arial", x(15)), variable=sorting, value=1, bg="#fff")
    sb_credits.place(x=x(120), y=y(400))
    sb_debits = Radiobutton(popup, text="Deposits Only", font=("Arial", x(15)), variable=sorting, value=2, bg="#fff")
    sb_debits.place(x=x(260), y=y(400))
    sb_reset = Radiobutton(popup, text="Both", font=("Arial", x(15)), variable=sorting, value=0, bg="#fff")
    sb_reset.place(x=x(415), y=y(400))
    pt.sortval = sorting

    filterby = Label(popup, text="Filters:", font=("Arial", x(22)), bg="white")
    filterby.place(x=x(15), y=y(450))

    fb_amt = Label(popup, text="Amount\n"
                               " |- Greater than:\n"
                               " |- Less than:", font=("Arial", x(22)), bg="white", justify=LEFT)
    fb_amt.place(x=x(130), y=y(450))
    amtgt = Entry(popup, width=x(8), font=("Helvetica", x(18)), bg="#BFE5FF")
    amtgt.place(x=x(340), y=y(488))
    amtlt = Entry(popup, width=x(11), font=("Helvetica", x(18)), bg="#BFE5FF")
    amtlt.place(x=x(302), y=y(522))
    pt.gamtval = amtgt
    pt.lamtval = amtlt

    fb_dt = Label(popup, text="Older Than", font=("Arial", x(22)), bg="white")
    fb_dt.place(x=x(475), y=y(450))
    olderthan = IntVar()
    dt_none = Radiobutton(popup, text="Reset", variable=olderthan, value=0, font=("Helvetica", x(18)), bg="#ffffff")
    dt_none.place(x=x(482), y=y(485))
    dt_3m = Radiobutton(popup, text="3 Months", variable=olderthan, value=3, font=("Helvetica", x(18)), bg="#ffffff")
    dt_3m.place(x=x(482), y=y(515))
    dt_6m = Radiobutton(popup, text="6 Months", variable=olderthan, value=6, font=("Helvetica", x(18)), bg="#ffffff")
    dt_6m.place(x=x(482), y=y(545))
    dt_1y = Radiobutton(popup, text="1 Year", variable=olderthan, value=12, font=("Helvetica", x(18)), bg="#ffffff")
    dt_1y.place(x=x(482), y=y(575))
    pt.older = olderthan

    fb_reason = Label(popup, text="Reason", font=("Arial", x(22)), bg="white")
    fb_reason.place(x=x(700), y=y(450))
    reason = IntVar()
    fb_none = Radiobutton(popup, text="Reset", variable=reason, value=0, font=("Helvetica", x(18)), bg="#ffffff")
    fb_none.place(x=x(707), y=y(485))
    fb_has = Radiobutton(popup, text="Must Have:", variable=reason, value=1, font=("Helvetica", x(18)), bg="#ffffff")
    fb_has.place(x=x(707), y=y(515))
    fb_is = Radiobutton(popup, text="Must Be:", variable=reason, value=2, font=("Helvetica", x(18)), bg="#ffffff")
    fb_is.place(x=x(707), y=y(545))
    reasonhas = Entry(popup, width=x(12), font=("Helvetica", x(18)), bg="#BFE5FF")
    reasonhas.place(x=x(860), y=y(517))
    reasonis = Entry(popup, width=x(14), font=("Helvetica", x(18)), bg="#BFE5FF")
    reasonis.place(x=x(835), y=y(549))
    pt.reasonval = reason
    pt.reasonis = reasonis
    pt.reasonhas = reasonhas

    apply_filters = Button(popup, text="Apply All", font=("Arial", x(15)), bg="#FFCF61",
                        command=pt.show)
    apply_filters.place(x=x(400), y=y(620))
    reset_filters = Button(popup, text="Reset Filters", font=("Arial", x(15)), bg="#81a9fd",
                           command=pt.resetfilters)
    reset_filters.place(x=x(500), y=y(620))

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

with open("data/fd.json", "r") as f:
    root.fd = json.load(f)

bg_canvas = Canvas(root, width=root.x, height=root.wm_maxsize()[1])
bg_canvas.place(x=x(0), y=y(0))
root.rootbgimage = bg_canvas.create_image(0, 0, image=root.bgimg, anchor="nw")

mainbg = Frame(root, width=root.wm_maxsize()[0], height=25)
mainbg.place(x=x(0), y=y(0))
close = Button(mainbg, text="Close", command=root.destroy)
close.place(x=(root.x- x(42)), y=y(2))
restore = Button(mainbg, text="Restore", command=restore_root)
restore.place(x=(root.x- x(93)), y=y(2))

login_field = Entry(root, width=x(25), font=("Helvetica", x(22)))
login_field.place(x=x(95), y=y(350))

password_field = Entry(root, width=x(25), font=("Helvetica", x(22)), show="*")
password_field.place(x=x(95), y=y(490))
cacheid = root.cache.get("id")
if cacheid is not None:
    login_field.insert(0, cacheid)
    password_field.focus_set()
else: login_field.focus_set()

submit_login = Button(root, text="Login", font=("Arial", x(18)), width=x(14), bg="#62E1FF", command=create_login)
submit_login.place(x=x(85), y=y(600))

submit_create = Button(root, text="Create Account", font=("Arial", x(18)), width=x(14), bg="#62E1FF", command=submit_data)
submit_create.place(x=x(300), y=y(600))

status = Label(root, font=("Helvetica", x(16)), bg="#ffffff", fg="#FF0000")

fs = root.cache.setdefault("fs", True)
if not fs: restore_root()
cacheupdate()

root.mainloop()