from tkinter import *
from tkinter import messagebox  # ? Caused by __all__ ?
import helpers
import tkmacosx


def login(self):
    self.login = Toplevel(bg="#1e1e1e")
    self.login.title("Ilo Login")
    self.login.resizable(width=False, height=False)
    self.login.configure(width=505, height=365)
    self.title_message = Label(
        self.login,
        text="Please login to continue",
        justify=CENTER,
        font="Helvetica 14 bold",
        bg="#1e1e1e",
        fg="#ffffff",
    )
    self.title_message.place(x=160, y=30, width=213, height=30)
    self.label_name = Label(
        self.login,
        text="Username",
        font="Helvetica 13",
        bg="#1e1e1e",
        fg="#ffffff",
    )
    self.label_name.place(x=220, y=90, width=70, height=25)
    self.entry_name = Entry(
        self.login,
        font="Helvetica 14",
        bg="#1e1e1e",
        fg="#ffffff",
        highlightcolor="#505050",
        highlightbackground="#505050",
        highlightthickness="0",
    )
    self.entry_name.place(x=150, y=120, width=210, height=37)
    self.entry_name.focus()
    self.entry_password = Entry(
        self.login,
        show="*",
        font="Helvetica 14",
        bg="#1e1e1e",
        fg="#ffffff",
        highlightcolor="#505050",
        highlightbackground="#505050",
        highlightthickness="0",
    )
    self.entry_password.place(x=150, y=230, width=210, height=37)
    self.password_label = Label(
        self.login,
        text="Password",
        font="Helvetica 13",
        bg="#1e1e1e",
        fg="#ffffff",
    )
    self.password_label.place(x=220, y=200, width=70, height=25)
    self.login_button = tkmacosx.Button(
        self.login,
        text="Login",
        command=lambda: self.goAhead(self.entry_name.get()),
        borderless=1,
        bg="#1e1e1e",
        fg="#ffffff",
    )
    self.login_button.place(x=210, y=300, width=78, height=34)
    self.register_button = tkmacosx.Button(
        self.login,
        text="Register",
        borderless=1,
        bg="#1e1e1e",
        fg="#ffffff",
        command=lambda: _register_command(self),
    )
    self.register_button.place(x=20, y=300, width=74, height=34)


def chatroom(self, name):
    self.name = name
    self.Window.deiconify()
    self.Window.title("Ilo")
    self.Window.resizable(width=False, height=False)
    self.Window.configure(width=470, height=550, bg="#1e1e1e")
    self.labelHead = Label(
        self.Window,
        bg="#1e1e1e",
        fg="#ffffff",
        text=self.name,
        font="Helvetica 13 bold",
        pady=12,
    )
    self.labelHead.place(relwidth=1)
    self.textCons = Text(
        self.Window,
        width=20,
        height=2,
        bg="#1e1e1e",
        fg="#ffffff",
        font="Helvetica 14",
        padx=5,
        pady=5,
        borderwidth=0,
    )
    self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
    self.labelBottom = Label(self.Window, bg="#1e1e1e", height=80)
    self.labelBottom.place(relwidth=1, rely=0.825)
    self.entryMsg = Entry(
        self.labelBottom,
        bg="#1e1e1e",
        fg="#ffffff",
        font="Helvetica 13",
        borderwidth=0,
    )
    self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
    self.entryMsg.focus()
    self.buttonMsg = tkmacosx.Button(
        self.labelBottom,
        text="Send",
        font="Helvetica 12 bold",
        width=20,
        bg="#1e1e1e",
        fg="#ffffff",
        borderless=1,
        command=lambda: self.send_button(self.entryMsg.get()),
    )
    self.newChat = tkmacosx.Button(
        self.Window,
        text="New Chatroom",
        font="Helvetica 11 bold",
        width=120,
        bg="#1e1e1e",
        fg="#ffffff",
        borderless=1,
        command=lambda: _popup(self),
    )
    self.newChat.place(x=10, y=10)
    self.Window.bind("<Return>", lambda x: self.send_button(self.entryMsg.get()))
    self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
    self.textCons.config(cursor="arrow")
    scrollbar = Scrollbar(self.textCons, bg="#1e1e1e")
    scrollbar.place(relheight=1, relx=0.974)
    scrollbar.config(command=self.textCons.yview)
    self.textCons.config(state=DISABLED)


def _popup(self):
    self.popup = Toplevel(self.Window)
    self.l = Label(self.popup,text="Chatroom name")
    self.l.pack()
    self.e = Entry(self.popup)
    self.e.pack()
    self.b=tkmacosx.Button(self.popup,text="Connect",command=lambda:_popup_cleanup(self))
    self.b.pack()
    self.Window.wait_window(self.popup)

def _popup_cleanup(self):
    name = self.e.get()
    helpers.connect_new_chatroom(self,name)
    self.popup.destroy()
    del self.popup

def _register_command(self):
    username: str = self.entry_name.get()
    password: str = self.entry_password.get()
    if helpers.register(username, password):
        self.login.destroy()
        chatroom(self, username)
    else:
        messagebox.showwarning(
            "Ilo", "This username and password could not be registered"
        )
