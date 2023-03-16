# Imports
from network.peer.peer_discovery import PeerDiscovery
from tools.external_address import ExternalAddress
from network.peer.peer import Peer
from tools.logger import Logger
import socket
import threading
import time


class Node(Peer):

    def __init__(self, host, port):
        # Objects
        super().__init__(host, port)
        self.logger = Logger("node", "node.log", "debug")

        # Sockets;
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
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

            # Debug;
            self.logger.print_logger("info", f"Incoming connection received from {client_address[0]}:{client_address[1]}")

            # Starts server communication thread;
            server_thread = threading.Thread(target=self.handle_server_client, args=(client_socket,))
            server_thread.start()

    def handle_server_client(self, client_socket):
        # Server communication logic with the client;
        pass

    def handle_client_connections(self):
        while True:

            # Search peers discovery;
            peer_discovery = PeerDiscovery()

            # Get peers;
            new_peers = peer_discovery.discover_peers()

            # Manage new peers;
            for peer in new_peers:

                # Objects;
                external_ip = ExternalAddress()

                # Vars;
                get_external_ip = external_ip.getExternalAddress()
                host = peer[0]
                port = peer[1]

                # Create peer;
                peer = Peer(host, port)

                if host == get_external_ip:
                    self.logger.print_logger("error", f"It is not possible to connect to peer {host} and the IP is the same as your external address {external_ip}.")

                else:

                    # Tries to connect to a node from the peer list;
                    try:
                        # Connect client connection;
                        self.client_socket.connect((peer.host, peer.port))
                        self.logger.print_logger("info", f"Outbound connection established with {peer.host}:{peer.port}")

                        # Manage connection;
                        self.handle_client_server()

                    except:
                        self.logger.print_logger("error", f"Could not connect with {peer.host}:{peer.port}")

                    # Sleep and try again;
                    time.sleep(10)

    def handle_client_server(self):
        # Lógica de comunicação do cliente com o servidor
        pass
