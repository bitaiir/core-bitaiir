# Imports
from network.peers import Params
import socket


class Peer:
    def __init__(self, address):
        self.address = address
        self.socket = None
        self.last_ping = 0

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.socket.connect(self.address)

    def send_message(self, message):
        message_bytes = Params.MAGIC_BYTES + message.encode("ascii")
        self.socket.sendall(message_bytes)

    def receive_message(self):
        magic = self.socket.recv(7)
        if magic != Params.MAGIC_BYTES:
            raise ValueError("Invalid magic bytes")
        length = int.from_bytes(self.socket.recv(7), byteorder='little')
        message = self.socket.recv(length)
        return message.decode('ascii')

    def close(self):
        self.socket.close()
