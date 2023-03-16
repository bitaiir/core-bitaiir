# Imports
from tools.logger import Logger
import socket


class LocalAddress:

    def getLocalAddress(self):
        # Objects;
        logger = Logger("local_address", "local_address.log", "debug")

        # Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)

        try:
            s.connect(('10.254.254.254', 1))   # Doesn't even have to be reachable;
            local_ip = s.getsockname()[0]
        except Exception as error:
            local_ip = "127.0.0.1"
            logger.print_logger("error", str(error))
        finally:
            s.close()

        return local_ip

# # Debug
# if __name__ == "__main__":
#     localAddress = LocalAddress()
#     my_local_ip = localAddress.getLocalAddress()
#     print(my_local_ip)
