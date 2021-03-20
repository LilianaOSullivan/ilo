import base64
import json
import threading
from tkinter import *

import requests as r
import tkmacosx
import websocket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import helpers

private_key, public_key = helpers.get_personal_private_key()
encrypt_me = PKCS1_OAEP.new(public_key).encrypt
decrypt_me = PKCS1_OAEP.new(private_key).decrypt

with open("otherPrK.pem") as f:
    private_key = RSA.import_key(f.read())
with open("otherpK.pem") as f:
    public_key = RSA.import_key(f.read())

encrypt_other = PKCS1_OAEP.new(public_key).encrypt
decrypt_other = PKCS1_OAEP.new(private_key).decrypt


def jsonify(m: str):
    m_encrypted = encrypt_other(m.encode("utf-8"))
    sending = base64.b64encode(m_encrypted).decode()
    return json.dumps({"data": {"message": sending}})


class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
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
            command=lambda: helpers.register(
                self.entry_name.get(), self.entry_password.get()
            ),
        )
        self.register_button.place(x=20, y=300, width=74, height=34)

        def message(ws, m):
            for decrypt in [decrypt_me, decrypt_other]:
                try:
                    received = base64.b64decode(m)
                    m = decrypt(received).decode("utf-8")
                    break
                except Exception:
                    pass
            else:
                m = self.msg
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, m + "\n\n")
            self.textCons.config(state=DISABLED)
            self.textCons.see(END)

        self.ws = websocket.WebSocketApp(
            "ws://localhost:4000/ws/chat",
            on_message=message,
        )
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        self.rcv = threading.Thread(target=self.run)
        self.rcv.start()

    def run(self):
        self.ws.run_forever()

    def layout(self, name):
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
        self.Window.bind("<Return>", lambda x: self.send_button(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.textCons.config(cursor="arrow")
        scrollbar = Scrollbar(self.textCons, bg="#1e1e1e")
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

    def send_button(self, msg):
        self.textCons.config(state=DISABLED)
        self.entryMsg.delete(0, END)
        self.msg = msg
        send_thread = threading.Thread(
            target=lambda x: self.ws.send(jsonify(x)), args=(msg,)
        )
        send_thread.start()


g = GUI()
