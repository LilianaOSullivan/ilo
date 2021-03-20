import base64
import os
from typing import Tuple

import requests as r
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

ilo_user: str = "0.0.0.0:8000/user"
api_key: str = "399d79ac-8725-11eb-83c2-acde48001122"


def get_personal_private_key(username: str) -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    private_key = None
    if os.path.isfile(f"{username}{os.sep}private_key.pem"):
        with open(f"{username}{os.sep}private_key.pem", "r") as f:
            private_key = RSA.import_key(f.read())
    else:
        private_key = RSA.generate(4096)
        with open(f"{username}{os.sep}private_key.pem", "w") as f:
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
    if not os.path.exists(username):
        os.makedirs(username)
    with open(f"{username}{os.sep}private_key.pem", "w") as priv_key, open(
        "public_key.pem", "w"
    ) as pub_key:
        priv_key.write(private_key.export_key().decode("utf-8"))
        pub_key.write(public_key.export_key().decode("utf-8"))
    public_key_str: str = base64.b64encode(public_key.export_key("DER")).decode()
    response = r.post(
        ilo_user,
        json={
            "username": username,
            "password": password,
            "public_key": public_key_str,
            "api_key": api_key,
        },
    )
    return response.status_code == 201
