import json
import os.path
import threading
import base64
from tkinter import *

import requests as r
import tkmacosx
import websocket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

private_key = None
if os.path.isfile("private_key.pem"):
    with open("private_key.pem") as f:
        private_key = RSA.import_key(f.read())

breakpoint()