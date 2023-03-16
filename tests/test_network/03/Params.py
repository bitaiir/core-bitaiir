# Imports
from tools.local_address import LocalAddress

# Vars
localAddress = LocalAddress()  # Get local ip address;
HOST = "{0}".format(str(localAddress.getLocalAddress()))  # Get local IPv4 address;
PORT = 30333  # Port to server socket;
BYTE_SIZE = 1024  # Data size in bytes;
