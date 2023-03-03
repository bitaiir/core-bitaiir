# Imports
from network.peers.PeerClient import PeerClient
from network.peers import Params
from tools.Debug import Debug
import time


class PeerManager:
    def __init__(self):
        self.peers = []

    def add_peer(self, address):
        if len(self.peers) >= Params.MAX_PEERS:
            return
        for peer in self.peers:
            if peer.address == address:
                Debug.log("Address is equal")
                return

        # Create peer;
        peerClient = PeerClient(address)

        # Connect peer;
        peerClient.connect()

        # Send message to verify peer in network/protocol;

        Debug.log("Adding Peer: {0}".format(str(address)))

        self.peers.append(peerClient)

        # for peer in self.peers:
        #     Debug.log("Peers: {0}".format(str(peer)))

    def send_all(self, message):
        for peer in self.peers:
            try:
                peer.send_message(message)
            except:
                self.peers.remove(peer)

    def receive_all(self):
        messages = []
        for peer in self.peers:
            try:
                message = peer.receive_message()
                messages.append((peer.address, message))
            except:
                self.peers.remove(peer)
        return messages

    def ping_all(self):
        now = int(time.time())
        if now % Params.PING_INTERVAL != 0:
            return
        for peer in self.peers:
            if now - peer.last_ping > Params.PING_INTERVAL:
                try:
                    peer.send_message("ping")
                    time.sleep(1)
                    peer.receive_message()
                    time.sleep(1)
                    peer.last_ping = now
                except Exception as error:
                    Debug.error("[PING] Peer Address {0} removed! Error: {1}.".format(str(peer.address), str(error)))
                    self.peers.remove(peer)
