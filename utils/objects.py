import random
import string
import sys
from minesweeper import Server
from flask_socketio import SocketIO
from typing import Dict, Tuple

sys.path.append("..")

clearMine_socketio = SocketIO()
cookie_user_dict: Dict[str, Tuple[str, float]] = {}
user_cookie: Dict[str, str] = {}

CM_server = Server()


def gen_cookie():
    digits = string.digits
    cookie = ''.join(random.choices(digits, k=25))
    return int(cookie)
