# Imports
from tools.external_address import ExternalAddress
from tools.logger import Logger
from network.params import params
import time


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

            # Debug;
            self.logger.print_logger("warning", f"The peer {self.host}:{self.port} already exists!")

        return peer_status

    def server_send_ping(self, socket):
        try:
            while True:
                # Debug;
                self.logger.print_logger("info", f"Send 'ping' message to client: {self.host}.")

                # Send "ping" message to client;
                socket.send("ping".encode())

                # Set timeout to socket;
                socket.settimeout(5.0)

                # Wait answer "pong" from client;
                response = socket.recv(1024)

                # If there is no answer, the connection has dropped;
                if not response:
                    # Debug;
                    self.logger.print_logger("info", "Connection terminated by the other side.")
                    break

                # Verify response;
                if response.decode() == "pong":
                    # Debug;
                    self.logger.print_logger("info", f"Received 'pong' response from client: {self.host}!")
                else:
                    # Debug;
                    self.logger.print_logger("warning", f"Received invalid response from client: {self.host}!")

                # Set time sleep;
                time.sleep(params.PING_INTERVAL * 60)

        except socket.timeout:
            # Debug;
            self.logger.print_logger("error", "Timeout: connection may have been lost.")

        except Exception as error:
            # Debug;
            self.logger.print_logger("error", f"Exception: {error}")

    def client_send_ping(self, socket):
        while True:
            try:
                # Receive "ping" message from server;
                data = socket.recv(1024)

                # Verify message;
                if data.decode() == "ping":
                    # Debug;
                    self.logger.print_logger("info", "Message 'ping' received from server.")

                    # Send "pong" message;
                    socket.send("pong".encode())

                    # Debug;
                    self.logger.print_logger("info", "Message 'pong' send to server.")

                else:
                    # Debug;
                    self.logger.print_logger("error", "Message invalid received from server.")

                # Set time sleep;
                time.sleep(1)

            except Exception as error:
                # Debug;
                self.logger.print_logger("error", f"Exception: {error}")
                break
