from tests.Client import Client
from tests.Server import Server


class Node:

    def __init__(self):

        try:
            client = Client()
        except:
            pass

        try:
            server = Server()
        except:
            pass

# Start
if __name__ == "__main__":
    # Debug
    node = Node()
