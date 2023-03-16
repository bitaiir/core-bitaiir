# Imports
from network.peers import Params
from network.peers.Peer import Peer
from tools.Debug import Debug
from tools.ping import Ping


class PeerManager:
    def __init__(self):
        self.peers = []

    def add_peer(self, address, peer_type):

        # Vars;
        connect_error = False

        # Get IP address;
        ip_address = address[0]

        # Get port;
        port_address = address[1]

        # Create peer;
        peer = Peer(address)

        # Get external peer public ipv4;
        external_ip = peer.get_external_ip()

        # Verify max peers;
        if len(self.peers) >= Params.MAX_PEERS:
            return Debug.error("Peers: {0} | Max peers  is: {1}!".format(len(self.peers), str(Params.MAX_PEERS)))
        elif external_ip == address[0]:
            return Debug.error("External IPv4 is equal to DNS seed peer!")
        else:
            # Verify peers address;
            for peer in self.peers:
                if peer.address == address:
                    return Debug.error("peer address: {0} is equal to new peer: {1}!".format(str(peer.address), str(address)))

            # Debug;
            Debug.log("Ping command start in {0}.".format(str(ip_address)))

            # Ping peer;
            ping_result = self.ping(ip_address)

            if not ping_result:
                # Ping error;
                Debug.error("Ping Timeout: peer address {0} removed!".format(str(ip_address)))

                if self.peers:
                    # Remove peer address;
                    self.peers.remove(peer)

            else:

                # Debug;
                Debug.log("Ping sucess.")

                if peer_type == "discovery":
                    # Connect peer;
                    connect_error = peer.connect()

                if not connect_error:

                    if peer_type == "discovery":
                        # Verify peer network protocol;
                        status_peer = self.verify_peer(peer, "discovery")
                    else:
                        status_peer = self.verify_peer(peer, "listen")

                    if status_peer:

                        # Debug;
                        Debug.log("Adding peer: {0}".format(str(address)))

                        # Add peer in list;
                        self.peers.append(peer)

                    else:
                        Debug.error("Status peer error!")

    def verify_peer(self, peer, peer_type):
        # Vars;
        status_peer = True

        if peer_type == "discovery":

            # Receive message;
            received_message = peer.receive_message_listen()

            if received_message != "bitaiir":
                status_peer = False
        else:
            # Send message;
            peer.send_message_listen("bitaiir")

        return status_peer

    def ping(self, address):
        try:
            # Objects;
            ping = Ping()

            # Create ping command;
            ping_result = ping.command_ping(address, 5, 1000)

            return ping_result

        except Exception as error:
            Debug.error("Ping: error: {0}.".format(str(error)))
