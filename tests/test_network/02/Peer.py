# Imports
from network.peers import Params
from tools.local_address import LocalAddress
from tools.external_address import ExternalAddress
from tools.Debug import Debug
import socket


class Peer:

    def __init__(self, address):
        self.address = address
        self.socket = None
        self.socket_listen = None
        self.last_ping = 0

    def get_local_ip(self):
        # Objects;
        local_address = LocalAddress()

        # Get local IPv4;
        get_local_ip = local_address.getLocalAddress()

        return get_local_ip

    def get_external_ip(self):
        # Objects;
        external_address = ExternalAddress()

        # Get external public IPv4;
        get_external_ip = external_address.getExternalAddress()

        return get_external_ip

    def connect(self):
        try:
            # Vars;
            connect_error = False

            # Debug;
            Debug.log("Connecting in {0}.".format(str(self.address)))

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect(self.address)

            # Debug log;
            Debug.log("New connection: {0}".format(str(self.address)))

            return connect_error

        except Exception as error:
            connect_error = True
            Debug.error("Connect: {0}".format(str(error)))
            return connect_error

    def send_message(self, message):
        message_bytes = Params.MAGIC_BYTES + message.encode("ascii")

        self.socket.send(message_bytes)

        Debug.log("Send message: [ {0} ] | Bytes message: [ {1} ].".format(str(message), str(message_bytes)))

    def receive_message(self):
        try:
            magic = self.socket.recv(7)

            Debug.log("Receive magic message: [ {0} ]. | Bytes message: [ {1} ].".format(str(magic.decode("ascii"), str(magic))))

            if magic != Params.MAGIC_BYTES:
                raise ValueError("Invalid magic bytes")

            length = int.from_bytes(self.socket.recv(7), byteorder="little")

            message = self.socket.recv(length)

            Debug.log("Receive message decode: [ {0} ].".format(str(message.decode("ascii"))))

            return message.decode("ascii")

        except Exception as error:
            Debug.error("Receive: {0}.".format(str(error)))

    def close(self):
        try:
            # Close sockets;
            self.socket.close()
            self.socket_listen.close()

        except Exception as error:
            Debug.error("Close: {0}.".format(str(error)))

# Socket Listen #

    def bind_socket(self):
        try:
            # Get local ip address;
            local_ip = self.get_local_ip()

            # Create socket;
            self.socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind socket;
            self.socket_listen.bind((local_ip, Params.DEFAULT_PORT))

            # Debug;
            Debug.log("Socket bind sucess!")

        except Exception as error:
            Debug.error("Bind: {0}".format(str(error)))

    def listen(self):
        try:

            # Get local ipv4;
            local_ip = self.get_local_ip()

            # Debug;
            Debug.log("Socket listening in {0}:{1}".format(str(local_ip), str(Params.DEFAULT_PORT)))

            # Listen socket;
            self.socket_listen.listen()

        except Exception as error:
            Debug.error("Listen: {0}".format(str(error)))

    def accept(self):
        try:
            # Accept socket;
            connection, address = self.socket_listen.accept()

            return connection, address

        except Exception as error:
            Debug.error("Accept: {0}".format(str(error)))

    def send_message_listen(self, message):
        message_bytes = Params.MAGIC_BYTES + message.encode("ascii")

        self.socket_listen.send(message_bytes)

        Debug.log("Send message: [ {0} ] | Bytes message: [ {1} ].".format(str(message), str(message_bytes)))

    def receive_message_listen(self):
        try:
            magic = self.socket_listen.recv(7)

            Debug.log("Receive magic message: [ {0} ]. | Bytes message: [ {1} ].".format(str(magic.decode("ascii"), str(magic))))

            if magic != Params.MAGIC_BYTES:
                raise ValueError("Invalid magic bytes")

            length = int.from_bytes(self.socket_listen.recv(7), byteorder="little")

            message = self.socket_listen.recv(length)

            Debug.log("Receive message decode: [ {0} ].".format(str(message.decode("ascii"))))

            return message.decode("ascii")

        except Exception as error:
            Debug.error("Receive: {0}.".format(str(error)))
