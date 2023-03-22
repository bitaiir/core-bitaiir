# Imports
from network.params import params
from network.node.node import Node
from network.peer.peer import Peer
from tools.logger import Logger
from tools.local_address import LocalAddress
import pyfiglet


class Core:

    def __init__(self):
        # Show logo;
        self.show_logo()

        # Objects;
        self.logger = Logger("core", "core.log", "debug")

        # Debug;
        self.logger.print_logger("info", "Starting Core...")

    def show_logo(self):
        # Create ascii logo;
        ascii_logo = pyfiglet.figlet_format("bitaiir", font="banner3-D")

        # Show logo in terminal;
        print(ascii_logo)

    def init(self):
        # Vars;
        local_ip = LocalAddress().getLocalAddress()
        port = params.DEFAULT_PORT

        # Objects;
        local_peer = Peer(local_ip, port)
        node = Node(local_peer.host, local_peer.port)

        # Start node;
        node.run()
