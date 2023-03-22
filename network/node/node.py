# Imports
from network.peer.peer_discovery import PeerDiscovery
from database.database import Database
from network.peer.peer import Peer
from tools.logger import Logger
import socket
import threading
import time


class Node(Peer):

    def __init__(self, host, port):
        super().__init__(host, port)
        # Objects
        self.logger = Logger("node", "node.log", "debug")

        # Vars;
        self.delay_discovery = 30

        # Debug;
        self.logger.print_logger("info", "Starting Node...")

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
        # Objects;
        database = Database()

        # Connect database;
        database.connect()

        while True:
            # Accept incoming connection from server;
            client_socket, client_address = self.server_socket.accept()

            host = client_address[0]
            port = client_address[1]

            # Create peer;
            peer = Peer(host, port)

            # Verify peer;
            peer_status = peer.verify_peer(database)

            if peer_status:

                # Debug;
                self.logger.print_logger("info",
                                         f"Incoming connection received from {client_address[0]}:{client_address[1]}")

                # Add peer in database and save;
                database.add_peer(peer.host, peer.port)

                # Create thread;
                server_thread = threading.Thread(target=self.handle_server_client, args=(client_socket,))

                # Starts thread server communication;
                server_thread.start()

    def handle_server_client(self, client_socket):
        # Server communication logic with the client;
        pass

    def handle_client_connections(self):
        # Objects;
        database = Database()

        # Connect database;
        database.connect()

        while True:

            # Search peers discovery;
            peer_discovery = PeerDiscovery()

            # Get peers;
            new_peers = peer_discovery.discover_peers()

            # Manage new peers;
            for peer in new_peers:
                # Vars;
                host = peer[0]
                port = peer[1]

                # Create peer;
                peer = Peer(host, port)

                # Verify peer;
                peer_status = peer.verify_peer(database)

                if peer_status:

                    # Tries to connect to a node from the peer list;
                    try:
                        # Connect client connection;
                        self.client_socket.connect((peer.host, peer.port))

                        # Add peer in database and save;
                        database.add_peer(peer.host, peer.port)

                        # Debug;
                        self.logger.print_logger("info", f"Outbound connection established with {peer.host}:{peer.port}")

                        # Manage connection;
                        self.handle_client_server()

                    except OSError as error:
                        self.logger.print_logger("warning", f"Could not connect with {peer.host}:{peer.port}! Error: {error}")

            # Sleep and try again;
            time.sleep(self.delay_discovery)

    def handle_client_server(self):
        # Lógica de comunicação do cliente com o servidor
        pass
