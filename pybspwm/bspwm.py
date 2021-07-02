import socket
from glob import glob
from os import getenv


class BspwmError(Exception):
    pass


class Bspwm:
    def __init__(self, socket_path=None):
        if socket_path:
            self.socket_path = socket_path
        elif getenv("BSPWM_SOCKET"):
            self.socket_path = getenv("BSPWM_SOCKET")
        else:
            possible_sockets = glob("/tmp/bspwm*_*_*-socket")
            if not possible_sockets or len(possible_sockets) > 1:
                raise ValueError(
                    "Cannot deduce the BSPWM socket path. "
                    + "Passing a value via the socket_path argument is required."
                )
            self.socket_path = possible_sockets[0]

    def __call__(self, *command):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path)
        for word in command:
            s.send(word.encode() + b"\0")
        response = s.recv(4096)
        s.close()
        if response and response[0] == 7:
            raise BspwmError(response[1:-1].decode())
        else:
            return response[:-1].decode()
