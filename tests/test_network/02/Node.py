# Imports
from tools.Debug import Debug
from network.peers.PeerDiscovery import PeerDiscovery
from network.peers.PeerManager import PeerManager
from network.peers.PeerListen import PeerListen
from network.peers import Params
import threading
import pyfiglet
import time


class Node:

    def __init__(self):
        self.discoverying_peers = True

        # Start node;
        self.start_node()

    def start_node(self):
        # Start informations;
        self.start_infos()

        # Threading for search new peers;
        thread_listen_peers = threading.Thread(target=self.listen_peers)
        thread_discovery_peers = threading.Thread(target=self.discovery_peers)

        # Start threads;
        thread_listen_peers.start()
        time.sleep(3)
        thread_discovery_peers.start()

    def start_infos(self):
        # Vars.
        ascii_logo = pyfiglet.figlet_format("bitaiir", font="banner3-D")

        # Debug;
        Debug.art_ascii(ascii_logo)

    def listen_peers(self):
        # Debug;
        Debug.info("Starting listen for new peers...")

        # Objects;
        peer_listen = PeerListen()

        # Listen for peers;
        peer_listen.listen_for_peers()

    def discovery_peers(self):

        # Objects;
        peer_discovery = PeerDiscovery()
        peer_manager = PeerManager()

        # Verifying new peers in DNS seeds;
        while self.discoverying_peers:
            # Debug;
            Debug.info("Starting discovery new peers...")

            # New peers addresses;
            new_peers = peer_discovery.discover_peers()

            # Add new peers;
            for address in new_peers:
                # Debug;
                Debug.log("Start add process to new peer address: {0}.".format(address))

                # Add peer;
                peer_manager.add_peer(address, "discovery")

            # Sleep;
            time.sleep(Params.PING_INTERVAL)


if __name__ == "__main__":
    node_test = Node()
