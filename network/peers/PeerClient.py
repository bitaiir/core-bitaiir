# Imports
from network.peers import Params
from tools.Debug import Debug
import socket


class PeerClient:
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
        self.socket.send(message_bytes)
        Debug.log("Send message: [ {0} ] | Bytes message: [ {1} ].".format(str(message), str(message_bytes)))

    def receive_message(self):
        magic = self.socket.recv(7)
        Debug.log("Receive magic message: [ {0} ]. | Bytes message: [ {1} ].".format(str(magic.decode("ascii"), str(magic))))

        if magic != Params.MAGIC_BYTES:
            raise ValueError("Invalid magic bytes")

        length = int.from_bytes(self.socket.recv(7), byteorder='little')
        message = self.socket.recv(length)
        Debug.log("Receive message decode: [ {0} ].".format(str(message.decode('ascii'))))

        return message.decode('ascii')

    def close(self):
        self.socket.close()
