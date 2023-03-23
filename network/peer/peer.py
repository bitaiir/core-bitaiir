# Imports
from tools.external_address import ExternalAddress
from tools.logger import Logger
import time


class Peer:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        # Objects;
        self.logger = Logger("peer", "peer.log", "debug")

    def verify_peer(self, database):
        # Objects;
        external_ip = ExternalAddress()

        # Vars;
        get_external_ip = external_ip.getExternalAddress()
        peer_status = True

        # If external IP is equal a node IP;
        if self.host == get_external_ip:
            # Debug;
            self.logger.print_logger("error",
                                     f"It is not possible to connect to peer {self.host},"
                                     f" the IP is the same as your external address.")

            # Set status;
            peer_status = False

        # Verify if peer exists in database;
        elif database.select_peer(self.host, self.port):
            # Set status;
            peer_status = False

            # Debug;
            self.logger.print_logger("warning", f"The peer {self.host}:{self.port} already exists!")

        return peer_status

    def server_send_ping(self, socket):
        # Enviar mensagem "ping" para o cliente
        socket.send("ping".encode())

        # Esperar resposta "pong" do cliente
        data = socket.recv(1024)

        if data.decode() == "pong":
            print(f"Resposta 'pong' recebida do cliente {self.host}")
        else:
            print(f"Resposta inválida recebida do cliente {self.host}")

    def client_send_ping(self, socket):
        # Receber mensagem "ping" do servidor
        data = socket.recv(1024)

        if data.decode() == "ping":
            print("Mensagem 'ping' recebida do servidor")

            # Responder com mensagem "pong"
            socket.send("pong".encode())

            print("Mensagem 'pong' enviada para o servidor")

        else:
            print("Mensagem inválida recebida do servidor")
