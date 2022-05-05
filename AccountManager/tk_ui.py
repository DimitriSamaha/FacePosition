from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from sql_connector import Connector, get_score_history
from manage_acc import Account_handler 
account_handler = Account_handler()

import sys
sys.path.append('C:\dimi_coding\FacePosition\Game')
import manage

connector = Connector("faceposition")
user = "Guest"


def play(form, user:str) -> None:
    """
    This function accepts 1 parameter, user : str \n
    calls manage.play(user) and destroys window \n
    return None
    """
    form.window.destroy()
    manage.play(user)
    return

def new_form(form) -> None:
    form.window.destroy()
    form.__init__()
    return

## Tk window UI ##
class LogForm():
    def __init__(self):
        self.backgr = "#bdbbfc"
        self.window = Tk()
        self.icon = ImageTk.PhotoImage(Image.open("Images\\lock_icon.jpg"))
        self.window.iconphoto(False, self.icon)
        self.window.title("Welcome to FacePosition")
        self.window.config(bg=self.backgr)
        self.frame1 = Frame(self.window, bg=self.backgr)
        self.frame2 = Frame(self.window, bg=self.backgr)
        ### frame 1
        self.frame1.pack()
        # Header
        long_text = "before we start log in or register!"
        Label(self.frame1, text="Welcome!", font=("Arial", 100), bg=self.backgr).grid(row=0, column=0, columnspan=6)
        Label(self.frame1, text=long_text, font=("Arial", 15), bg=self.backgr).grid(row=1, column=1, columnspan=4)

        Label(self.frame1,height=2, bg=self.backgr).grid(row=2)

        #Entrys
        entry_width = 30

        Label(self.frame1, text="Username : ", bg=self.backgr).grid(row=3, column=0)
        Label(self.frame1, text="Password : ", bg=self.backgr).grid(row=4, column=0)
        self.user_entry = Entry(self.frame1, width=entry_width, font=("Arial", 10))
        self.user_entry.grid(row=3, column=1, columnspan=2)
        self.pass_entry = Entry(self.frame1, width=entry_width, font=("Arial", 10), show="*")
        self.pass_entry.grid(row=4, column=1, columnspan=2)

        # Buttons
        Button(self.frame1, text="Play as Guest", bg=self.backgr, command=self.guest).grid(row=3, rowspan=2, column= 3,columnspan=3)
        Button(self.frame1, text="Log in", command=self.log_in).grid(row=5, column=1, pady=5)
        Button(self.frame1, text="Register", command=self.register).grid(row=5, column=2, pady=5)


        self.window.mainloop()

    def create_scroll_bar(self, main_frame):
        # create a canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill="both", expand = 1)
        # add scroll to canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill='y')
        # config the canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        # create another frame inside the canvas
        second_frame = Frame(my_canvas)
        # add that frame to a window in the canvas
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        return second_frame

    def logged_on(self, user:str):
        """
        This function accepts 1 arguments
        return None
        """
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        self.window.geometry(f"{w}x{h+120}")
        self.frame1.destroy()
        self.frame2.pack()
        #frame2 after the log on form
        # Header
        Label(self.frame2, text=f"Welcome {user}", font=("Arial", 30), bg=self.backgr).grid(row=0, column=0, columnspan=6)

        Button(self.frame2, text="Play",width=20 ,command=lambda : play(self, user)).grid(row=1, columnspan=6, pady=10)
        Button(self.frame2, text="Log out", width=10, command= lambda : new_form(self)).grid(row=1, column=5)

        note_book = ttk.Notebook(self.frame2)

        tab1 = Frame(note_book) # new frame for tab1
        tab2 = Frame(note_book) # new frame for tab2
        tab3 = Frame(note_book) # new frame for tab3

        note_book.add(tab1, text="Score history                     ")
        note_book.add(tab2, text="Top ranks, MatchPosition              ")
        note_book.add(tab3, text="Top ranks, FollowPosition             ")
        note_book.grid(row=2, columnspan=6)

        frame_tab1 = self.create_scroll_bar(tab1)
        frame_tab2 = self.create_scroll_bar(tab2)
        frame_tab3 = self.create_scroll_bar(tab3)

        data_list = get_score_history(user)
        for data in data_list:
            Label(frame_tab1, text=data, font=("Arial", 15)).pack()

        rank_match = connector.get_data("scores", column="Game", values="M")
        rank_match.sort(key = lambda a: a[3])
        rank_follow = connector.get_data("scores", column="Game", values="F")
        rank_follow.sort(key = lambda a: a[3])
        r = 0 
        for i in rank_match:
            Label(frame_tab2, text=f"{i[4]} |", font=("Arial", 15)).grid(row=r, column=0)
            Label(frame_tab2, text=f"{i[3]}", font=("Arial", 15)).grid(row=r, column=1)
            Label(frame_tab2, text=f"s by {i[1]}", font=("Arial", 15)).grid(row=r, column=2)
            r += 1
        r = 0 
        for i in rank_follow:
            Label(frame_tab3, text=f"{i[4]} |", font=("Arial", 15)).grid(row=r, column=0)
            Label(frame_tab3, text=f"{i[3]}", font=("Arial", 15)).grid(row=r, column=1)
            Label(frame_tab3, text=f"s by {i[1]}", font=("Arial", 15)).grid(row=r, column=2)
            r += 1
        return
    
    def register(self):
        username_input = self.user_entry.get()
        if username_input[:4].lower() == "guest":
            username_input = "Your username can't begin with guest."
        password_input = self.pass_entry.get()
        credentials = account_handler.register(username_input, password_input)
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
                user = credentials[0]
                self.logged_on(user)
                connector.add_data("accounts", ("UserName", "Passwd"), (credentials))
                messagebox.showinfo(title="Sign in", message="Successfully signed in")
        # User not signed in
        else:
            u_ans = credentials[0]; p_ans = credentials[1]
            if u_ans != username_input:
                messagebox.showerror(title="ERROR", message=u_ans)
            else:
                messagebox.showerror(title="ERROR", message=p_ans)

    
    def log_in(self):
        acc_list = connector.get_data("accounts", "UserName, Passwd")
        username_input = self.user_entry.get()
        password_input = self.pass_entry.get()
        credentials = account_handler.log_in(username_input, password_input, acc_list)
        # User logged in
        if credentials == username_input:
            user = credentials
            self.logged_on(user)
            messagebox.showinfo(title="Logged in", message=f"Successfully Logged in!\n Welcome {username_input}")
        # User not logged in
        else:
            messagebox.showerror(title="ERROR", message=credentials)

    def guest(self):
        user = account_handler.guest()
        manage.play(user)

form = LogForm()
