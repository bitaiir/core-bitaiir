# Imports
from tools.Debug import Debug
from tests.Params import *
import socket
import threading


class Server:

    def __init__(self):
        print("Starting Server")

        # Vars
        self.server_error = False  # Verify error in server;
        self.client_sockets = set()  # All connected client's sockets;

        try:

            # Objects
            s = socket.socket()  # Create a TCP socket;

            # Socket
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Make the port as reusable port;
            s.bind((HOST, PORT))  # Bind the socket to the address we specified;
            s.listen(5)  # Listen for upcoming connections;

            Debug.log("Listening as {0}:{1}".format(str(HOST), str(PORT)))

            # Start looping
            while not self.server_error:
                client_socket, client_address = s.accept()  # We keep listening for new connections all the time;
                Debug.log("{0} connected.".format(str(client_address)))
                self.client_sockets.add(client_socket)  # Add the new connected client to connected sockets;
                t = threading.Thread(target=self.listenClient, args=(client_socket, client_address,))  # Start a new thread that listens for each client's messages;
                t.daemon = True  # Make the thread daemon, so it ends whenever the main thread ends;
                t.start()  # Start the thread

            # Close client sockets;
            for cs in self.client_sockets:
                cs.close()

            # Close server socket;
            s.close()

        except Exception as error:
            Debug.error(str(error))
            self.server_error = True

    def listenClient(self, cs, ca):
        """
        This function keep listening for a message from `cs` socket
        Whenever a message is received, broadcast it to all other connected clients
        """
        while True:
            try:
                msg = cs.recv(1024).decode()  # Keep listening for a message from `cs` socket;
            except Exception as error:
                Debug.error(str(error))  # Client no longer connected;
                self.client_sockets.remove(cs)  # Remove it from the set;
            else:
                Debug.log("{0}: {1}".format(str(ca), str(msg)))  # Received a message;

            # Iterate over all connected sockets;
            for client_socket in self.client_sockets:
                # Send the message;
                client_socket.send(msg.encode())
                client_socket.send("\n".encode())
