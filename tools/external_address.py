# Imports
from tools.logger import Logger
import requests
import re
import time


class ExternalAddress:

    def getExternalAddress(self):
        # Objects;
        logger = Logger("external_address", "external_address.log", "debug")

        # Make a request to checkip.dyndns.org as proposed
        # in https://en.bitcoin.it/wiki/Satoshi_Client_Node_Discovery#DNS_Addresses
        try:
            # Create request to get response in text;
            response = requests.get("http://checkip.dyndns.org").text

            # Sleep 5 seconds;
            time.sleep(5)

            # Filter the response with a regex for an IPv4 address
            ip_match = re.search("(?:[0-9]{1,3}\.){3}[0-9]{1,3}", response)

            if ip_match is not None:
                ip = ip_match.group()
            else:
                raise Exception("Failed to retrieve external IP address")

        except Exception as error:
            ip = "127.0.0.1"
            logger.print_logger("error", str(error))

        return ip
# # Debug
# if __name__ == "__main__":
#     externalAddress = ExternalAddress()
#     my_external_ip = externalAddress.getExternalAddress()
#     print(my_external_ip)
