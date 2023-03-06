# Imports
from tools.LocalAddress import LocalAddress
from network.peers.Peer import Peer


class PeerListen:

    def listen_for_peers(self):
        # Objects;
        get_local_address = LocalAddress()

        # Get local IPv4 address;
        local_address = get_local_address.getLocalAddress()

        # Create peer;
        peer = Peer(local_address)

        # Bind socket listen;
        peer.bind_socket()

        # Listen socket;
        peer.listen()



