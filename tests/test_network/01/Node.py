# Imports
from tests.test_network import PeerDiscovery
from tests.test_network import PeerManager
from tests.test_network import PeerServer
from tools.Debug import Debug
import threading
import time


class Node:

    def __init__(self):

        # Objects;
        self.peer_server = PeerServer()

        # Bind socket;
        self.peer_server.bind_socket()

        # Listen socket;
        self.peer_server.listen_connection()

        # Threading for listening new peers;
        thread_listen_for_peers = threading.Thread(target=self.accept_peers)

        # Threading for search new peers;
        thread_search_peers = threading.Thread(target=self.search_peers)

        # Start threads;
        thread_search_peers.start()
        thread_listen_for_peers.start()

    def accept_peers(self):

        Debug.log("Listening for peers...")

        while True:
            received = False

            # Accept socket connection;
            connection, address = self.peer_server.accept_connection()

            # Debug log;
            Debug.log("New connection: {0}".format(str(address)))

            while not received:
                # Receive message for peer verification;
                received = self.peer_server.receive_message()

            Debug.log("End")

    def search_peers(self):

        # Objects;
        peer_manager = PeerManager()
        peer_discovery = PeerDiscovery()

        while True:
            # Vars;
            error = False

            new_peers = peer_discovery.discover_peers()

            for address in new_peers:
                error = peer_manager.add_peer(address)
                time.sleep(2)

            if not error:
                peer_manager.ping_all()

                time.sleep(2)

                peer_manager.send_messagel("bitaiir")


if __name__ == "__main__":
    node_test = Node()
