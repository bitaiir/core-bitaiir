# Imports
from network.peers import Params
from tools.LocalAddress import LocalAddress
from network.peers.PeerDiscovery import PeerDiscovery
from network.peers.PeerManager import PeerManager
from tools.Debug import Debug
import socket
import threading
import time


class Node:

    def __init__(self):

        # Objects;
        local_address = LocalAddress()

        # Get local IPv4;
        local_ip = local_address.getLocalAddress()

        # # Add peer;
        # peer_manager.add_peer((local_ip, Params.DEFAULT_PORT))

        # Create socket;
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket;
        self.peer_socket.bind((local_ip, Params.DEFAULT_PORT))

        # Debug
        Debug.log("Socket listening in {0}:{1}".format(str(local_ip), str(Params.DEFAULT_PORT)))

        # Socket listen;
        self.peer_socket.listen()

        # Threading for listening new peers;
        t = threading.Thread(target=self.listen_for_peers)
        t.start()

    def listen_for_peers(self):

        Debug.log("Listening for peers...")

        while True:
            # Wait connection;
            connection, address = self.peer_socket.accept()

            # Debug log;
            Debug.log("New connection: {0}".format(str(address)))

            # Processing new connection;
            # Aqui você pode adicionar a lógica específica do seu programa para lidar com as mensagens do protocolo do Bitcoin
            # e sincronizar a blockchain com outros peers

    def search_peers(self):

        peer_manager = PeerManager()
        peer_discovery = PeerDiscovery()

        while True:
            new_peers = peer_discovery.discover_peers()
            for address in new_peers:
                peer_manager.add_peer(address)
            peer_manager.ping_all()
            time.sleep(1)


if __name__ == "__main__":
    node_test = Node()
