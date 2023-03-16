# Imports
from tools.Debug import Debug
import requests
import re


class ExternalAddress:

    def getExternalAddress(self):
        # Make a request to checkip.dyndns.org as proposed
        # in https://en.bitcoin.it/wiki/Satoshi_Client_Node_Discovery#DNS_Addresses
        try:
            response = requests.get('http://checkip.dyndns.org').text

            # Filter the response with a regex for an IPv4 address
            ip = re.search("(?:[0-9]{1,3}\.){3}[0-9]{1,3}", response).group()
            return ip
        except Exception as error:
            Debug.error(str(error))

# # Debug
# if __name__ == "__main__":
#     externalAddress = ExternalAddress()
#     my_external_ip = externalAddress.getExternalAddress()
#     print(my_external_ip)
