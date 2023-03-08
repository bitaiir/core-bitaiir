# Imports
from tools.Debug import Debug
from tests.Params import  *
from datetime import datetime
import socket
import threading


class Client:

    def __init__(self):
        print("Starting Client")

        # Objects
        s = socket.socket()
        Debug.log("Connecting to {0}:{1}...".format(str(HOST), str(PORT)))

        # Connect to the server;
        s.connect((HOST, PORT))
        Debug.log("Connected.")

        # Prompt the client for a name;
        name = input("Enter your name: ")

        # Make a thread that listens for messages to this client & print them;
        t = threading.Thread(target=self.listenMessages, args=(s, ))

        # Make the thread daemon so it ends whenever the main thread ends;
        t.daemon = True

        # Start the thread;
        t.start()

        while True:
            # Input message we want to send to the server;
            to_send = input("")

            # Way to exit the program;
            if to_send.lower() == "q":
                break

            # Add the datetime, name & the color of the sender;
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            to_send = f"[{date_now}] {name}: {to_send}"

            # Finally, send the message;
            s.send(to_send.encode())

        # Close the socket;
        s.close()

    def listenMessages(self, s):
        while True:
            message = s.recv(1024).decode()
            Debug.log(str(message))
