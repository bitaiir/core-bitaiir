# Imports
from tools.external_address import ExternalAddress
from tools.logger import Logger


class Peer:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        # Objects;
        self.logger = Logger("peer", "peer.log", "debug")

    def verify_peer(self, database):
        # Objects;
        external_ip = ExternalAddress()

        # Vars;
        get_external_ip = external_ip.getExternalAddress()
        peer_status = True

        # If external IP is equal a node IP;
        if self.host == get_external_ip:
            # Debug;
            self.logger.print_logger("error",
                                     f"It is not possible to connect to peer {self.host},"
                                     f" the IP is the same as your external address.")

            # Set status;
            peer_status = False

        # Verify if peer exists in database;
        elif database.select_peer(self.host, self.port):
            # Set status;
            peer_status = False

        return peer_status


