import base64
import os
import threading
from tkinter.constants import END
from typing import Tuple

import requests as r
import websocket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

ilo_user: str = "https://0.0.0.0:8000/user"
api_key: str = "399d79ac-8725-11eb-83c2-acde48001122"


def get_personal_private_key(username: str) -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    """Retrieves a private and public from disk for a specified username.

    Args:
        username (str): The username to get the private key of

    Returns:
        Tuple[RSA.RsaKey, RSA.RsaKey]: [Private Key, Public Key]
    """
    private_key = None
    if not os.path.exists(f"users/{username}"):
        os.mkdir(f"users/{username}")
        private_key = RSA.generate(4096)
        with open(f"users{os.sep}{username}{os.sep}private_key.pem", "w") as f:
            f.write(private_key.export_key().decode("utf-8"))
    elif os.path.isfile(f"users{os.sep}{username}{os.sep}private_key.pem"):
        with open(f"users{os.sep}{username}{os.sep}private_key.pem", "r") as f:
            private_key = RSA.import_key(f.read())
    else:
        private_key = RSA.generate(4096)
        with open(f"users{os.sep}{username}{os.sep}private_key.pem", "w") as f:
            f.write(private_key.export_key().decode("utf-8"))
    return private_key, private_key.public_key()


def register(username: str, password: str) -> bool:
    """
    Registers with Ilo with the provided username and password.
    The cryptographic keys will be created automatically

    Args:
        username (str): Username to register with
        password (str): Password of the username

    Returns:
        bool: True or False indication the success of a registration
    """
    private_key = RSA.generate(4096)
    public_key = private_key.public_key()
    public_key_str: str = base64.b64encode(public_key.export_key("DER")).decode()
    response = r.post(
        ilo_user,
        json = {
            "username": username,
            "password": password,
            "public_key": public_key_str,
            "api_key": api_key,
        },
        verify=False,
    )
    if response.status_code == 201:
        if not os.path.exists(f"users/{username}"):
            os.mkdir(f"users/{username}")
        with open(f"users{os.sep}{username}{os.sep}private_key.pem", "w") as f:
            f.write(private_key.export_key().decode("utf-8"))
        return True
    return False


def connect_new_chatroom(self, name: str):
    self.ws.close()
    self.textCons.delete(1.0,END)
    self.ws = websocket.WebSocketApp(
        f"ws://localhost:4000/ws/{name}", on_message=self.message
    )
    self.run_thread = threading.Thread(target=self.run)
    self.run_thread.start()
