import tkinter as tk
from tkinter import OptionMenu, StringVar, messagebox
from PIL import Image,ImageTk
import random, string
import json

PASSWORD="click to generate"
complexity = "Special chars"
pass_len = 16
pass_complex = [
    "Lower letters",
    "Lower and Upper",
    "Letters and numbers",
    "Special chars",
]

# generate pass
def generate_pass():
    password_builder = string.ascii_letters

    if complexity == "Letters and numbers":
        password_builder = password_builder + string.digits
    elif complexity == "Special chars":
        password_builder = password_builder + string.digits + string.punctuation

    try:
        pass_len = int(input_len.get())
    except:
        tk.messagebox.showwarning(title=None, message="Pass length must be a number")
    else:
        PASSWORD = ''.join([random.choice(password_builder) for n in range(pass_len)])

        if complexity == "Lower letters":
            PASSWORD = PASSWORD.lower()

        password.delete(0, "end")
        password.insert(0, PASSWORD)

# save pass
def save():
    ws = website.get()
    em = email.get()
    pw = password.get()

    if ws == "" or em == "" or pw == "":
        tk.messagebox.showwarning(title=None, message="Fill all the fields")
    else:
        from pathlib import Path
        Path("./generated_pswrds").mkdir(parents=True, exist_ok=True)

        dict = {ws: {"Email": em, "Password": pw}}
        

        try:
            data = open(f"./generated_pswrds/all_data.json", "r")
        except FileNotFoundError:
            hold = dict
        else: 
            hold = json.load(data)
            hold.update(dict)
        finally:
            data = open(f"./generated_pswrds/all_data.json", "w")
            json.dump(hold, data, indent=4)
            data.close()

            #clear
            website.delete(0, "end")
            email.delete(0, "end")
            password.delete(0, "end")
            tk.messagebox.showinfo(title=None, message="Saved!")

# searcn
def search():
    try:
        with open("./generated_pswrds/all_data.json") as data:
            hold = json.load(data)
            ws = website.get()
            pw = hold[ws]["Password"]
            em = hold[ws]["Email"]
    except FileNotFoundError:
        tk.messagebox.showwarning(title=None, message="No passwords generated")
    except KeyError:
        tk.messagebox.showwarning(title=None, message=f"Website {ws} does not exist in db")
    else:
        tk.messagebox.showwarning(title=None, message=f"Email: {em}\nPassword: {pw}")
    
def show_dropdown(option):
    global complexity
    complexity = option
    print(option)




window = tk.Tk()
window.title("Password manager")
window.config(padx=20, pady=20)

canvas = tk.Canvas(window, width=200, height=200)
canvas.grid(column=1, row=0)

psw_icon = ImageTk.PhotoImage(Image.open("./src/icon.png"))
canvas.create_image(136, 100, image=psw_icon)

# datatype of dropdown text
clicked = StringVar()
clicked.set("Special chars")

label_settings = tk.Label(text = "Pass complex")
label_settings.grid(column=0, row=1)
drop = OptionMenu(window, clicked, *pass_complex, command = show_dropdown)
drop.grid(column=1, row=1, columnspan=1)

label_set_length = tk.Label(text = "Pass length")
label_set_length.grid(column=2, row=1)
input_len = tk.Entry(width=2)
input_len.insert(0, pass_len)
input_len.grid(column=3, row=1)

label_ws = tk.Label(text="Website")
label_ws.grid(column=0, row=2)
website = input_ws = tk.Entry(width=21)
input_ws.grid(column=1, row=2)
btn_genarate = tk.Button(text="Search db", width=10, command=search)
btn_genarate.grid(column=2, row=2)

label_em = tk.Label(text="Email")
label_em.grid(column=0, row=3)
email = input_em = tk.Entry(width=35)
input_em.grid(column=1, row=3, columnspan=2)

label_pw = tk.Label(text="Password")
label_pw.grid(column=0, row=4)
password = input_pw = tk.Entry(width=21, textvariable=PASSWORD)
input_pw.grid(column=1, row=4)
btn_genarate = tk.Button(text="Generate", width=10, command=generate_pass)
btn_genarate.grid(column=2, row=4)

btn_save = tk.Button(text="Add", width=33, command=save)
btn_save.grid(column=1, row=5, columnspan=2)

window.mainloop()