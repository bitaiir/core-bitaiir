# Imports
from network.peers import Params
from tools.LocalAddress import LocalAddress
from tools.Debug import Debug
import socket


class PeerServer:
    def __init__(self):
        # Create socket;
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Objects;
        self.local_address = LocalAddress()

        # Get local IPv4;
        self.local_ip = self.local_address.getLocalAddress()

    def bind_socket(self):
        try:

            # Bind socket;
            self.socket.bind((self.local_ip, Params.DEFAULT_PORT))

            # Debug;
            Debug.log("Socket bind sucess!")

        except Exception as error:
            Debug.error("Bind: {0}".format(str(error)))

    def listen_connection(self):
        try:
            # Listen socket;
            self.socket.listen()

            # Debug;
            Debug.log("Socket listening in {0}:{1}".format(str(self.local_ip), str(Params.DEFAULT_PORT)))

        except Exception as error:
            Debug.error("Listen: {0}".format(str(error)))

    def accept_connection(self):
        try:
            # Accept socket;
            connection, address = self.socket.accept()

            return connection, address
        except Exception as error:
            Debug.error("Accept: {0}".format(str(error)))

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
