# Imports
from network.peers.Peer import Peer
from network.peers import Params
from tools.Debug import Debug
import socket
import time


class PeerManager:
    def __init__(self):
        self.peers = []

    def add_peer(self, address):
        if len(self.peers) >= Params.MAX_PEERS:
            return
        for peer in self.peers:
            if peer.address == address:
                return
        Debug.log("Adding Peer: {0}".format(str(address)))
        peer = Peer(address)
        peer.connect()
        self.peers.append(peer)

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
                    peer.receive_message()
                    peer.last_ping = now
                except:
                    self.peers.remove(peer)
