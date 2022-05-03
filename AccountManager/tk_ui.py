from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

from sql_connector import Connector
import manage_acc as ma

import sys
sys.path.append('C:\dimi_coding\FacePosition\Game')
import manage

connector = Connector("faceposition")

def sign_in():
    username_input = sign_user_entry.get()
    password_input = sign_pass_entry.get()
    credentials = ma.sign_in(username_input, password_input)
    # User signed in
    if credentials == (username_input, password_input):
        username_list = connector.get_data("accounts", "UserName")
        already_taken = False
        for username in username_list:
            if credentials[0] == username:
                already_taken = True
                break
        if already_taken:
            messagebox.showwarning(title="Username already taken", message="The username is already take. \n Please try a new") 
        else:
            connector.add_data("accounts", ("UserName", "Passwd"), (credentials))
            messagebox.showinfo(title="Sign in", message="Successfully signed in")
            window.destroy()
            manage.play(username_input)
    # User not signed in
    else:
        u_ans = credentials[0]; p_ans = credentials[1]
        if u_ans != username_input:
            messagebox.showerror(title="ERROR", message=u_ans)
        else:
            messagebox.showerror(title="ERROR", message=p_ans)


def log_in():
    acc_list = connector.get_data("accounts", "UserName, Passwd")
    username_input = log_user_entry.get()
    password_input = log_pass_entry.get()
    credentials = ma.log_in(username_input, password_input, acc_list)
    # User logged in
    if credentials == username_input:
        messagebox.showinfo(title="Logged in", message=f"Successfully Logged in!\n Welcome {username_input}")
        window.destroy()
        manage.play(username_input)
    # User not logged in
    else:
        messagebox.showerror(title="ERROR", message=credentials)

def guest():
    user = ma.guest()
    window.destroy()
    manage.play(user)


## Tk window UI ##
backgr = "#bdbbfc"
window = Tk()
icon = ImageTk.PhotoImage(Image.open("Images\\lock_icon.jpg"))
window.iconphoto(False, icon)
window.title("Welcome")
window.config(bg=backgr)

long_text = "before we start log in or sign in"
Label(window, text="Welcome!", font=("Arial", 100), bg=backgr).grid(row=0, column=0, columnspan=6)
Label(window, text=long_text, font=("Arial", 15), bg=backgr).grid(row=1, column=1, columnspan=4)

Label(window,height=2, bg=backgr).grid(row=2)
Button(window, text="Play as Guest", bg=backgr, command=guest).grid(row=2, columnspan=6)

entry_width = 30
entry_height = 3

Label(window, text="Username : ", bg=backgr).grid(row=3, column=0)
Label(window, text="Password : ", bg=backgr).grid(row=4, column=0)
log_user_entry = Entry(window, width=entry_width, font=("Arial", 10))
log_user_entry.grid(row=3, column=1, columnspan=2)
log_pass_entry = Entry(window, width=entry_width, font=("Arial", 10), show="*")
log_pass_entry.grid(row=4, column=1, columnspan=2)
Button(window, text="Log in", command=log_in).grid(row=5, column=1)

Label(window, text="Username : ", bg=backgr).grid(row=3, column=3)
Label(window, text="Password : ", bg=backgr).grid(row=4, column=3)
sign_user_entry = Entry(window, width=entry_width, font=("Arial", 10))
sign_user_entry.grid(row=3, column=4, columnspan=2)
sign_pass_entry = Entry(window, width=entry_width, font=("Arial", 10),  show="*")
sign_pass_entry.grid(row=4, column=4, columnspan=2)
Button(window, text="Sign in", command=sign_in).grid(row=5, column=4)

window.mainloop()
