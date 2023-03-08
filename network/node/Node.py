# Imports
from network.params import Params
from tools.Debug import Debug
import socket
import threading


class Node:

    def __init__(self, host, port, peers):
        # Vars;
        self.host = host
        self.port = port
        self.peers = peers

        # Sockets;
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(Params.MAX_LISTEN)
        #
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        # Server threads.
        server_thread = threading.Thread(target=self.handle_server_connections)
        server_thread.start()

        # Client threads.
        client_thread = threading.Thread(target=self.handle_client_connections)
        client_thread.start()

        # Join threads;
        server_thread.join()
        client_thread.join()

    def handle_server_connections(self):
        while True:
            # Accept incoming connection from server;
            client_socket, client_address = self.server_socket.accept()
            Debug.log(f'Incoming connection received from {client_address[0]}:{client_address[1]}')

            # Inicia a thread de comunicação do servidor
            server_thread = threading.Thread(target=self.handle_server_client, args=(client_socket,))
            server_thread.start()

    def handle_server_client(self, client_socket):
        # Lógica de comunicação do servidor com o cliente
        pass

