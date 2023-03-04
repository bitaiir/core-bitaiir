# Imports
from network.peers.PeerClient import PeerClient
from network.peers import Params
from tools.ExternalAddress import ExternalAddress
from tools.Debug import Debug
import time


class PeerManager:
    def __init__(self):
        self.peers = []

    def add_peer(self, address):

        # Objects;
        external_address = ExternalAddress()

        # Get local IPv4;
        external_ip = external_address.getExternalAddress()

        if address[0] == external_ip:
            # Debug.error("Your public IPv4 is equal in peer list!")
            error = True
            return error

        if len(self.peers) >= Params.MAX_PEERS:
            error = True
            return error
        for peer in self.peers:
            if peer.address == address:
                Debug.error("Address is equal")
                error = True
                return error

        # Create peer;
        peerClient = PeerClient(address)

        try:
            # Connect peer;
            peerClient.connect()

        except Exception as error:
            Debug.error("Connect to {0}: {1}".format(str(address), str(error)))
            error = True
            return error

        Debug.log("Adding Peer: {0}".format(str(address)))

        self.peers.append(peerClient)

        error = False

        return error

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
