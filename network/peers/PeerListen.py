# Imports
from tools.Debug import Debug
from tools.LocalAddress import LocalAddress
from network.peers.PeerManager import PeerManager
from network.peers.Peer import Peer


class PeerListen:

    def listen_for_peers(self):
        # Objects;
        get_local_address = LocalAddress()
        peer_manager = PeerManager()

        # Get local IPv4 address;
        local_address = get_local_address.getLocalAddress()

        # Create peer;
        peer = Peer(local_address)

        # Bind socket listen;
        peer.bind_socket()

        # Listen socket;
        peer.listen()

        while True:

            # Accept connection;
            connection, address = peer.accept()

            # Debug log;
            Debug.log("New connection: {0}".format(str(address)))

            # Add peer;
            peer_manager.add_peer(peer.address, "listen")




