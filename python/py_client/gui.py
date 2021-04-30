import base64
import json
import threading
import os
from tkinter import *

import websocket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import helpers
import gui_layouts

private_key, public_key = None, None
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
    def message(self, ws, m):
        for decrypt in [self.decrypt_me, decrypt_other]:
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

    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
        gui_layouts.login(self)

        self.ws = websocket.WebSocketApp(
            "ws://localhost:4000/ws/testroom",
            on_message=self.message,
        )
        self.Window.mainloop()

    def goAhead(self, name):
        # ? This might not be needed
        self.private_key, self.public_key = helpers.get_personal_private_key(name)
        self.encrypt_me = PKCS1_OAEP.new(self.public_key).encrypt
        self.decrypt_me = PKCS1_OAEP.new(self.private_key).decrypt

        self.login.destroy()
        gui_layouts.chatroom(self, name)
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()

    def run(self):
        self.ws.run_forever()

    def send_button(self, msg):
        self.textCons.config(state=DISABLED)
        self.entryMsg.delete(0, END)
        self.msg = msg
        send_thread = threading.Thread(
            target=lambda x: self.ws.send(jsonify(x)), args=(msg,)
        )
        send_thread.start()


if not os.path.exists("users"):
    os.mkdir("users")
g = GUI()